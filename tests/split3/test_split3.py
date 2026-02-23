import os
import re
import stat
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common.run_jq import run_jq


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def fixture_path(name: str) -> str:
    return str(FIXTURES_DIR / name)


def assert_stderr_matches(stderr: str, pattern: str) -> None:
    assert re.search(pattern, stderr, flags=re.IGNORECASE), f"stderr did not match /{pattern}/: {stderr!r}"


def test_invalid_json_file_returns_parse_error_and_no_stdout() -> None:
    rc, out, err = run_jq([".", fixture_path("invalid.json")])

    assert rc != 0
    assert out.strip() == ""
    assert_stderr_matches(err, r"parse")


def test_empty_json_file_returns_parse_error_and_no_stdout() -> None:
    rc, out, err = run_jq([".", fixture_path("empty.json")])

    assert out.strip() == ""
    # jq versions differ here: some treat empty input as parse error,
    # others as a valid "no-input" case with exit 0.
    if rc == 0:
        assert err.strip() == ""
    else:
        assert_stderr_matches(err, r"parse")


def test_invalid_filter_returns_compile_or_syntax_error_and_no_stdout() -> None:
    rc, out, err = run_jq([".[ ", fixture_path("valid.json")])

    assert rc == 3
    assert out.strip() == ""
    assert_stderr_matches(err, r"compile|syntax")


def test_missing_file_returns_open_error_and_no_stdout() -> None:
    missing = str(FIXTURES_DIR / "does_not_exist.json")
    rc, out, err = run_jq([".", missing])

    assert rc == 2
    assert out.strip() == ""
    assert_stderr_matches(err, r"could\s+not\s+open|no\s+such\s+file")


def test_permission_denied_returns_error(tmp_path: Path) -> None:
    if os.name == "nt":
        pytest.skip("POSIX permission mode test is not portable on Windows")

    path = tmp_path / "no_read.json"
    path.write_text('{"a":1}\n', encoding="utf-8")

    original_mode = path.stat().st_mode
    try:
        path.chmod(0)

        # Skip when effective user can still read despite chmod 000 (e.g., root or special FS).
        if os.access(path, os.R_OK):
            pytest.skip("Permission model allows reading chmod 000 file in this environment")

        rc, out, err = run_jq([".", str(path)])
        assert rc == 2
        assert out.strip() == ""
        assert_stderr_matches(err, r"permission|denied|could\s+not\s+open")
    finally:
        # Ensure cleanup can remove the temp file.
        path.chmod(original_mode | stat.S_IRUSR | stat.S_IWUSR)


def test_exit_status_truthy_output_returns_zero_nonempty_stdout_empty_stderr() -> None:
    rc, out, err = run_jq(["-e", ".a", fixture_path("valid.json")])

    assert rc == 0
    assert out.strip() != ""
    assert err.strip() == ""


def test_exit_status_missing_returns_one_and_quiet_stderr() -> None:
    rc, out, err = run_jq(["-e", ".missing", fixture_path("valid.json")])

    assert rc == 1
    # jq versions may print null for missing key; accept either empty or null output.
    assert out.strip() in {"", "null"}
    assert err.strip() == ""


def test_exit_status_false_returns_one() -> None:
    rc, _out, err = run_jq(["-e", ".c", fixture_path("valid.json")])

    assert rc == 1
    assert err.strip() == ""


def test_exit_status_null_returns_one() -> None:
    rc, _out, err = run_jq(["-e", ".b", fixture_path("valid.json")])

    assert rc == 1
    assert err.strip() == ""


def test_exit_status_no_output_empty_filter_returns_four() -> None:
    rc, out, err = run_jq(["-e", "empty", fixture_path("valid.json")])

    assert rc == 4
    assert out.strip() == ""
    assert err.strip() == ""


def test_exit_status_invalid_filter_returns_three_and_compile_error() -> None:
    rc, out, err = run_jq(["-e", ".[ ", fixture_path("valid.json")])

    assert rc == 3
    assert out.strip() == ""
    assert_stderr_matches(err, r"compile|syntax")
