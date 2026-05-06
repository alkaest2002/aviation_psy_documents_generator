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
        for k, v in node.items():
            if k != key:
                yield from pluck_nested(v, key)
    elif isinstance(node, list):
        for item in node:
            yield from pluck_nested(item, key)