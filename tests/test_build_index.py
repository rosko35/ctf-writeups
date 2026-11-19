from __future__ import annotations

from datetime import date

import build_index
import new_writeup


def make(repo, platform, name, day, **kw):
    return new_writeup.create_writeup(repo, platform, name, today=date.fromisoformat(day), **kw)


def test_parse_front_matter():
    text = '---\ntitle: "A: B"\ntags: [x, "y z"]\nempty: []\n---\nbody'
    meta = build_index.parse_front_matter(text)
    assert meta == {"title": "A: B", "tags": ["x", "y z"], "empty": []}
    assert build_index.parse_front_matter("no front matter") == {}


def test_empty_state_is_honest(repo):
    assert build_index.main(["--root", str(repo)]) == 0
    en = (repo / "README.md").read_text(encoding="utf-8")
    tr = (repo / "README.tr.md").read_text(encoding="utf-8")
    assert "No writeups yet" in en
    assert "Henüz writeup yok" in tr
    assert "old" not in en
    assert en.endswith("footer\n")


def test_index_with_entries(repo):
    make(repo, "tryhackme", "Alpha", "2026-01-02", category="web")
    make(repo, "picoctf", "Beta | Pipe", "2026-03-04", category="crypto", difficulty="hard")
    assert build_index.main(["--root", str(repo)]) == 0
    en = (repo / "README.md").read_text(encoding="utf-8")
    assert "[Alpha](tryhackme/2026-01-02-alpha/README.md)" in en
    assert "Beta \\| Pipe" in en
    assert en.index("Beta") < en.index("Alpha")  # newest first
    assert "**Total:** 2" in en
    assert "tryhackme: 1, hackthebox: 0, picoctf: 1, other: 0" in en
    assert "crypto: 1, web: 1" in en
    tr = (repo / "README.tr.md").read_text(encoding="utf-8")
    assert "| Tarih | Platform |" in tr
    assert "Platforma göre" in tr


def test_check_detects_outdated_then_passes(repo):
    assert build_index.main(["--root", str(repo), "--check"]) == 1
    before = (repo / "README.md").read_text(encoding="utf-8")
    assert "old" in before  # --check must not write
    assert build_index.main(["--root", str(repo)]) == 0
    assert build_index.main(["--root", str(repo), "--check"]) == 0
    make(repo, "other", "New One", "2026-02-02")
    assert build_index.main(["--root", str(repo), "--check"]) == 1


def test_idempotent(repo):
    make(repo, "other", "One", "2026-02-02")
    build_index.main(["--root", str(repo)])
    first = (repo / "README.md").read_text(encoding="utf-8")
    build_index.main(["--root", str(repo)])
    assert (repo / "README.md").read_text(encoding="utf-8") == first


def test_missing_markers(repo, capsys):
    (repo / "README.md").write_text("# no markers\n", encoding="utf-8")
    assert build_index.main(["--root", str(repo)]) == 2
    assert "markers" in capsys.readouterr().err


def test_platform_readmes_are_not_entries(repo):
    (repo / "tryhackme" / "README.md").write_text("---\ntitle: x\n---\n", encoding="utf-8")
    assert build_index.collect(repo) == []
