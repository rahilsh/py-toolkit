import os
import shutil


def make_dir_from_path(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def delete_dir(path):
    shutil.rmtree(path, ignore_errors=True)
