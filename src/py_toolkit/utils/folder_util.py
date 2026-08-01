import logging
import os
import shutil

logger = logging.getLogger(__name__)


def make_dir_from_path(path: str) -> None:
    """Create a directory and all parent directories.

    Succeeds silently if the directory already exists.

    Args:
        path: Directory path to create.

    Raises:
        OSError: If the path exists as a file or cannot be created.

    Example:
        >>> make_dir_from_path("/tmp/a/b/c")
    """
    try:
        os.makedirs(path)
        logger.debug("Created directory: %s", path)
    except OSError:
        if not os.path.isdir(path):
            logger.error("Failed to create directory: %s", path)
            raise


def delete_dir(path: str) -> None:
    """Recursively delete a directory tree.

    Does nothing if the path does not exist.

    Args:
        path: Directory path to delete.

    Example:
        >>> delete_dir("/tmp/old_folder")
    """
    shutil.rmtree(path, ignore_errors=True)
    logger.debug("Deleted directory: %s", path)
