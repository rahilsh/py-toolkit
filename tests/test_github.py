import pytest

from py_toolkit.exceptions import GitError
from py_toolkit.git.github import (
    GITHUB_API_URL,
    delete_repo,
    fork_repo,
    read_repo_names,
)


class TestForkRepo:
    def test_fork_repo_success(self, requests_mock):
        requests_mock.post(
            f"{GITHUB_API_URL}/repos/octocat/Hello-World/forks",
            json={"full_name": "you/Hello-World"},
            status_code=202,
        )
        result = fork_repo("octocat/Hello-World", "tok")
        assert result == {"full_name": "you/Hello-World"}

    def test_fork_repo_sends_auth_header(self, requests_mock):
        requests_mock.post(
            f"{GITHUB_API_URL}/repos/octocat/Hello-World/forks",
            json={},
            status_code=202,
        )
        fork_repo("octocat/Hello-World", "secret-token")
        assert requests_mock.last_request.headers["Authorization"] == "token secret-token"

    def test_fork_repo_error_status_raises(self, requests_mock):
        requests_mock.post(
            f"{GITHUB_API_URL}/repos/octocat/Hello-World/forks",
            json={"message": "Not Found"},
            status_code=404,
        )
        with pytest.raises(GitError):
            fork_repo("octocat/Hello-World", "tok")

    def test_fork_repo_network_error_raises(self, requests_mock):
        import requests

        requests_mock.post(
            f"{GITHUB_API_URL}/repos/octocat/Hello-World/forks",
            exc=requests.ConnectionError,
        )
        with pytest.raises(GitError):
            fork_repo("octocat/Hello-World", "tok")

    def test_fork_repo_custom_api_url(self, requests_mock):
        requests_mock.post(
            "https://ghe.example.com/repos/o/r/forks",
            json={"ok": True},
            status_code=202,
        )
        result = fork_repo("o/r", "tok", api_url="https://ghe.example.com")
        assert result == {"ok": True}


class TestDeleteRepo:
    def test_delete_repo_success(self, requests_mock):
        requests_mock.delete(f"{GITHUB_API_URL}/repos/you/old-repo", status_code=204)
        delete_repo("you/old-repo", "tok")
        assert requests_mock.called

    def test_delete_repo_sends_auth_header(self, requests_mock):
        requests_mock.delete(f"{GITHUB_API_URL}/repos/you/old-repo", status_code=204)
        delete_repo("you/old-repo", "secret-token")
        assert requests_mock.last_request.headers["Authorization"] == "token secret-token"

    def test_delete_repo_error_status_raises(self, requests_mock):
        requests_mock.delete(
            f"{GITHUB_API_URL}/repos/you/old-repo",
            json={"message": "Forbidden"},
            status_code=403,
        )
        with pytest.raises(GitError):
            delete_repo("you/old-repo", "tok")

    def test_delete_repo_network_error_raises(self, requests_mock):
        import requests

        requests_mock.delete(
            f"{GITHUB_API_URL}/repos/you/old-repo",
            exc=requests.ConnectionError,
        )
        with pytest.raises(GitError):
            delete_repo("you/old-repo", "tok")


class TestReadRepoNames:
    def test_read_repo_names(self, temp_dir):
        import os

        path = os.path.join(temp_dir, "repos.csv")
        with open(path, "w") as f:
            f.write("octocat/Hello-World\noctocat/Spoon-Knife extra columns\n")
        assert read_repo_names(path) == ["octocat/Hello-World", "octocat/Spoon-Knife"]

    def test_read_repo_names_skips_blank_lines(self, temp_dir):
        import os

        path = os.path.join(temp_dir, "repos.csv")
        with open(path, "w") as f:
            f.write("a/b\n\n   \nc/d\n")
        assert read_repo_names(path) == ["a/b", "c/d"]

    def test_read_repo_names_missing_file_raises(self):
        with pytest.raises(GitError):
            read_repo_names("/tmp/_nonexistent_repos_file_.csv")
