#!/usr/bin/python3
# This script deploys the web static content
import os

from fabric.api import env, put, run, sudo

env.hosts = ['52.23.178.146', '100.26.223.57']
env.user = 'ubuntu'
env.key_filename = ['/home/yk/.ssh/id_rsa']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""

    # Check if the archive exists
    if not os.path.exists(archive_path):
        print(f"Error: Archive {archive_path} not found.")
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
    sudo(f'rm /tmp/{archive_filename}')

    # Delete the symbolic link /data/web_static/current
    run('rm -f /data/web_static/current')

    # Create a new symbolic link to the new version
    sudo(f'ln -s {remote_path} /data/web_static/current')

    print("New version deployed successfully.")
    return True


if __name__ == '__main__':
    do_deploy('versions/web_static_20231207111310.tgz')
