from pathlib import Path
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape

def regex_replace(value, pattern, replacement):
    return re.sub(pattern, replacement, value)

def get_jinja_env() -> Environment:
    """Return a Jinja2 environment loaded from the templates folder."""

    base_dir: Path = Path(__file__).resolve().parent
    templates_path: Path = base_dir / "templates"

    if not templates_path.exists():
        print(f"Templates directory not found: {templates_path}")
        raise FileNotFoundError(f"Templates directory not found: {templates_path}")

    env: Environment = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(["html", "xml"]),
    )

    env.filters["regex_replace"] = regex_replace
    env.filters["strip_cs"] = lambda value: value.strip(", ")

    return env