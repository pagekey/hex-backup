import json
from hex import Params


def run(params: Params) -> dict[str, str]:
    refresh_token = params.inputs.get("refresh_token")
    data_dir = params.workspace / "hexmod-backup"
    data_dir.mkdir(exist_ok=True, parents=True)
    secrets_path = data_dir / "secrets.json"
    secrets_path.write_text(json.dumps({"refresh_token": refresh_token}))
    return {
        "secrets_path": str(secrets_path.absolute()),
    }
