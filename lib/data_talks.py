import datetime
import sys

from itertools import groupby
from typing import Any

import jq
import orjson
import pytz

from lib.data import JSONData
from lib.utils import normalize_filename


def get_data(options: str | None = None) -> list[tuple[str, dict[str, Any]]]:
    """Load and process speaker data from the program, applying optional jq filters.
    
    Args:
        options (str | None): An optional jq filter to apply to the speaker data.

    Returns:
        list[tuple[str, dict[str, Any]]]: A list of tuples containing speaker identifiers and 
            their corresponding data dictionaries, ready for rendering in templates.
    """

    # Load data from JSONData
    data = JSONData().get_data()
    
    # Initialize vars
    all_talks = []

    # Extract all talks and speakers from the program data
    for day in data.get("days", []):
        for event in day.get("events", []):
            if event.get("eventType") == "talk":
                all_talks.append({**event, "date": day.get("date"), "panel": event.get("title")})
            if event.get("eventType") == "panel":
                for talk in event.get("talks", []):
                    if talk.get("eventType") == "talk":
                        all_talks.append({**talk, "date": day.get("date"), "panel": event.get("title")})

    # Group talks by their status
    # sort order: tobeDefined, toBeConfirmed, final, unknown (use findIndex)
    status_order = ["toBeDefined", "toBeConfirmed", "final", "unknown"]
    data_sorted = sorted(all_talks, key=lambda x: status_order.index(x.get("status", "unknown")))
    processed_talks = {
        key: list(group) for key, group in groupby(data_sorted, key=lambda x: x.get("status", "unknown"))
    }

    # In this context, options is expected to be a jq filter 
    if options:
        talks = jq.compile(options).input(processed_talks).all()
    else:
        talks = processed_talks

    tz = pytz.timezone('Europe/Rome')
    current_time = datetime.datetime.now(tz)
    current_time = current_time.strftime("%d/%m/%Y")

    return [(normalize_filename("talks"), {
        "talks": talks,
        "updated_at": current_time
    })]

if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")