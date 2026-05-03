from collections.abc import Generator

def pluck_nested(node, key: str) -> Generator[dict, None, None]:
    """Recursively yield all dicts found under a given key."""
    if isinstance(node, dict):
        yield from (i for i in (node.get(key) or []) if isinstance(i, dict))
        for k, v in node.items():
            if k != key:
                yield from pluck_nested(v, key)
    elif isinstance(node, list):
        for item in node:
            yield from pluck_nested(item, key)