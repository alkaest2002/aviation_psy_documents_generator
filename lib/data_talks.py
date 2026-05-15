import datetime
import sys
from itertools import groupby
from typing import Any

import jq
import orjson
import pytz

from lib.data import JSONData
from lib.utils import normalize_filename


def get_data(jq_filter: str | None = None) -> list[tuple[str, dict[str, Any]]]:
    """Load and process speaker data from the program, applying optional jq filters.

    Args:
        jq_filter (str | None): An optional jq filter to apply to the speaker data.

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
                all_talks.append(
                    {**event, "date": day.get("date"), "panel": event.get("title")}
                )
            if event.get("eventType") == "panel":
                for talk in event.get("talks", []):
                    if talk.get("eventType") == "talk":
                        all_talks.append(
                            {
                                **talk,
                                "date": day.get("date"),
                                "panel": event.get("title"),
                            }
                        )

    # In this context, jq_filter is expected to be a jq filter
    if jq_filter:
        processed_talks = jq.compile(jq_filter).input(all_talks).all()
    else:
        processed_talks = all_talks

    # Group talks by their status
    status_order = ["toBeDefined", "toBeConfirmed", "final", "unknown"]
    data_sorted = sorted(
        processed_talks, key=lambda x: status_order.index(x.get("status", "unknown"))
    )
    # Group talks by their status
    talks_by_status = {
        key: list(group)
        for key, group in groupby(data_sorted, key=lambda x: x.get("status", "unknown"))
    }

    # Get the current time in the specified timezone and format it as a string
    tz = pytz.timezone("Europe/Rome")
    current_time = datetime.datetime.now(tz)
    current_time = current_time.strftime("%d/%m/%Y")

    # Return the processed talks and their grouping by status, along with the last updated time
    return [
        (
            normalize_filename("talks"),
            {
                "talks": all_talks,
                "talks_by_status": talks_by_status,
                "updated_at": current_time,
            },
        )
    ]


# This block allows the script to be run directly, outputting the processed speaker data as JSON to stdout.
if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")
