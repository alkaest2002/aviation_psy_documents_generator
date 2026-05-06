import sys
from typing import Any

import jq
import orjson
from lib.data import JSONData


def get_data(options: str | None = None) -> dict[str, Any]:
    
    # Load data from JSONData
    data = JSONData().get_data()

    # In this context, options is expected to be a jq filter 
    if options:
        data = jq.compile(options).input(data).all()

    return "program", data

if __name__ == "__main__":
    data = get_data()
    sys.stdout.buffer.write(orjson.dumps(data))
    sys.stdout.buffer.write(b"\n")