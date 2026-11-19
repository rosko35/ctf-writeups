from __future__ import annotations

from datetime import date

import build_index
import new_writeup
import pytest

DAY = date(2026, 5, 17)


@pytest.mark.parametrize(
    ("name", "slug"),
    [
        ("Room Name", "room-name"),
        ("  Some_Room: v2!  ", "some-room-v2"),
        ("Şifre Çözücü Ağ", "sifre-cozucu-ag"),
        ("ışık ÖĞÜT", "isik-ogut"),
        ("!!!", ""),
    ],
)
def test_slugify(name, slug):
    assert new_writeup.slugify(name) == slug


def test_creates_folder_readme_and_img(repo):
    readme = new_writeup.create_writeup(
        repo, "tryhackme", "Room Name", difficulty="medium", category="web", today=DAY
    )
    folder = repo / "tryhackme" / "2026-05-17-room-name"
    assert readme == folder / "README.md"
    assert (folder / "img").is_dir()
    text = readme.read_text(encoding="utf-8")
    meta = build_index.parse_front_matter(text)
    assert meta["title"] == "Room Name"
    assert meta["platform"] == "tryhackme"
    assert meta["category"] == "web"
    assert meta["difficulty"] == "medium"
    assert meta["date"] == "2026-05-17"
    assert "# Room Name" in text
    assert "YYYY-MM-DD" not in text


def test_turkish_template(repo):
    readme = new_writeup.create_writeup(repo, "picoctf", "Örnek Oda", lang="tr", today=DAY)
    text = readme.read_text(encoding="utf-8")
    assert "## Özet" in text
    assert "# Örnek Oda" in text
    assert readme.parent.name == "2026-05-17-ornek-oda"


def test_refuses_to_overwrite(repo):
    new_writeup.create_writeup(repo, "other", "Same", today=DAY)
    readme = repo / "other" / "2026-05-17-same" / "README.md"
    readme.write_text("my notes", encoding="utf-8")
    with pytest.raises(FileExistsError):
        new_writeup.create_writeup(repo, "other", "Same", today=DAY)
    assert readme.read_text(encoding="utf-8") == "my notes"


def test_title_with_quotes_roundtrips(repo):
    readme = new_writeup.create_writeup(repo, "other", 'The "Quoted" Box', today=DAY)
    meta = build_index.parse_front_matter(readme.read_text(encoding="utf-8"))
    assert meta["title"] == 'The "Quoted" Box'


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"platform": "vulnhub", "name": "X"}, "platform"),
        ({"platform": "other", "name": "!!!"}, "name"),
        ({"platform": "other", "name": "X", "category": "Bad Cat"}, "category"),
    ],
)
def test_invalid_input(repo, kwargs, match):
    with pytest.raises(ValueError, match=match):
        new_writeup.create_writeup(repo, today=DAY, **kwargs)


def test_cli_success_and_failure(repo, capsys):
    argv = [
        "--root",
        str(repo),
        "--platform",
        "hackthebox",
        "--name",
        "Box",
        "--date",
        "2026-05-17",
    ]
    assert new_writeup.main(argv) == 0
    assert "Created" in capsys.readouterr().out
    assert new_writeup.main(argv) == 1
    assert "refusing to overwrite" in capsys.readouterr().err


def test_cli_bad_date(repo, capsys):
    argv = ["--root", str(repo), "--platform", "other", "--name", "Box", "--date", "nope"]
    assert new_writeup.main(argv) == 1
    assert "error" in capsys.readouterr().err
