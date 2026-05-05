from typing import Any
from lib.data import JSONData


def get_data(options: str | None = None) -> dict[str, Any]:
    
    # Load data from JSONData
    data = JSONData().get_data()

    return "program", data

if __name__ == "__main__":
   print(get_data())