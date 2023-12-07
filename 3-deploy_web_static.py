#!/usr/bin/python3
"""This script deploys the static files to 2 remote servers"""

import os
from datetime import datetime

from fabric.api import env, put, run
from fabric.api import local

# Define global variables/constants
LOCAL_PATH = 'web_static'
# servers
env.hosts = ['52.23.178.146', '100.26.223.57']
archive_path = None


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


def do_deploy():
    """Distributes an archive to the web servers."""
    global archive_path
    try:
        # Check if the archive exists
        if not os.path.exists(archive_path):
            return False

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/
        # releases/<archive_filename_without_extension>
        archive_filename = os.path.basename(archive_path)
        archive_filename_without_extension = (
            os.path.splitext(archive_filename))[0]
        remote_path = (f"/data/web_static/releases/"
                       f"{archive_filename_without_extension}/")

        run(f'mkdir -p {remote_path}')
        run(f'tar -xzf /tmp/{archive_filename} -C {remote_path}')

        # Delete the archive from the web server
        run(f'rm /tmp/{archive_filename}')
        run(f'mv {remote_path}web_static/* {remote_path}')
        run(f'rm -rf {remote_path}web_static')

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run(f'ln -s {remote_path} /data/web_static/current')

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Creates and deploys a new static collection"""
    global archive_path  # Use the global archive_path variable

    # Call do_pack only if archive_path is not set
    if archive_path is None:
        archive_path = do_pack()
    return do_deploy()


if __name__ == '__main__':
    deploy()
