from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

from jinja2 import Environment, Template
from jinja2.exceptions import TemplateNotFound
from weasyprint import HTML

from lib.data import JSONDataError
from lib.data_guests import get_data as guests_data
from lib.data_program import get_data as program_data
from lib.data_speakers import get_data as speakers_data
from lib.data_talks import get_data as talks_data
from lib.jinja import JinjaError, get_jinja_env
from lib.paths import PathEnum, PathsError, get_paths

DATA_PROVIDERS: dict[str, Callable] = {
    "program": program_data,
    "guest_invite": guests_data,
    "speaker_email": speakers_data,
    "speaker_invite": speakers_data,
    "speaker_invite_email": speakers_data,
    "talks": talks_data,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Jinja2 template to PDF.")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        choices=["pdf", "html", "txt"],
        default="pdf",
        help="Output format",
    )
    parser.add_argument(
        "-q",
        "--js_filter",
        type=str,
        help="Optional jq filter to apply to the data before rendering",
    )
    parser.add_argument(
        "-t", "--template", type=str, required=True, help="Template name"
    )
    return parser.parse_args()


def generate_docs(args: argparse.Namespace) -> None:

    # Extract arguments
    template_name: str = args.template
    js_filter: str | None = args.js_filter
    output_format: str = args.output

    # Get paths
    templates_path, output_path = get_paths(PathEnum.TEMPLATES, PathEnum.OUTPUT)

    # Load and render template
    env: Environment = get_jinja_env()

    # Get the template and render it with data from JSONData
    template: Template = env.get_template(f"tpl_{template_name}.html")

    # Call the appropriate hook if it exists
    if template_name in DATA_PROVIDERS:
        data: list[tuple[str, dict[str, Any]]] = DATA_PROVIDERS[template_name](
            js_filter
        )
    else:
        raise ValueError(f"No hook defined for template: {template_name}")

    # Loop through each item in the list
    # and render a separate PDF for each
    for item in data:
        # Unpack the filename and item data from the current item tuple
        filename, item_data = item

        # Render the template for the current item
        rendered_tpl: str = template.render(item_data)

        # case match
        match output_format:
            case "pdf":
                (
                    HTML(string=rendered_tpl, base_url=str(templates_path)).write_pdf(
                        output_path / f"{filename}.pdf"
                    )
                )
            case "html":
                (
                    (output_path / f"{filename}.html").write_text(
                        rendered_tpl, encoding="utf-8"
                    )
                )
            case "txt":
                (
                    (output_path / f"{filename}.txt").write_text(
                        rendered_tpl, encoding="utf-8"
                    )
                )

    # Print success message
    print(f"finished rendering job for {template_name}")


def main() -> None:

    # Parse command-line arguments
    args = parse_args()

    try:
        # Generate the docs on the provided template and options
        generate_docs(args)

    except (JSONDataError, JinjaError, PathsError, TemplateNotFound, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
