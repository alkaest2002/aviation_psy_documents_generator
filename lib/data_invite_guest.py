import sys
import orjson
import jq
from lib import data
from lib.data import JSONData
from typing import Any


def get_data(options: str | None = None) -> list[tuple[str, dict[str, Any]]]:

    # Load data from JSONData
    data = JSONData().get_data()

    # Initialize vars
    processed_invitations = []
    all_invitees = data["invitations"]

    # In this context, options is expected to be a jq filter 
    if options:
        invitees = jq.compile(options).input(all_invitees).all()
    else:
        invitees = all_invitees

    # make sure invitees is a list for consistent processing
    if not isinstance(invitees, list):
        invitees = [invitees]
    
    # Process each invitee and prepare data for rendering
    for invitee in invitees:
        processed_invitations.append((
            f"ospiti_{invitee['name'].lower().replace(' ', '_')}", 
            { **invitee, "day1_time": data["days"][0]["timeWindow"], "day2_time": data["days"][1]["timeWindow"] }
        ))
        
    return processed_invitations


if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")