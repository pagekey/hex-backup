import os
import shutil
import subprocess
from hex import Params


def run(params: Params) -> dict[str, str]:
    src_folder = params.inputs["src_folder"]
    dst_folder = params.inputs["dst_folder"]
    daily_time = params.inputs["daily_time"]
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    refresh_token = params.inputs["refresh_token"]
    hour, minute = daily_time.split(":")

    hex_path = shutil.which("hex") or "/usr/local/bin/hex"

    full_command = (
        f"{hex_path} run "
        "hexmod-backup.run_backup "
        f"-i src_folder={src_folder} "
        f"-i dst_folder={dst_folder} "
        f"-i client_id={client_id} "
        f"-i client_secret={client_secret} "
        f"-i refresh_token={refresh_token} "
        f"-w {str(params.workspace.resolve())}"
    ).strip()

    cron_entry = f"{minute} {hour} * * * {full_command} # HEX_JOB:backup"

    try:
        current_cron = subprocess.check_output(["crontab", "-l"], text=True)
    except subprocess.CalledProcessError:
        current_cron = ""

    lines = current_cron.strip().split("\n")
    new_lines = []
    updated = False

    for line in lines:
        if "# HEX_JOB:backup" in line:
            new_lines.append(cron_entry)
            updated = True
        elif line.strip():
            new_lines.append(line)

    if not updated:
        new_lines.append(cron_entry)

    # 6. Write back
    subprocess.run(
        ["crontab", "-"], input="\n".join(new_lines) + "\n", text=True, check=True
    )

    return {"report": f"Scheduled cron entry: {cron_entry}"}
