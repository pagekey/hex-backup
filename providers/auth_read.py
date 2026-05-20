import json
from hex import Params


def run(params: Params) -> dict[str, str]:
    data_dir = params.workspace / "hexmod-backup"
    data_dir.mkdir(exist_ok=True, parents=True)
    secrets_path = data_dir / "secrets.json"
    data = json.loads(secrets_path.read_text())
    return {
        "client_id": data.get("client_id"),
        "client_secret": data.get("client_secret"),
        "refresh_token": data.get("refresh_token"),
    }
