#!/usr/bin/python3
"""
Distributes an archive to the web servers
Usage: ./2_do_deploy_web_static.py do_deploy
"""

from fabric.api import *
from os import path

env.hosts = ['54.236.33.113', '34.207.189.181']
env.user = 'ubuntu'


@task(alias="deploy")
def do_deploy(archive_path):
    """
    Distributes the archived file to the web servers

    Attr:
        archive_path (str): The path to the archived file

    Returns:
        True if all operations have been done correctly
        otherwise returns False
    """
    if not path.exists(archive_path):
        return False
    try:
        # split the archive path and extract base location
        arc = archive_path.split("/")
        # base location
        base_loc = arc[1].strip('.tgz')
        # upload archive to remote server
        put(archive_path, '/tmp/')
        # extract, move and create symlinks to the web_static files
        sudo('mkdir -p /data/web_static/releases/{}'.format(base_loc))
        main_loc = "/data/web_static/releases/{}".format(base_loc)
        sudo('tar -xzf /tmp/{} -C {}/'.format(arc[1], main_loc))
        sudo('rm /tmp/{}'.format(arc[1]))
        sudo('mv {}/web_static/* {}/'.format(main_loc, main_loc))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ "/data/web_static/current"'.format(main_loc))

        return True
    except Exception:
        return False
