from enum import Enum
from pathlib import Path


class PathEnum(Enum):
    """Defines an enumeration of the physical paths used in the project."""

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
    # Resolve the base path to the project root
    base = Path(__file__).resolve().parent.parent

    # Define the paths relative to the base path
    paths = {
        PathEnum.BASE: base,
        PathEnum.LIB: base / "lib",
        PathEnum.TEMPLATES: base / "lib" / "templates",
        PathEnum.DATA: base / "../../sites/aviation-psy/src/",
        PathEnum.OUTPUT: base / "out",
    }

    # If specific paths are requested, validate and return them; otherwise, return all paths
    if requested:
        # Validate that all requested keys are PathEnum members
        invalid = [r for r in requested if not isinstance(r, PathEnum)]
        # Raise an error if any requested key is not a PathEnum member
        if invalid:
            raise PathsError(f"Invalid path keys: {', '.join(str(i) for i in invalid)}")
        # Return the selected paths
        selected = [paths[r] for r in requested]
    else:
        # Return all paths in enum order
        selected = list(paths.values())

    # Check for missing paths and raise an error if any are found
    missing = [
        f"{requested[i].value if requested else list(paths.keys())[i].value}: {path}"
        for i, path in enumerate(selected)
        if not path.exists()
    ]
    # Raise an error if any paths are missing
    if missing:
        raise PathsError("Missing required physical paths:\n" + "\n".join(missing))

    return selected
