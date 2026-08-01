import os

from py_toolkit.git.git_config import (
    find_git_configs,
    replace_in_git_config,
    replace_username_in_configs,
)


def _make_git_config(root: str, repo_name: str, content: str) -> str:
    git_dir = os.path.join(root, repo_name, ".git")
    os.makedirs(git_dir)
    config_path = os.path.join(git_dir, "config")
    with open(config_path, "w") as f:
        f.write(content)
    return config_path


class TestFindGitConfigs:
    def test_finds_git_config(self, temp_dir):
        config_path = _make_git_config(temp_dir, "repo", "content")
        assert find_git_configs(temp_dir) == [config_path]

    def test_finds_multiple_configs(self, temp_dir):
        c1 = _make_git_config(temp_dir, "repo1", "a")
        c2 = _make_git_config(temp_dir, "repo2", "b")
        assert set(find_git_configs(temp_dir)) == {c1, c2}

    def test_ignores_non_git_config_files(self, temp_dir):
        # A "config" file not inside a .git folder should be ignored.
        os.makedirs(os.path.join(temp_dir, "other"))
        with open(os.path.join(temp_dir, "other", "config"), "w") as f:
            f.write("x")
        assert find_git_configs(temp_dir) == []

    def test_empty_when_no_configs(self, temp_dir):
        assert find_git_configs(temp_dir) == []


class TestReplaceInGitConfig:
    def test_replaces_and_returns_true(self, temp_dir):
        path = _make_git_config(temp_dir, "repo", "git@github.com:rahils/x")
        modified = replace_in_git_config(path, "git@github.com:rahils/", "git@github.com:rahilsh/")
        assert modified is True
        with open(path) as f:
            assert f.read() == "git@github.com:rahilsh/x"

    def test_returns_false_when_not_present(self, temp_dir):
        path = _make_git_config(temp_dir, "repo", "no match here")
        assert replace_in_git_config(path, "old", "new") is False
        with open(path) as f:
            assert f.read() == "no match here"


class TestReplaceUsernameInConfigs:
    def test_replaces_across_tree(self, temp_dir):
        c1 = _make_git_config(temp_dir, "repo1", "git@github.com:rahils/one")
        c2 = _make_git_config(temp_dir, "repo2", "git@github.com:rahils/two")
        _make_git_config(temp_dir, "repo3", "unrelated remote")

        modified = replace_username_in_configs(
            temp_dir, "git@github.com:rahils/", "git@github.com:rahilsh/"
        )
        assert set(modified) == {c1, c2}
        with open(c1) as f:
            assert f.read() == "git@github.com:rahilsh/one"

    def test_returns_empty_when_no_matches(self, temp_dir):
        _make_git_config(temp_dir, "repo", "nothing to change")
        assert replace_username_in_configs(temp_dir, "old", "new") == []
