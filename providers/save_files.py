from datetime import datetime
from pathlib import Path
from hex import Params
import os


def run(params: Params) -> dict[str, str]:
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
        report.append(f"Wrote {target_path.resolve()}")
    return {
        "report": report,
    }
