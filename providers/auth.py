import os

import requests
import secrets
import urllib.parse
import hashlib
import base64


def ui_input(prompt: str) -> str:
    url = "http://127.0.0.1:8000/api/graphs/request_input"
    payload = {"prompt": prompt}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    response_json = response.json()
    return response_json.get("response")


def generate_url(client_id, redirect_uri, scope):
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
        # PKCE
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(
        params
    )
    return url, code_verifier


def generate_token(code, redirect_uri, client_id, client_secret, code_verifier):
    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            # PKCE
            "code_verifier": code_verifier,
        },
    )

    if resp.status_code != 200:
        raise Exception(f"Token exchange failed: {resp.text}")

    data = resp.json()

    return {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in"),
        "token_type": data.get("token_type"),
    }


def run(inputs: dict[str, str]) -> dict[str, str]:
    redirect_uri = inputs["redirect_uri"]
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

    scope = "https://www.googleapis.com/auth/drive"
    # scope = "https://www.googleapis.com/auth/drive.readonly"  # uncomment to use readonly scope

    url, code_verifier = generate_url(client_id, redirect_uri, scope)

    print(f"Visit the following url: {url}")
    code = ui_input(f"Visit the following url: {url}. Paste the code: ")

    creds = generate_token(code, redirect_uri, client_id, client_secret, code_verifier)

    return {
        "access_token": creds.get("access_token"),
        "refresh_token": creds.get("refresh_token"),
        "expires_in": creds.get("expires_in"),
        "token_type": creds.get("token_type"),
    }
