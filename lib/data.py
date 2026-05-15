from typing import Any

import orjson

from lib.paths import PathEnum, get_paths


class JSONDataError(Exception):
    """Custom exception for data-related errors."""

    pass


class JSONData:
    """Class to handle loading and processing of JSON data."""

    def __init__(self) -> None:
        """Initialize JSONData instance."""
        self.data = None

    def _load_data(self) -> dict[str, Any]:
        """Load and return JSON data from the program.json file."""

        # Get the path to the JSON data file from the paths module
        (data_path,) = get_paths(PathEnum.DATA)

        # Load the JSON data from the file
        try:
            with data_path.open("r", encoding="utf-8") as f:
                return orjson.loads(f.read())

        # Handle specific exceptions
        except FileNotFoundError:
            raise JSONDataError(f"Data file not found: {data_path}")
        except orjson.JSONDecodeError as e:
            raise JSONDataError(f"Error decoding JSON data: {e}")

    def get_data(self) -> dict[str, Any]:
        """Return the loaded JSON data."""
        if self.data is None:
            self.data = self._load_data()
        return self.data
