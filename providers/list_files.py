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

    url = "https://www.googleapis.com/drive/v3/files"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "pageSize": 50,
        "fields": "files(id, name, mimeType)",
    }

    q_parts = ["trashed = false"]

    if path and not path.startswith("1"):
        path = get_folder_id_by_name(path, access_token)

    if path:
        q_parts.append(f"'{path}' in parents")

    params["q"] = " and ".join(q_parts)

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Drive API request failed ({response.status_code}): {response.text}")
            exit(1)

        files = response.json().get("files", [])

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
