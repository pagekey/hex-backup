def run(inputs: dict[str, str]) -> dict[str, str]:
    for f in inputs["files"]:
        print(f["name"] + ":")
        print(f["content"])
    return {}
