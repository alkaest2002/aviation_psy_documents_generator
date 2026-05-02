from enum import Enum
from pathlib import Path


class PathEnum(Enum):
    BASE = "base"
    LIB = "lib"
    TEMPLATES = "templates"
    DATA = "data"
    OUTPUT = "output"


class PathsError(Exception):
    """Raised when a required path is missing or an invalid path is requested."""


def get_paths(*requested: PathEnum) -> dict[PathEnum, Path]:
    """Return resolved paths as a dictionary keyed by PathEnum.
    
    If no arguments are provided, all paths are returned.

    Raises:
        PathsError: If any requested key is not a PathEnum or any path does not exist.
    """
    base = Path(__file__).resolve().parent.parent
    lib = base / "lib"

    all_paths = {
        PathEnum.BASE: base,
        PathEnum.LIB: lib,
        PathEnum.TEMPLATES: lib / "templates",
        PathEnum.DATA: base / "../../sites/aviation-psy/src/program.json",
        PathEnum.OUTPUT: base / "out",
    }

    invalid = [r for r in requested if not isinstance(r, PathEnum)]
    if invalid:
        raise PathsError(f"Invalid path keys: {', '.join(str(i) for i in invalid)}")

    paths = {k: v for k, v in all_paths.items() if k in requested} if requested else all_paths

    missing = [f"{k.value}: {v}" for k, v in paths.items() if not v.exists()]
    if missing:
        raise PathsError("Missing required paths:\n" + "\n".join(missing))

    return paths