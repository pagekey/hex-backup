import shutil
import subprocess


def run(inputs: dict[str, str]) -> dict[str, str]:
    src_folder = inputs["src_folder"]
    dst_folder = inputs["dst_folder"]
    daily_time = inputs["daily_time"]
    token = inputs["token"]
    hour, minute = daily_time.split(":")

    hex_path = shutil.which("hex") or "/usr/local/bin/hex"

    full_command = f"{hex_path} run hex-backup.run_backup -i src_folder={src_folder} -i dst_folder={dst_folder} -i token={token}".strip()  # TODO: add -w for workspace.

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
