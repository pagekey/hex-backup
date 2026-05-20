from hex import Params


def run(params: Params) -> dict[str, str]:
    full_refresh_token = params.inputs.get("refresh_token", "")
    return {
        "refresh_token": f"{full_refresh_token[0:3]}**********{full_refresh_token[-3:]}",
    }
