from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jinja2 import Environment
from weasyprint import HTML

from lib.jinja import get_jinja_env, JinjaError
from lib.data import JSONData, JSONDataError
from lib.paths import get_paths, PathEnum, PathsError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Jinja2 template to PDF.")
    parser.add_argument("-t", "--template", type=str, required=True, help="Template name")
    parser.add_argument("-x", "--html", action="store_true", help="Output HTML alongside PDF for debugging")
    return parser.parse_args()


def render(template_name: str, output_html: bool) -> None:
    paths: dict[PathEnum, Path] = get_paths(PathEnum.TEMPLATES, PathEnum.OUTPUT)
    templates_path: Path = paths[PathEnum.TEMPLATES]
    output_path: Path = paths[PathEnum.OUTPUT]

    env: Environment = get_jinja_env()
    template = env.get_template(f"{template_name}/template.html")
    rendered_html: str = template.render(JSONData().get_data())

    output_path.mkdir(parents=True, exist_ok=True)

    HTML(string=rendered_html, base_url=str(templates_path)).write_pdf(
        str(output_path / f"{template_name}.pdf")
    )

    if output_html:
        (output_path / f"{template_name}.html").write_text(rendered_html, encoding="utf-8")

    print(f"Created {template_name}.pdf in {output_path}")


def main() -> None:
    args = parse_args()

    try:
        render(args.template, args.html)
    except (JSONDataError, JinjaError, PathsError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()