#!/usr/bin/python3
"""This script deploys the static files to 2 remote servers"""
import os

from fabric.api import env, put, run, sudo

env.hosts = ['52.23.178.146', '100.26.223.57']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""

    # Check if the archive exists
    if not os.path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")

    # Extract the archive to /data/web_static/releases/<archive_filename_without_extension>
    archive_filename = os.path.basename(archive_path)
    archive_filename_without_extension = os.path.splitext(archive_filename)[0]
    remote_path = f"/data/web_static/releases/{archive_filename_without_extension}"

    run(f'mkdir -p {remote_path}')
    run(f'tar -xzf /tmp/{archive_filename} -C {remote_path} --strip-components=1')

    # Delete the archive from the web server
    run(f'rm /tmp/{archive_filename}')

    # Delete the symbolic link /data/web_static/current
    run('rm -f /data/web_static/current')

    # Create a new symbolic link to the new version
    sudo(f'ln -s {remote_path} /data/web_static/current')

    print("New version deployed successfully.")
    return True
