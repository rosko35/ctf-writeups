#!/usr/bin/env python3
"""Fail if the repository contains unredacted CTF flags.

Looks for THM{...}, HTB{...}, picoCTF{...} and flag{...}. A match is accepted only
when the braces hold an obvious redaction (``...``, ``***``, ``xxx``, ``redacted``,
``<placeholder>`` or nothing). Anything else counts as a leaked flag.

    python tools/check_flags.py [path]      # exit 1 if a flag is found
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FLAG_RE = re.compile(r"(?<![A-Za-z0-9_])(THM|HTB|picoCTF|flag)\{([^}\n]*)\}", re.IGNORECASE)
REDACTED_RE = re.compile(
    r"^\s*(?:|\.{2,}|…|\*+|x+|[<\[(]?\s*redacted\s*[>\])]?|<[^<>]*>)\s*$",
    re.IGNORECASE,
)
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
SKIP_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".pdf", ".zip", ".gz", ".7z",
    ".pcap", ".pcapng", ".pyc", ".bin", ".exe", ".mp4",
}  # fmt: skip
MAX_BYTES = 5_000_000


def is_redacted(inner: str) -> bool:
    return bool(REDACTED_RE.match(inner))


def scan_text(text: str) -> list[tuple[int, str]]:
    """Return (line number, prefix) for every unredacted flag in ``text``."""
    found = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in FLAG_RE.finditer(line):
            if not is_redacted(match.group(2)):
                found.append((lineno, match.group(1)))
    return found


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES or path.stat().st_size > MAX_BYTES:
            continue
        yield path


def scan_repo(root: Path) -> list[tuple[Path, int, str]]:
    results = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, prefix in scan_text(text):
            results.append((path.relative_to(root), lineno, prefix))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan the repo for unredacted flags.")
    parser.add_argument("path", nargs="?", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)

    results = scan_repo(args.path)
    if not results:
        print("OK: no unredacted flags found.")
        return 0
    for rel, lineno, prefix in results:
        print(f"{rel.as_posix()}:{lineno}: unredacted flag ({prefix}{{...}}) - redact it")
    print(f"FAIL: {len(results)} unredacted flag(s) found.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
