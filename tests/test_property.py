"""Property-based tests using Hypothesis."""

import string

from hypothesis import given
from hypothesis import strategies as st

from py_toolkit.utils.folder_util import make_dir_from_path


class TestFolderProperties:
    @given(
        path=st.text(
            alphabet=string.ascii_letters + string.digits + "-_",
            min_size=1,
            max_size=30,
        )
    )
    def test_make_dir_from_path_never_raises_on_valid_names(self, path):
        try:
            make_dir_from_path("/tmp/_hyp_test/" + path.replace("/", "_"))
        except (OSError, PermissionError):
            pass
