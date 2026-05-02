def pluck_nested(node, key: str) -> list[dict]:
    """Recursively collect all dicts found under a given key."""
    if isinstance(node, dict):
        items = [i for i in (node.get(key) or []) if isinstance(i, dict)]
        nested = [i for v in node.values() for i in pluck_nested(v, key)]
        return items + nested
    elif isinstance(node, list):
        return [i for item in node for i in pluck_nested(item, key)]
    return []