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


def get_paths(*requested: PathEnum) -> list[Path]:
    """Return resolved paths as a list of Path values.

    Args:
        *requested (PathEnum): Variable length argument list of PathEnum keys to return.
            If empty, all paths will be returned in enum order.

    Raises:
        PathsError: If any requested key is not a PathEnum or any path does not exist.
    """
    base = Path(__file__).resolve().parent.parent

    paths = {
        PathEnum.BASE: base,
        PathEnum.LIB: base / "lib",
        PathEnum.TEMPLATES: base / "lib" / "templates",
        PathEnum.DATA: base / "../../sites/aviation-psy/src/program.json",
        PathEnum.OUTPUT: base / "out",
    }

    if requested:
        invalid = [r for r in requested if not isinstance(r, PathEnum)]
        if invalid:
            raise PathsError(f"Invalid path keys: {', '.join(str(i) for i in invalid)}")
        selected = [paths[r] for r in requested]
    else:
        selected = list(paths.values())

    missing = [f"{requested[i].value if requested else list(paths.keys())[i].value}: {path}"
               for i, path in enumerate(selected)
               if not path.exists()]
    if missing:
        raise PathsError("Missing required physical paths:\n" + "\n".join(missing))

    return selected