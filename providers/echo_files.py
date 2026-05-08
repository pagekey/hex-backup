from hex import Params


def run(params: Params) -> dict[str, str]:
    for f in params.inputs["files"]:
        print(f["name"] + ":")
        print(f["content"])
    return {}
