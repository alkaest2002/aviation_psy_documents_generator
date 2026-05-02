from __future__ import annotations

from pathlib import Path

from jinja2 import Environment
from weasyprint import HTML

from lib.jinja import get_jinja_env
from lib.paths import get_paths
from lib.data import JSONData

def main() -> None:
    
    _, _, output_path, _, templates_path = get_paths()

    # Get JSON data
    json_data: JSONData = JSONData()

    # Get Jinja2 environment
    env: Environment = get_jinja_env()

    # Render program.html with JSON data
    template = env.get_template("program/template.html")
    rendered_html: str = template.render({ **json_data.data, "speakers": json_data.get_speakers() })

    # Convert rendered HTML to PDF
    output_pdf: Path = output_path / "program.pdf"
    HTML(string=rendered_html, base_url=str(templates_path)).write_pdf(str(output_pdf))

    # Output program.html also for debugging
    doc_html: Path = output_path / "program.html"
    doc_html.write_text(rendered_html, encoding="utf-8")

    print("Created program.pdf and program.html in output folder.")

if __name__ == "__main__":
    main()