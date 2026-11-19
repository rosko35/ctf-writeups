from __future__ import annotations

import shutil
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A throw-away repo layout with the real templates and marker-only READMEs."""
    shutil.copytree(REPO_ROOT / "templates", tmp_path / "templates")
    for platform in ("tryhackme", "hackthebox", "picoctf", "other"):
        (tmp_path / platform).mkdir()
    marked = "# Title\n\n<!-- INDEX:START -->\nold\n<!-- INDEX:END -->\n\nfooter\n"
    (tmp_path / "README.md").write_text(marked, encoding="utf-8")
    (tmp_path / "README.tr.md").write_text(marked, encoding="utf-8")
    return tmp_path
