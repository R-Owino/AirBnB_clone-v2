#!/usr/bin/python3
# Fabfile script to delete out-of-date archives

import os
from fabric.api import local, cd, lcd, run

env.hosts = ['54.236.33.113', '34.207.189.181']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives, etc.

    Returns:
        None
    """
    number = 1 if int(number) == 0 else int(number)

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))

    with cd("/data/web_static/releases"):
        run("ls -t | grep web_static | tail -n +{} | xargs rm -rf".format
            / (number + 1))
