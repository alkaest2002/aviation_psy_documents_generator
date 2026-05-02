import json

from lib.paths import get_paths


class JSONDataError(Exception):
    """Custom exception for data-related errors."""
    pass

class JSONData:
    """Class to handle loading and processing of JSON data."""

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """Load and return JSON data from the program.json file."""
        _, data_path, _, _, _= get_paths()
        with data_path.open("r", encoding="utf-8") as f:
            return json.load(f)


    def get_speakers(self):
        """
        Return an ordered list of unique authors from nested dict/list JSON data.
        Uses set for uniqueness and map to build the uniqueness key.
        """
        """
        Return a list of unique authors ordered by name.
        Uses set for uniqueness and map for key extraction.
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