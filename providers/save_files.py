from datetime import datetime
from pathlib import Path


def run(inputs: dict[str, str]) -> dict[str, str]:
    files = inputs["files_content"]
    dst_folder = inputs["dst_folder"]
    backup_folder_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S_GoogleDrive")
    dst_path = Path(dst_folder) / backup_folder_name
    dst_path.mkdir(parents=True, exist_ok=True)
    report = []
    for file in files:
        target_path = dst_path / file.get("name")
        target_path.write_text(file.get("content"))
        report.append(f"Wrote {target_path}")
    return {
        "report": report,
    }
