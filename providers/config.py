def run(inputs: dict[str, str]) -> dict[str, str]:
    return {
        "src_folder": input("Enter Google Drive folder to back up: "),
        "dst_folder": input("Enter local folder path to store backup: "),
    }
