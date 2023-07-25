import os
import subprocess
import gzip
from django.conf import settings
from pathlib import Path
from datetime import datetime


def execute_mysqldump():
    database_config = settings.DATABASES['default']
    mysql_host = database_config['HOST']
    mysql_user = database_config['USER']
    mysql_password = database_config['PASSWORD']
    database_name = database_config['NAME']

    backup_file_name = datetime.now().strftime("%Y-%m-%dT%H%M") + ".sql.gz"

    base_directory = Path(__file__).resolve().parent.parent
    file_rel_path: str = os.path.join('backup', backup_file_name)
    file_abs_path: str = os.path.join(base_directory, file_rel_path)

    command = [
        "mysqldump",
        "-h",
        mysql_host,
        "-u",
        mysql_user,
        "-p" + mysql_password,
        "--single-transaction",
        "--quick",
        "--skip-lock-tables",
        database_name,
    ]

    try:
        # Execute mysqldump command and capture the output
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        backup_data = process.stdout.read()
        process.wait()

        with gzip.open(file_abs_path, "wb") as backup_file:
            backup_file.write(backup_data)
        print("Backup created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    execute_mysqldump()
