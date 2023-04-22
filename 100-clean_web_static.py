#!/usr/bin/python3
# Fabfile script to delete out-of-date archives

import os
from fabric.api import local, cd, lcd, run

env.hosts = ['54.236.33.113', '34.207.189.181']
env.user = 'ubuntu'


def do_clean(number=0):

    number = 1 if int(number) == 0 else int(number)

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))

    with cd("/data/web_static/releases"):
        run("ls -t | grep web_static | tail -n +{} | xargs rm -rf".format
            / (number + 1))
