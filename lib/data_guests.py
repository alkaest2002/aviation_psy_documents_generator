import sys

from typing import Any

import jq
import orjson

from lib import data
from lib.data import JSONData
from lib.utils import normalize_filename


def get_data(jq_filter: str | None = None) -> list[tuple[str, dict[str, Any]]]:
    """Load and process invitation data for speakers, applying optional jq filters.

    Args:
        jq_filter (str | None): An optional jq filter to apply to the invitee data.

    Returns:
        list[tuple[str, dict[str, Any]]]: A list of tuples containing invitee identifiers and
            their corresponding data dictionaries, ready for rendering in templates.
    """

    # Load data from JSONData
    data = JSONData().get_data()

    # Initialize vars
    processed_invitations = []
    all_invitees = data["invitations"]

    if jq_filter:
        invitees = jq.compile(jq_filter).input(all_invitees).all()
    else:
        invitees = all_invitees

    # Process each invitee and prepare data for rendering
    for invitee in invitees:
        processed_invitations.append((
            f"ospiti_{normalize_filename(invitee['name'])}",
            { **invitee, "day1_time": data["days"][0]["timeWindow"], "day2_time": data["days"][1]["timeWindow"] }
        ))

    return processed_invitations


if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")
