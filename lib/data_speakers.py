import sys

from typing import Any

import jq
import orjson

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
    all_speakers = []
    processed_speakers = []

    # Extract paper expiration dates if available,
    # to include in speaker data for potential use in templates.
    paperExpirationDates = data.get("paperExpirationDates", {})

    # Extract all talks and speakers from the program data
    for day in data.get("days", []):
        for event in day.get("events", []):
            if event.get("eventType") == "talk":
                all_talks.append({**event, "date": day.get("date"), "panel": event.get("title")})
            if event.get("eventType") == "panel":
                for talk in event.get("talks", []):
                    if talk.get("eventType") == "talk":
                        all_talks.append({**talk, "date": day.get("date"), "panel": event.get("title")})

    # Process each talk to extract speaker information,
    # ensuring that speakers with the name "Autore da definire" are excluded.
    for talk in all_talks:
        authors = talk.get("authors", []) or []
        authors = [{ **author, "is_first": i == 0 } for i, author in enumerate(authors)]
        for author in authors:
            if not author.get("name") == "Autore da definire":
                all_speakers.append({
                    "talk_date": talk.get("date"),
                    "talk_timeWindow": talk.get("timeWindow"),
                    "talk_title": talk.get("title"),
                    "talk_panel": talk.get("panel"),
                    "talk_duration": talk.get("duration"),
                    **{f"author_{k}": v for k, v in author.items()},
                    "author_collaborates_with": [ a for a in authors if a != author ],
                    **paperExpirationDates
                })

    if jq_filter:
        speakers = jq.compile(jq_filter).input(all_speakers).all()
    else:
        speakers = all_speakers

    # Process each speaker and prepare data for rendering
    for speaker in speakers:
        processed_speakers.append((
            normalize_filename(speaker['author_name']),
            speaker
        ))

    return processed_speakers

if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")
