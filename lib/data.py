import orjson

from lib.paths import get_paths


class JSONDataError(Exception):
    """Custom exception for data-related errors."""
    pass

class JSONData:
    """Class to handle loading and processing of JSON data."""

    def __init__(self) -> None:
        """Initialize JSONData instance."""
        self.data = None

    def _load_data(self):
        """Load and return JSON data from the program.json file."""
        
        # Get the path to the JSON data file from the paths module
        _, data_path, _, _, _= get_paths()

        try:
            with data_path.open("r", encoding="utf-8") as f:
                return orjson.loads(f.read())
        except FileNotFoundError:
            raise JSONDataError(f"Data file not found: {data_path}")
        except orjson.JSONDecodeError as e:
            raise JSONDataError(f"Error decoding JSON data: {e}")

    def _get_speakers(self):
        """
        Return an ordered list of unique authors from nested dict/list JSON data.
        Uses set for uniqueness and map to build the uniqueness key.
        """
        author_set = set()
        fields = ("title", "name", "affiliation", "role")

        def walk(node):
            if isinstance(node, dict):
                authors = node.get("authors")
                if isinstance(authors, list):
                    for a in authors:
                        if isinstance(a, dict):
                            author_set.add(tuple(map(a.get, fields)))
                for v in node.values():
                    walk(v)

            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(self.data)

        # set[tuple] -> list[dict]
        result = [dict(zip(fields, t)) for t in author_set]

        # order by name
        result.sort(key=lambda a: (a.get("name") or "").lower())
        return result
    
    def get_data(self):
        """Return the loaded JSON data."""
        self.data = self._load_data()
        self.data["speakers"] = self._get_speakers()
        return self.data