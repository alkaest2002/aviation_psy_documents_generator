import sys

from typing import Any

import jq
import orjson

from lib.data import JSONData
from lib.utils import normalize_filename


def get_data(language: str = "it", jq_filter: str | None = None) -> list[tuple[str, dict[str, Any]]]:
    """Load and process speaker data from the program, applying optional jq filters.

    Args:
        language (str): The language to load data for.
        jq_filter (str | None): An optional jq filter to apply to the speaker data.

    Returns:
        list[tuple[str, dict[str, Any]]]: A list of tuples containing speaker identifiers and
            their corresponding data dictionaries, ready for rendering in templates.
    """

    # Load the program data
    data = JSONData().get_data()

    # Initialize vars
    all_talks = []
    processed_talks = []

    # Extract paper expiration dates if available,
    # to include in speaker data for potential use in templates.
    paperExpirationDates = data.get("paperExpirationDates", {})

    # Extract all talks and speakers from the program data
    for day in data.get("days", []):
        for event in day.get("events", []):
            if event.get("eventType") == "talk":
                all_talks.append({
                    **event,
                    "date": day.get("date"),
                    "panel": event.get("title"),
                    **paperExpirationDates
                })
            if event.get("eventType") == "panel":
                for talk in event.get("talks", []):
                    if talk.get("eventType") == "talk":
                        all_talks.append({
                            **talk,
                            "date": day.get("date"),
                            "panel": event.get("title"),
                            **paperExpirationDates
                        })

    if jq_filter:
        talks = jq.compile(jq_filter).input(all_talks).all()
    else:
        talks= all_talks

    # Prepare data for rendering
    for talk in talks:
        if talk["authors"][0]['name'] == "Autore da definire":
            continue
        processed_talks.append((
        f"relatori_invito_{normalize_filename(talk["authors"][0]['name'])}",
            talk
        ))

    return processed_talks

if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")
