import sys

from typing import Any

import jq
import orjson

from lib.data import JSONData
from lib.utils import normalize_filename, pluck_nested

def _get_speakers(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract unique speaker information from the program data.

    Args:
        data (dict[str, Any]): The program data loaded from JSON.

    Returns:
        list[dict[str, Any]]: A sorted list of unique speaker information dictionaries.
    """

    # Define the fields to extract for each speaker
    fields = ("title", "name", "affiliation", "role")

    # Use a set comprehension to collect unique tuples of speaker
    # information from the nested "authors" key in the data
    unique = {
        tuple(map(a.get, fields))
            for a in pluck_nested(data, "authors")
    }

    # Convert the unique tuples back into dictionaries
    # and sort them by the "name" field (case-insensitive)
    return sorted(
        [dict(zip(fields, t)) for t in unique], key=lambda a: (a.get("name") or "").lower(),
    )

def get_data(jq_filter: str | None = None) -> list[tuple[str, dict[str, Any]]]:
    """Load and process program data, extracting speaker information and applying optional jq filters.

    Args:
        jq_filter (str | None): An optional jq filter to apply to the program data.

    Returns:
        list[tuple[str, dict[str, Any]]]: A list of tuples containing a single identifier ("program")
            and the corresponding data dictionary, ready for rendering in templates.
    """

    # Load data from JSONData
    data: dict[str, Any] = JSONData().get_data()

    # Extract speaker information and add it to the
    # data dictionary under the "speakers" key
    data["speakers"] = _get_speakers(data)

    if jq_filter:
        data = jq.compile(jq_filter).input(data).all()

    return [(normalize_filename("program"), data)]

if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")
