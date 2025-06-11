import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from tier1.hw04.folder_list import print_tree


def test_simple_tree_output() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "file1.txt").write_text("hello")
        (root / "dir1").mkdir()
        (root / "dir1" / "file2.txt").write_text("world")
        (root / "dir2").mkdir()

        buf = StringIO()
        with redirect_stdout(buf):
            print_tree(root)

        output = buf.getvalue()

        assert "file1.txt" in output
        assert "dir1/" in output
        assert "file2.txt" in output
        assert "dir2/" in output

        # Color codes check (optional, not asserting exact ANSI)
        assert "\x1b[" in output  # Means colorama worked
