from hex import Params


def run(params: Params) -> dict[str, str]:
    full_client_id = params.inputs.get("client_id", "")
    full_client_secret = params.inputs.get("client_secret", "")
    return {
        "client_id": f"{full_client_id[0:2]}...{full_client_id[-2:]}",
        "client_secret": f"{full_client_secret[0:2]}...{full_client_secret[-2:]}",
    }
