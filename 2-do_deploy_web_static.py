#!/usr/bin/python3
"""This script deploys the static files to 2 remote servers"""
from fabric.api import *
from os.path import exists


env.hosts = ['52.23.178.146', '100.26.223.57']


def do_deploy(archive_path):
    """
    deploying an archive to a server
    """
    if not exists(archive_path):
        return False
    try:
        archive_fname = archive_path.split('/')[-1]
        archive_bname = archive_fname.split('.')[0]
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}'.format(archive_bname))
        run('tar -xzf /tmp/{0}.tgz -C /data/web_static/releases/{0}'.format(
                    archive_bname))
        run(('mv /data/web_static/releases/{0}/web_static/* ' +
            '/data/web_static/releases/{0}/').format(archive_bname))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            archive_bname))
        run('rm -f /tmp/{}'.format(archive_fname))
        run('rm -f /data/web_static/current')
        run(('ln -s /data/web_static/releases/{}' +
            ' /data/web_static/current').format(archive_bname))
        return True
    except Exception:
        return False
