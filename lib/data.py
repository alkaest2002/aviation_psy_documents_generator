import orjson

from lib.paths import PathEnum, get_paths
from lib.utils import pluck_nested


class JSONDataError(Exception):
    """Custom exception for data-related errors."""
    pass

class JSONData:
    """Class to handle loading and processing of JSON data."""

    SPEAKER_FIELDS = ("title", "name", "affiliation", "role")
    
    def __init__(self) -> None:
        """Initialize JSONData instance."""
        self.data = None

    def _load_data(self):
        """Load and return JSON data from the program.json file."""
        
        # Get the path to the JSON data file from the paths module
        data_path = get_paths(PathEnum.DATA)[PathEnum.DATA]

        try:
            with data_path.open("r", encoding="utf-8") as f:
                return orjson.loads(f.read())
        except FileNotFoundError:
            raise JSONDataError(f"Data file not found: {data_path}")
        except orjson.JSONDecodeError as e:
            raise JSONDataError(f"Error decoding JSON data: {e}")

    def _get_speakers(self) -> list[dict]:
        # Define the fields to extract for each speaker
        fields = ("title", "name", "affiliation", "role")

        # Use a set comprehension to collect unique tuples of speaker 
        # information from the nested "authors" key in the data
        unique = {
            tuple(map(a.get, fields))
                for a in pluck_nested(self.data, "authors")
        }

        # Convert the unique tuples back into dictionaries 
        # and sort them by the "name" field (case-insensitive)
        return sorted(
            [dict(zip(fields, t)) for t in unique], key=lambda a: (a.get("name") or "").lower(),
        )
        
    def get_data(self):
        """Return the loaded JSON data."""
        self.data = self._load_data()
        self.data["speakers"] = self._get_speakers()
        return self.data