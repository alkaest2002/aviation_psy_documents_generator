from __future__ import annotations

import argparse
from pathlib import Path

from jinja2 import Environment
from weasyprint import HTML

from lib.jinja import get_jinja_env
from lib.paths import get_paths
from lib.data import JSONData

def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--template", type=str, required=True, help="Template name")
    parser.add_argument("-x", "--html", action="store_true", help="Output HTML alongside PDF for debugging")
    args = parser.parse_args()
    
    _, _, output_path, _, templates_path = get_paths()

    # Get JSON data
    json_data: JSONData = JSONData()

    # Get Jinja2 environment
    env: Environment = get_jinja_env()

    # Render program.html with JSON data
    template = env.get_template(f"{args.template}/template.html")
    rendered_html: str = template.render(json_data.get_data())

    # Convert rendered HTML to PDF
    output_pdf: Path = output_path / f"{args.template}.pdf"
    HTML(string=rendered_html, base_url=str(templates_path)).write_pdf(str(output_pdf))

    # Output program.html also for debugging
    if args.html:
        doc_html: Path = output_path / f"{args.template}.html"
        doc_html.write_text(rendered_html, encoding="utf-8")

    print(f"Created {args.template}.pdf in output folder.")

if __name__ == "__main__":
    main()