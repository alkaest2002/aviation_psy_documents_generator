import re
from collections.abc import Generator
from typing import Any


def pluck_nested(node: Any, key: str) -> Generator[dict[str, Any], None, None]:
    """Recursively yield all dicts found under a given key.

    Args:
        node (Any): The current node in the data structure to search.
        key (str): The key to look for in the dictionaries.

    Yields:
        dict[str, Any]: Each dictionary found under the specified key.
    """
    if isinstance(node, dict):
        yield from (i for i in (node.get(key) or []) if isinstance(i, dict))
        for k, value in node.items():
            if k != key:
                yield from pluck_nested(value, key)
    elif isinstance(node, list):
        for el in node:
            yield from pluck_nested(el, key)


def normalize_filename(name: str) -> str:
    """Normalize a string to be used as a filename by converting to lowercase and replacing spaces with underscores."""
    return re.sub(r"[^\w]", "_", name.lower()).strip("_")
