#!/usr/bin/env python3
"""Regenerate the writeup index in README.md and README.tr.md.

Scans ``<platform>/*/README.md`` for front matter and rewrites the block between
``<!-- INDEX:START -->`` and ``<!-- INDEX:END -->``.

    python tools/build_index.py           # update the READMEs
    python tools/build_index.py --check   # exit 1 if they are out of date
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

PLATFORMS = ("tryhackme", "hackthebox", "picoctf", "other")
START = "<!-- INDEX:START -->"
END = "<!-- INDEX:END -->"
REPO_ROOT = Path(__file__).resolve().parent.parent

TARGETS = (("README.md", "en"), ("README.tr.md", "tr"))

TEXT = {
    "en": {
        "empty": "No writeups yet. This index fills itself when the first one is added.",
        "headers": ("Date", "Platform", "Name", "Category", "Difficulty", "Tags"),
        "total": "Total",
        "by_platform": "By platform",
        "by_category": "By category",
    },
    "tr": {
        "empty": "Henüz writeup yok. İlk writeup eklendiğinde bu indeks kendiliğinden dolacak.",
        "headers": ("Tarih", "Platform", "Ad", "Kategori", "Zorluk", "Etiketler"),
        "total": "Toplam",
        "by_platform": "Platforma göre",
        "by_category": "Kategoriye göre",
    },
}


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        quote = value[0]
        value = value[1:-1]
        if quote == '"':
            value = value.replace('\\"', '"').replace("\\\\", "\\")
    return value


def parse_front_matter(text: str) -> dict[str, str | list[str]]:
    """Parse the simple ``key: value`` / ``key: [a, b]`` front matter used here."""
    text = text.replace("\r\n", "\n").lstrip("\ufeff")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str | list[str]] = {}
    for line in text[4:end].split("\n"):
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            items = [_unquote(p) for p in raw[1:-1].split(",")]
            data[key.strip()] = [i for i in items if i]
        else:
            data[key.strip()] = _unquote(raw)
    return data


def collect(root: Path) -> list[dict]:
    entries = []
    for platform in PLATFORMS:
        for readme in sorted((root / platform).glob("*/README.md")):
            meta = parse_front_matter(readme.read_text(encoding="utf-8"))
            if not meta:
                continue
            tags = meta.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            entries.append(
                {
                    "date": str(meta.get("date", "")),
                    "platform": platform,
                    "name": str(meta.get("title") or readme.parent.name),
                    "category": str(meta.get("category", "")),
                    "difficulty": str(meta.get("difficulty", "")),
                    "tags": tags,
                    "path": readme.relative_to(root).as_posix(),
                }
            )
    entries.sort(key=lambda e: (e["date"], e["name"].lower()), reverse=True)
    return entries


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render(entries: list[dict], lang: str = "en") -> str:
    t = TEXT[lang]
    if not entries:
        return t["empty"]
    lines = [
        "| " + " | ".join(t["headers"]) + " |",
        "|" + "---|" * len(t["headers"]),
    ]
    for e in entries:
        row = (
            _cell(e["date"]),
            _cell(e["platform"]),
            f"[{_cell(e['name'])}]({e['path']})",
            _cell(e["category"]),
            _cell(e["difficulty"]),
            _cell(", ".join(e["tags"])),
        )
        lines.append("| " + " | ".join(row) + " |")
    by_platform = Counter(e["platform"] for e in entries)
    by_category = Counter(e["category"] or "-" for e in entries)
    lines += [
        "",
        f"**{t['total']}:** {len(entries)}",
        "",
        f"**{t['by_platform']}:** " + ", ".join(f"{p}: {by_platform.get(p, 0)}" for p in PLATFORMS),
        "",
        f"**{t['by_category']}:** "
        + ", ".join(f"{c}: {n}" for c, n in sorted(by_category.items())),
    ]
    return "\n".join(lines)


def replace_block(readme_text: str, block: str) -> str:
    start = readme_text.find(START)
    end = readme_text.find(END)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"markers {START} / {END} not found")
    return readme_text[: start + len(START)] + "\n" + block + "\n" + readme_text[end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate the writeup index in the READMEs.")
    parser.add_argument("--check", action="store_true", help="do not write; exit 1 if outdated")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    entries = collect(args.root)
    print(f"Found {len(entries)} writeup(s).")
    outdated = False
    for filename, lang in TARGETS:
        path = args.root / filename
        if not path.is_file():
            print(f"error: {filename} not found", file=sys.stderr)
            return 2
        old = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        try:
            new = replace_block(old, render(entries, lang))
        except ValueError as exc:
            print(f"error: {filename}: {exc}", file=sys.stderr)
            return 2
        if new == old:
            print(f"{filename}: up to date")
            continue
        if args.check:
            print(f"{filename}: OUT OF DATE (run python tools/build_index.py)")
            outdated = True
        else:
            with path.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(new)
            print(f"{filename}: updated")
    return 1 if outdated else 0


if __name__ == "__main__":
    sys.exit(main())
