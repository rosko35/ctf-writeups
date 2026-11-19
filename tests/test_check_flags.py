from __future__ import annotations

import check_flags
import pytest

# Built by concatenation so this file itself never contains a flag-shaped string.
THM = "THM" + "{"
HTB = "HTB" + "{"
PICO = "picoCTF" + "{"
GENERIC = "flag" + "{"


@pytest.mark.parametrize("prefix", [THM, HTB, PICO, GENERIC])
def test_real_looking_flags_are_found(prefix):
    assert check_flags.scan_text(f"the answer is {prefix}n0t_s3cret}}") != []


def test_case_insensitive_prefix():
    assert check_flags.scan_text("Flag" + "{abc123}") != []
    assert check_flags.scan_text("thm" + "{abc123}") != []


@pytest.mark.parametrize(
    "inner", ["...", "…", "***", "xxxx", "redacted", "REDACTED", "<redacted>", "<flag here>", ""]
)
def test_redacted_forms_are_allowed(inner):
    for prefix in (THM, HTB, PICO, GENERIC):
        assert check_flags.scan_text(f"{prefix}{inner}}}") == []


def test_line_numbers_and_multiple_matches():
    text = f"ok\n{THM}...}} and {HTB}secret}}\n{PICO}a}}"
    assert check_flags.scan_text(text) == [(2, "HTB"), (3, "picoCTF")]


def test_no_false_positive_inside_words():
    assert check_flags.scan_text("xflag" + "{abc}") == []
    assert check_flags.scan_text("f = {a: 1}") == []


def test_scan_repo_and_exit_codes(tmp_path, capsys):
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "ok.md").write_text(f"`{THM}...}}`", encoding="utf-8")
    assert check_flags.main([str(tmp_path)]) == 0
    assert "OK" in capsys.readouterr().out

    (tmp_path / "tryhackme").mkdir()
    (tmp_path / "tryhackme" / "w.md").write_text(f"x\n{THM}leak}}\n", encoding="utf-8")
    assert check_flags.main([str(tmp_path)]) == 1
    out = capsys.readouterr()
    assert "tryhackme/w.md:2" in out.out
    assert "leak" not in out.out  # the value itself is never echoed


def test_skips_ignored_dirs_and_binary(tmp_path):
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "x.txt").write_text(f"{THM}leak}}", encoding="utf-8")
    (tmp_path / "bin.dat").write_bytes(b"\xff\xfe\x00" + f"{THM}leak}}".encode())
    (tmp_path / "pic.png").write_bytes(f"{THM}leak}}".encode())
    assert check_flags.scan_repo(tmp_path) == []
