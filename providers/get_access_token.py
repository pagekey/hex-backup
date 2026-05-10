import os

import requests

from hex import Params


def run(params: Params) -> dict[str, str]:
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    refresh_token = params.inputs["refresh_token"]

    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )
    response.raise_for_status()

    response_json = response.json()
    access_token = response_json.get("access_token")

    if not access_token:
        raise Exception(f"No access token returned: {response_json}")

    return {
        "access_token": access_token,
    }
