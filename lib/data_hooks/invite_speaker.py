import jq
from typing import Any


def hook(data: dict[str, Any], options: str | None = None) -> dict[str, Any]:

    # Initialize vars
    processed_invitations = []
    all_invitees =  data["invitations"]

    # In this context, options is expected to be a jq filter 
    # that selects specific invitees from the list of all invitees.
    if options:
        invitees = jq.compile(options).input(all_invitees).all()
    else:
        invitees = all_invitees

    # make sure invitees is a list for consistent processing
    if not isinstance(invitees, list):
        invitees = [invitees]
    
    # Process each invitee and prepare data for rendering
    for invitee in invitees:
        processed_invitations.append([
            f"{invitee['name'].lower().replace(' ', '_')}", 
            { **invitee, "day1_time": data["days"][0]["timeWindow"], "day2_time": data["days"][1]["timeWindow"] }
        ])
        
    return processed_invitations