from pathlib import Path
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape

class JinjaError(Exception):
    """Custom exception for Jinja-related errors."""
    pass

def regex_replace(value, pattern, replacement):
    return re.sub(pattern, replacement, value)

def get_jinja_env() -> Environment:
    """Return a Jinja2 environment loaded from the templates folder."""

    # Determine the path to the templates directory relative to this file
    base_dir: Path = Path(__file__).resolve().parent

    # The templates directory is expected to be in the same directory as this file
    templates_path: Path = base_dir / "templates"

    # Check if the templates directory exists
    if not templates_path.exists():
        print(f"Templates directory not found: {templates_path}")
        raise JinjaError(f"Templates directory not found: {templates_path}")

    # Create the Jinja2 environment with the FileSystemLoader pointing to the templates directory
    env: Environment = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Add custom filters to the Jinja2 environment
    env.filters["regex_replace"] = regex_replace
    env.filters["strip_cs"] = lambda value: value.strip(", ")

    return env