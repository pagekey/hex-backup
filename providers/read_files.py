import requests


def get_file(file_id: str, mime_type: str, token: str) -> str:
    headers = {
        "Authorization": f"Bearer {token}",
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


def run(inputs: dict[str, str]) -> dict[str, str]:
    token = inputs["token"]
    files = inputs["files"]
    files_content = [
        {
            "mimeType": f.get("mimeType"),
            "id": f.get("id"),
            "name": f.get("name"),
            "content": get_file(f.get("id"), f.get("mimeType"), token),
        }
        for f in files
    ]
    return {
        "files_content": files_content,
    }
