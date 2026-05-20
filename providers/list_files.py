import requests
from hex import Params


def get_folder_id_by_name(name, access_token):
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


def run(params: Params) -> dict[str, str]:
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
        path = get_folder_id_by_name(path, access_token)

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
