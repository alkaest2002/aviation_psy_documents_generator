import re
import sys

import jq
import orjson
from lib.data import JSONData
from typing import Any


def get_data(options: str | None = None) -> dict[str, Any]:

    # Load data from JSONData
    data = JSONData().get_data()
    
    # Initialize vars
    all_talks = []
    all_speakers = []
    processed_speakers = []

    # Extract all talks and speakers from the program data
    for day in data["days"]:
        for event in day["events"]:
            if event.get("eventType") == "talk":
                all_talks.append({**event, "date": day["date"]})
            if event.get("eventType") == "panel":
                for talk in event.get("talks", []):
                    all_talks.append({**talk, "date": day["date"]})

    # Process each talk to extract speaker information, 
    # ensuring that speakers with the name "Autore da definire" are excluded.
    for talk in all_talks:        
        authors = talk.get("authors", []) or []
        for author in authors:
            if not author.get("name") == "Autore da definire":
                all_speakers.append({
                    "date": talk["date"],
                    "timeWindow": talk["timeWindow"],
                    **author, 
                    "title": talk.get("title"), 
                    "co-authors": [ a for a in authors if a != author ]
                })

    # In this context, options is expected to be a jq filter 
    # that selects specific speakers from the list of all speakers.
    if options:
        speakers = jq.compile(options).input(all_speakers).all()
    else:
        speakers = all_speakers

    # make sure speakers is a list for consistent processing
    if not isinstance(speakers, list):
        speakers = [speakers]
    
    # Process each speaker and prepare data for rendering
    for speaker in speakers:
        processed_speakers.append([
            f"{re.sub(r'[^\w]', '_', speaker['name'].lower()).strip('_')}", 
            speaker
        ])
        
    return processed_speakers

if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")