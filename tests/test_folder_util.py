import os

import pytest

from py_toolkit.utils.folder_util import make_dir_from_path, delete_dir


class TestFolderUtil:
    def test_make_dir_from_path_creates_directory(self, temp_dir):
        path = os.path.join(temp_dir, "a", "b", "c")
        make_dir_from_path(path)
        assert os.path.isdir(path)

    def test_make_dir_from_path_existing_directory(self, temp_dir):
        make_dir_from_path(temp_dir)
        assert os.path.isdir(temp_dir)

    def test_make_dir_from_path_raises_on_file(self, temp_dir):
        existing_file = os.path.join(temp_dir, "blocker")
        with open(existing_file, "w") as f:
            f.write("")
        with pytest.raises(OSError):
            make_dir_from_path(existing_file)

    def test_delete_dir_removes_directory(self, temp_dir):
        path = os.path.join(temp_dir, "todelete")
        os.makedirs(path)
        assert os.path.isdir(path)
        delete_dir(path)
        assert not os.path.exists(path)

    def test_delete_dir_nonexistent_does_not_raise(self):
        delete_dir("/tmp/_nonexistent_path_for_testing_")

    def test_delete_dir_with_contents(self, temp_dir):
        path = os.path.join(temp_dir, "parent")
        os.makedirs(os.path.join(path, "child"))
        with open(os.path.join(path, "file.txt"), "w") as f:
            f.write("content")
        delete_dir(path)
        assert not os.path.exists(path)

    def test_make_dir_from_path_nested_creates_all_parents(self, temp_dir):
        path = os.path.join(temp_dir, "x", "y", "z")
        make_dir_from_path(path)
        assert os.path.isdir(path)
        assert os.path.isdir(os.path.join(temp_dir, "x", "y"))
        assert os.path.isdir(os.path.join(temp_dir, "x"))
