import requests
from hex import Params
from datetime import datetime
from pathlib import Path
import os


def list(params: Params) -> dict[str, str]:
    access_token = params.inputs["access_token"]
    path = params.inputs["path"]
    # 1. Grab the new parameter (default to False if it's not provided)
    directories_only = params.inputs.get("directories_only", "False").lower() == "true"
    names_only = params.inputs.get("names_only", "False").lower() == "true"

    url = "https://www.googleapis.com/drive/v3/files"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params_api = {
        "pageSize": 50,
        "fields": "files(id, name, mimeType)",
    }

    q_parts = ["trashed = false"]

    # 2. Add the folder filter if directories_only is True
    if directories_only:
        q_parts.append("mimeType = 'application/vnd.google-apps.folder'")

    if path and not path.startswith("1"):
        path = _get_folder_id_by_name(path, access_token)

    if path:
        q_parts.append(f"'{path}' in parents")

    params_api["q"] = " and ".join(q_parts)

    try:
        response = requests.get(url, headers=headers, params=params_api)

        if response.status_code != 200:
            print(f"Drive API request failed ({response.status_code}): {response.text}")
            exit(1)

        files = response.json().get("files", [])

        if names_only:
            return {"files": [f.get("name") for f in files]}
        else:
            files_checked = [
                {
                    "mimeType": f.get("mimeType"),
                    "id": f.get("id"),
                    "name": f.get("name"),
                }
                for f in files
            ]
            return {"files": files_checked}

    except Exception as e:
        print(f"Error listing Drive files: {e}")
        exit(1)


def read(params: Params) -> dict[str, str]:
    access_token = params.inputs["access_token"]
    files = params.inputs["files"]
    files_content = [
        {
            "mimeType": f.get("mimeType"),
            "id": f.get("id"),
            "name": f.get("name"),
            "content": _get_file(f.get("id"), f.get("mimeType"), access_token),
        }
        for f in files
    ]
    return {
        "files_content": files_content,
    }


def save(params: Params) -> dict[str, str]:
    files = params.inputs["files_content"]
    dst_folder = params.inputs["dst_folder"]
    backup_folder_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S_GoogleDrive")
    dst_path = Path(dst_folder) / backup_folder_name
    dst_path.mkdir(parents=True, exist_ok=True)
    os.chmod(dst_path, 0o777)
    report = []
    for file in files:
        target_path = dst_path / file.get("name")
        target_path.write_text(file.get("content"))
        os.chmod(target_path, 0o777)
        report.append(f"Wrote {target_path.resolve()}\n")
    return {
        "report": report,
    }


def _get_folder_id_by_name(name, access_token):
    url = "https://www.googleapis.com/drive/v3/files"
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {
        "q": f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
        "fields": "files(id, name)",
        "pageSize": 1,
    }

    res = requests.get(url, headers=headers, params=params)
    files = res.json().get("files", [])

    if not files:
        return None

    return files[0]["id"]


def _get_file(file_id: str, mime_type: str, access_token: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        # Decide download method
        if "application/vnd.google-apps" in mime_type:
            # Google-native file → export
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export"
            params = {"mimeType": "text/plain"}
        else:
            # Regular file → direct download
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}"
            params = {"alt": "media"}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Drive API download failed: {response.text}")
            exit(1)

        return response.text

    except Exception as e:
        print(f"Error reading Drive file: {e}")
        exit(1)
