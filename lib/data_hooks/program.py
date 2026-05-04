from typing import Any


def hook(data: dict[str, Any], options: str | None = None) -> dict[str, Any]:
    return "program", data