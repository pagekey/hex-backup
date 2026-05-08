import requests
from hex import Params


def ui_input(prompt: str) -> str:
    url = "http://127.0.0.1:8000/api/graphs/request_input"
    payload = {"prompt": prompt}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    response_json = response.json()
    return response_json.get("response")


def run(params: Params) -> dict[str, str]:
    return {
        "src_folder": ui_input("Enter Google Drive folder to back up: "),
        "dst_folder": ui_input("Enter local folder path to store backup: "),
    }
