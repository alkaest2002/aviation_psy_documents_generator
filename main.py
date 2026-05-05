from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jinja2 import Environment
from weasyprint import HTML

from lib.jinja import get_jinja_env, JinjaError
from lib.data import JSONDataError
from lib.paths import get_paths, PathEnum, PathsError
from lib.data_program import get_data as program_data
from lib.data_invite_gues import get_data as invite_guest_data
from lib.data_invite_speaker import get_data as invite_speaker_data


HOOKS : dict[str, callable] = {
    "program": program_data,
    "invite_guest": invite_guest_data,
    "invite_speaker": invite_speaker_data,
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Jinja2 template to PDF.")
    parser.add_argument("-t", "--template", type=str, required=True, help="Template name")
    parser.add_argument("-o", "--options", type=str, help="Additional options for future use")
    parser.add_argument("-x", "--html", action="store_true", help="Output HTML alongside PDF for debugging")
    return parser.parse_args()


def generate_docs(args: argparse.Namespace) -> None:

    # Extract arguments
    template_name: str = args.template
    options: str | None = args.options
    output_html: bool = args.html
    
    # Get paths
    paths: dict[PathEnum, Path] = get_paths(PathEnum.TEMPLATES, PathEnum.OUTPUT)
    templates_path: Path = paths[PathEnum.TEMPLATES]
    output_path: Path = paths[PathEnum.OUTPUT]

    # Load and render template
    env: Environment = get_jinja_env()

    # Get the template and render it with data from JSONData
    template = env.get_template(f"tpl_{template_name}.html")

    # Call the appropriate hook if it exists
    if template_name in HOOKS:
        data = HOOKS[template_name](options)
    else:
        raise ValueError(f"No hook defined for template: {template_name}")
    
    # Ensure data is a list for consistent processing
    if not isinstance(data, list):
        data = [data]

    # Loop through each item in the list and render a separate PDF for each
    for i, item in enumerate(data):

        [filename, item_data] = item

        # Render the template for the current item
        rendered_html: str = template.render(item_data)  

        # Write the rendered HTML to PDF using WeasyPrint#
        HTML(string=rendered_html, base_url=str(templates_path)).write_pdf(
            str(output_path / f"{filename}.pdf")
        )

        # Optionally write the rendered HTML to a file for debugging
        if output_html:
            (output_path / f"{filename}.html").write_text(rendered_html, encoding="utf-8")

    # Print success message
    print(f"finished rendering {template_name}.pdf")


def main() -> None:
    
    # Parse command-line arguments
    args = parse_args()

    try:
        # Generate the docs on the provided template and options
        generate_docs(args)
    
    except (JSONDataError, JinjaError, PathsError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()