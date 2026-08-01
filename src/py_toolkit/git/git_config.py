"""Git config file helpers.

Modernised replacement for the original ``replace_username_in_git_config.py``
one-off script. The original used Python 2 ``print`` statements and hard-coded
paths; these functions are parameterised, typed and logged.
"""

import logging
import os

logger = logging.getLogger(__name__)


def find_git_configs(root: str) -> list[str]:
    """Recursively find all ``.git/config`` files under a directory.

    Args:
        root: Directory to walk.

    Returns:
        A list of paths to ``config`` files that live inside a ``.git`` folder.

    Example:
        >>> find_git_configs("/path/to/projects")  # doctest: +SKIP
        ['/path/to/projects/repo/.git/config']
    """
    configs: list[str] = []
    for current_dir, _dirs, files in os.walk(root):
        if os.path.basename(current_dir) == ".git" and "config" in files:
            configs.append(os.path.join(current_dir, "config"))
    logger.debug("Found %d git config files under %s", len(configs), root)
    return configs


def replace_in_git_config(path: str, old: str, new: str) -> bool:
    """Replace occurrences of ``old`` with ``new`` in a git config file.

    Args:
        path: Path to the git ``config`` file.
        old: Text to search for.
        new: Replacement text.

    Returns:
        ``True`` if the file was modified, ``False`` if ``old`` was not present.

    Raises:
        OSError: If the file cannot be read or written.

    Example:
        >>> replace_in_git_config(
        ...     "/repo/.git/config",
        ...     "git@github.com:rahils/",
        ...     "git@github.com:rahilsh/",
        ... )  # doctest: +SKIP
        True
    """
    with open(path) as f:
        content = f.read()

    if old not in content:
        logger.debug("No occurrences of %r in %s", old, path)
        return False

    new_content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(new_content)
    logger.info("Replaced %r with %r in %s", old, new, path)
    return True


def replace_username_in_configs(root: str, old: str, new: str) -> list[str]:
    """Replace a username in every git config file under a directory tree.

    Args:
        root: Directory to walk for ``.git/config`` files.
        old: Text to search for (e.g. an old remote URL prefix).
        new: Replacement text.

    Returns:
        A list of config file paths that were modified.

    Example:
        >>> replace_username_in_configs(
        ...     "/Users/me/code",
        ...     "git@github.com:rahils/",
        ...     "git@github.com:rahilsh/",
        ... )  # doctest: +SKIP
        ['/Users/me/code/repo/.git/config']
    """
    modified: list[str] = []
    for config in find_git_configs(root):
        if replace_in_git_config(config, old, new):
            modified.append(config)
    logger.info("Updated %d git config files under %s", len(modified), root)
    return modified
