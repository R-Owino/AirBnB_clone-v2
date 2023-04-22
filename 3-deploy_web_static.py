#!usr/bin/python3
"""
creates and distributes an archive to the web servers
"""

from fabric.api import task
from datetime import datetime
from os import path

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy


@task
def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    # create archive and get path
    archive_path = do_pack()
    if not archive_path:
        return False
    # deploy archive to web servers
    return do_deploy(archive_path)
