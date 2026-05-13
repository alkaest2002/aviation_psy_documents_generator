import locale
import re

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

class JinjaError(Exception):
    """Custom exception for Jinja-related errors."""
    pass

def regex_replace(value, pattern, replacement):
    """Custom Jinja filter to perform regex replacement on a string."""
    if not isinstance(value, str):
        return value
    return re.sub(pattern, replacement, value)

def humanize_minutes(minutes: int) -> str:
    """Convert minutes to a human-readable format."""
    if minutes < 60:
        return f"{minutes} {'minuti' if minutes != 1 else 'minuto'}"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes == 0:
        return f"{hours} {'ore' if hours != 1 else 'ora'}"
    return f"{hours} {'ore' if hours != 1 else 'ora'} e {remaining_minutes} {'minuti' if remaining_minutes != 1 else 'minuto'}"

def humanize_date(date_str: str) -> str:
    """Convert a date string in the format DD/MM/YYYY to a human-readable Italian format e.g., 27 ottobre 2026."""
    original_locale = locale.getlocale(locale.LC_TIME)
    try:
        locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")
        date_str = date_str.replace("-", "/")
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%-d %B %Y")
    except ValueError:
        return date_str
    finally:
        locale.setlocale(locale.LC_TIME, original_locale)

def get_jinja_env() -> Environment:
    """Return a Jinja2 environment loaded from the templates folder."""

    # Determine the path to the templates directory relative to this file
    base_dir: Path = Path(__file__).resolve().parent

    # The templates directory is expected to be in the same directory as this file
    templates_path: Path = base_dir / "templates"

    # Check if the templates directory exists
    if not templates_path.exists():
        raise JinjaError(f"Templates directory not found: {templates_path}")

    # Create the Jinja2 environment with the FileSystemLoader pointing to the templates directory
    env: Environment = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Add custom filters to the Jinja2 environment
    env.filters["regex_replace"] = regex_replace
    env.filters["strip_cs"] = lambda value: value.strip(", ")
    env.filters["humanize_minutes"] = humanize_minutes
    env.filters["humanize_date"] = humanize_date

    return env