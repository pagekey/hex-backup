import json
import os
from hex import Params


def run(params: Params) -> dict[str, str]:
    refresh_token = params.inputs.get("refresh_token")
    data_dir = params.workspace / "hexmod-backup"
    data_dir.mkdir(exist_ok=True, parents=True)
    secrets_path = data_dir / "secrets.json"
    secrets_path.write_text(
        json.dumps(
            {
                "client_id": os.getenv("GOOGLE_OAUTH_CLIENT_ID", ""),
                "client_secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", ""),
                "refresh_token": refresh_token,
            }
        )
    )
    return {
        "secrets_path": str(secrets_path.absolute()),
    }
