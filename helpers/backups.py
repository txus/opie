import os
import sys
import time
import opie
import click
import tarfile
import usb.core
import usb.util
from helpers import u
from datetime import datetime

BACKUPS_DIR = os.path.join(u.HOME, "backups")
ARCHIVE_FORMAT = "opie-backup-%Y-%m-%d-%H%M%S.tar.xz"

def assert_environment():
    os.makedirs(BACKUPS_DIR, exist_ok=True)

def generate_archive(mount, save_dir):
    name = os.path.join(save_dir, datetime.now().strftime(ARCHIVE_FORMAT))
    print("writing backup as %s" % (name))
    with tarfile.open(name, "x:xz") as tar:
        with click.progressbar(u.get_visible_children(mount)) as children:
            for child in children:
                tar.add(os.path.join(mount, child), child, filter=lambda x: None if x.name[0] == '.' else x)
    print("backup created.")

def restore_archive(file, mount):
    with tarfile.open(file, "r:xz") as tar:
        tar.extractall(path=mount)
    print("successfully restored from archive.")

