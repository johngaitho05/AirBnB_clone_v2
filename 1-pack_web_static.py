#!/usr/bin/python3
"""This script zips the content of web_static"""
from fabric.api import local
from datetime import datetime
import os

# Define global variables/constants
LOCAL_PATH = 'web_static'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    # Create the versions folder if it doesn't exist
    local('mkdir -p versions')

    # Get the current date and time
    now = datetime.utcnow()
    date_format = "%Y%m%d%H%M%S"
    date_str = now.strftime(date_format)

    # Define the archive path
    archive_name = f"web_static_{date_str}.tgz"
    archive_path = os.path.join("versions", archive_name)
    # Print the log
    print(f"Packing {LOCAL_PATH} to {archive_path}")

    # Create the archive
    local(f'tar -czvf {archive_path} {LOCAL_PATH}')

    # Print the size of the archive
    archive_size = os.path.getsize(archive_path)
    print(f"{LOCAL_PATH} packed: {archive_path} -> {archive_size} Bytes")

    print("\nDone.")
    return archive_path


if __name__ == "__main__":
    # Run the do_pack function when executing the script
    do_pack()
