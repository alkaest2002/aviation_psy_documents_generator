from typing import Any


def hook(data: dict[str, Any], options: str | None = None) -> dict[str, Any]:

    processed_invitations = []
    for invitee in data["invitations"]:
        processed_invitations.append([
            f"{invitee['name'].lower().replace(' ', '_')}", 
            { **invitee, "day1_time": data["days"][0]["timeWindow"], "day2_time": data["days"][1]["timeWindow"] }
        ])
        
    return processed_invitations