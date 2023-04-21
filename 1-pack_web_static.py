#!/usr/bin/python3
"""
Generates a .tgz archive from the contents of the web_static folder
Usage: ./1-pack_web_static.py do_pack
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses the files to an archive for deployment

    Returns:
        path of the archive if correctly generated otherwise None
    """

    # Creates a folder if it doesn't exist
    local("mkdir -p versions")

    # Format the name of the compressed file using datetime
    curr_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    # Archived file format
    archived_file = "versions/web_static_{}.tgz".format(curr_time)

    # Defines the bash command to compress the contents
    create = local("tar -cvzf {} web_static/".format(archived_file))

    if create.failed:
        return None
    return archived_file
