import os
from hex import Params


def run(params: Params) -> dict[str, str]:
    key = params.inputs.get("key")
    return {"value": os.getenv(key, "")}
