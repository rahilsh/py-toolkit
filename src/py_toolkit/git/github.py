"""GitHub repository helpers.

Modernised replacements for the original ``github_create_fork.py`` and
``github_delete_repo.py`` one-off scripts. Instead of prompting for a token on
stdin and reading a hard-coded CSV path, these functions accept parameters and
raise :class:`~py_toolkit.exceptions.GitError` on failure.
"""

import logging
from typing import Any

import requests

from py_toolkit.exceptions import GitError

logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"


def _auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def fork_repo(repo: str, token: str, api_url: str = GITHUB_API_URL) -> dict[str, Any]:
    """Fork a GitHub repository for the authenticated user.

    Args:
        repo: Repository in ``owner/name`` form (e.g. ``"octocat/Hello-World"``).
        token: GitHub personal access token.
        api_url: Base GitHub API URL. Override for GitHub Enterprise.

    Returns:
        The parsed JSON response describing the created fork.

    Raises:
        GitError: If the request fails or GitHub returns a non-2xx status.

    Example:
        >>> fork_repo("octocat/Hello-World", token)  # doctest: +SKIP
        {'id': 123, 'full_name': 'you/Hello-World', ...}
    """
    url = f"{api_url}/repos/{repo}/forks"
    try:
        response = requests.post(url, headers=_auth_headers(token), timeout=30)
        response.raise_for_status()
        logger.info("Forked repository %s", repo)
        return response.json()
    except requests.RequestException as e:
        msg = f"Failed to fork repository {repo}: {e}"
        logger.error(msg)
        raise GitError(msg) from e


def delete_repo(repo: str, token: str, api_url: str = GITHUB_API_URL) -> None:
    """Delete a GitHub repository.

    Warning:
        This is irreversible. The token must have the ``delete_repo`` scope.

    Args:
        repo: Repository in ``owner/name`` form (e.g. ``"you/old-repo"``).
        token: GitHub personal access token.
        api_url: Base GitHub API URL. Override for GitHub Enterprise.

    Raises:
        GitError: If the request fails or GitHub returns a non-2xx status.

    Example:
        >>> delete_repo("you/old-repo", token)  # doctest: +SKIP
    """
    url = f"{api_url}/repos/{repo}"
    try:
        response = requests.delete(url, headers=_auth_headers(token), timeout=30)
        response.raise_for_status()
        logger.info("Deleted repository %s", repo)
    except requests.RequestException as e:
        msg = f"Failed to delete repository {repo}: {e}"
        logger.error(msg)
        raise GitError(msg) from e


def read_repo_names(path: str) -> list[str]:
    """Read repository names from a whitespace/CSV-delimited file.

    Each non-empty line contributes its first whitespace-delimited token, which
    matches the format used by the original ``repos_to_fork.csv`` and
    ``repos_to_delete.csv`` files.

    Args:
        path: Path to the file listing repositories.

    Returns:
        A list of repository names (``owner/name``).

    Raises:
        GitError: If the file cannot be read.

    Example:
        >>> read_repo_names("repos_to_fork.csv")  # doctest: +SKIP
        ['octocat/Hello-World', 'octocat/Spoon-Knife']
    """
    try:
        with open(path) as f:
            repos = [line.split()[0] for line in f if line.strip()]
        logger.debug("Read %d repository names from %s", len(repos), path)
        return repos
    except OSError as e:
        msg = f"Failed to read repository list {path}: {e}"
        logger.error(msg)
        raise GitError(msg) from e
