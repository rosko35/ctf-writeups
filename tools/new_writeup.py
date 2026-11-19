#!/usr/bin/env python3
"""Create a dated writeup folder from the template.

Usage:
    python tools/new_writeup.py --platform tryhackme --name "Room Name" \
        [--lang tr|en] [--difficulty easy] [--category web]

Creates ``<platform>/YYYY-MM-DD-room-name/README.md`` (front matter filled in)
and an empty ``img/`` folder. It never overwrites an existing folder.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

PLATFORMS = ("tryhackme", "hackthebox", "picoctf", "other")
DIFFICULTIES = ("easy", "medium", "hard", "insane")
LANGS = ("en", "tr")
REPO_ROOT = Path(__file__).resolve().parent.parent

_TR_MAP = str.maketrans(
    {
        "ı": "i",
        "İ": "I",
        "ş": "s",
        "Ş": "S",
        "ğ": "g",
        "Ğ": "G",
        "ü": "u",
        "Ü": "U",
        "ö": "o",
        "Ö": "O",
        "ç": "c",
        "Ç": "C",
    }
)
_FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_CATEGORY_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def slugify(name: str) -> str:
    """Turn a room name into a lowercase ASCII, hyphen-separated slug."""
    text = name.translate(_TR_MAP)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()


def template_path(root: Path, lang: str) -> Path:
    filename = "writeup.md" if lang == "en" else "writeup.tr.md"
    return root / "templates" / filename


def fill_template(text: str, values: dict[str, str], title: str) -> str:
    """Replace the front matter values and the first H1 heading in the template."""
    text = text.replace("\r\n", "\n")
    match = _FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError("template has no front matter block")
    front = match.group(1)
    for key, value in values.items():
        front, count = re.subn(
            rf"^{re.escape(key)}:.*$",
            lambda _m, k=key, v=value: f"{k}: {v}",
            front,
            count=1,
            flags=re.MULTILINE,
        )
        if count == 0:
            raise ValueError(f"template front matter has no '{key}:' line")
    body = text[match.end() :]
    body = re.sub(r"^# .*$", lambda _m: f"# {title}", body, count=1, flags=re.MULTILINE)
    return f"---\n{front}\n---\n{body}"


def create_writeup(
    root: Path,
    platform: str,
    name: str,
    lang: str = "en",
    difficulty: str = "easy",
    category: str = "misc",
    today: date | None = None,
) -> Path:
    """Create the writeup folder and return the path of its README.md.

    Raises FileExistsError if the folder already exists, ValueError for bad input.
    """
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform: {platform}")
    slug = slugify(name)
    if not slug:
        raise ValueError("name must contain at least one letter or digit")
    category = category.strip().lower()
    if not _CATEGORY_RE.match(category):
        raise ValueError("category must be lowercase letters, digits and hyphens")

    today = today or date.today()
    folder = root / platform / f"{today.isoformat()}-{slug}"
    if folder.exists():
        raise FileExistsError(f"refusing to overwrite existing folder: {folder}")

    tpl = template_path(root, lang)
    if not tpl.is_file():
        raise FileNotFoundError(f"template not found: {tpl}")

    safe_title = name.strip().replace("\\", "\\\\").replace('"', '\\"')
    content = fill_template(
        tpl.read_text(encoding="utf-8"),
        {
            "title": f'"{safe_title}"',
            "platform": platform,
            "category": category,
            "difficulty": difficulty,
            "date": today.isoformat(),
        },
        title=name.strip(),
    )

    (folder / "img").mkdir(parents=True)
    (folder / "img" / ".gitkeep").write_text("", encoding="utf-8")
    readme = folder / "README.md"
    with readme.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    return readme


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a new writeup folder from the template.")
    parser.add_argument("--platform", required=True, choices=PLATFORMS)
    parser.add_argument("--name", required=True, help='room / challenge name, e.g. "Room Name"')
    parser.add_argument("--lang", choices=LANGS, default="en", help="template language")
    parser.add_argument("--difficulty", choices=DIFFICULTIES, default="easy")
    parser.add_argument("--category", default="misc", help="e.g. web, crypto, forensics, pwn")
    parser.add_argument("--date", help="override the date (YYYY-MM-DD); default is today")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        today = date.fromisoformat(args.date) if args.date else None
        readme = create_writeup(
            args.root,
            args.platform,
            args.name,
            lang=args.lang,
            difficulty=args.difficulty,
            category=args.category,
            today=today,
        )
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Created {readme}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
