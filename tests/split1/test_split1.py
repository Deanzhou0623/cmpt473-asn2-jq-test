"""Split 1: Input modes & file ingestion tests for jq.

Tests cover file vs stdin input, -R (raw-input), -s (slurp),
-n (null-input), and error cases (missing file, invalid JSON).
"""

import json
import re
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common.run_jq import run_jq

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def fixture_path(name: str) -> str:
    return str(FIXTURES_DIR / name)


def read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


def parse_json_stream(text: str) -> list:
    """Parse multiple concatenated JSON values from jq output."""
    decoder = json.JSONDecoder()
    values = []
    idx = 0
    text = text.strip()
    while idx < len(text):
        obj, end = decoder.raw_decode(text, idx)
        values.append(obj)
        idx = end
        while idx < len(text) and text[idx] in " \t\n\r":
            idx += 1
    return values


def assert_stderr_matches(stderr: str, pattern: str) -> None:
    assert re.search(pattern, stderr, flags=re.IGNORECASE), (
        f"stderr did not match /{pattern}/: {stderr!r}"
    )


# ---------------------------------------------------------------------------
# F01: file + valid_json + default mode
# ---------------------------------------------------------------------------
def test_file_valid_json_default() -> None:
    rc, out, err = run_jq([".", fixture_path("valid.json")])
    assert rc == 0
    assert json.loads(out) == {"a": 1, "b": "hello", "arr": [1, 2, 3]}
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F02: stdin + valid_json + default mode
# ---------------------------------------------------------------------------
def test_stdin_valid_json_default() -> None:
    content = read_fixture("valid.json")
    rc, out, err = run_jq([".", "-"], input_text=content)
    assert rc == 0
    assert json.loads(out) == {"a": 1, "b": "hello", "arr": [1, 2, 3]}
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F03: file + multi_json + default mode
# ---------------------------------------------------------------------------
def test_file_multi_json_default() -> None:
    rc, out, err = run_jq([".", fixture_path("multi.json")])
    assert rc == 0
    values = parse_json_stream(out)
    assert values == [{"x": 1}, {"x": 2}]
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F04: stdin + multi_json + default mode
# ---------------------------------------------------------------------------
def test_stdin_multi_json_default() -> None:
    content = read_fixture("multi.json")
    rc, out, err = run_jq([".", "-"], input_text=content)
    assert rc == 0
    values = parse_json_stream(out)
    assert values == [{"x": 1}, {"x": 2}]
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F05: file + plain_text + -R (raw-input)
# ---------------------------------------------------------------------------
def test_file_plain_text_raw_input() -> None:
    rc, out, err = run_jq(["-R", ".", fixture_path("plain.txt")])
    assert rc == 0
    lines = [json.loads(line) for line in out.strip().split("\n")]
    assert lines == ["hello world", "this is plain text", "line three"]
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F06: stdin + plain_text + -R (raw-input)
# ---------------------------------------------------------------------------
def test_stdin_plain_text_raw_input() -> None:
    content = read_fixture("plain.txt")
    rc, out, err = run_jq(["-R", ".", "-"], input_text=content)
    assert rc == 0
    lines = [json.loads(line) for line in out.strip().split("\n")]
    assert lines == ["hello world", "this is plain text", "line three"]
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F07: file + valid_json + -s (slurp)
# ---------------------------------------------------------------------------
def test_file_valid_json_slurp() -> None:
    rc, out, err = run_jq(["-s", ".", fixture_path("valid.json")])
    assert rc == 0
    assert json.loads(out) == [{"a": 1, "b": "hello", "arr": [1, 2, 3]}]
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F08: stdin + multi_json + -s (slurp)
# ---------------------------------------------------------------------------
def test_stdin_multi_json_slurp() -> None:
    content = read_fixture("multi.json")
    rc, out, err = run_jq(["-s", ".", "-"], input_text=content)
    assert rc == 0
    assert json.loads(out) == [{"x": 1}, {"x": 2}]
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F09: file + plain_text + -R -s (raw + slurp)
# ---------------------------------------------------------------------------
def test_file_plain_text_raw_slurp() -> None:
    rc, out, err = run_jq(["-R", "-s", ".", fixture_path("plain.txt")])
    assert rc == 0
    result = json.loads(out)
    assert result == "hello world\nthis is plain text\nline three\n"
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F10: stdin + valid_json + -R -s (raw + slurp)
# ---------------------------------------------------------------------------
def test_stdin_valid_json_raw_slurp() -> None:
    content = read_fixture("valid.json")
    rc, out, err = run_jq(["-R", "-s", ".", "-"], input_text=content)
    assert rc == 0
    result = json.loads(out)
    # The entire file content is read as a raw string (including trailing newline)
    assert result == content
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F11: file + valid_json + -n (null-input)
# ---------------------------------------------------------------------------
def test_file_null_input() -> None:
    rc, out, err = run_jq(["-n", ".", fixture_path("valid.json")])
    assert rc == 0
    assert json.loads(out) is None
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F12: stdin + empty + -n (null-input)
# ---------------------------------------------------------------------------
def test_stdin_null_input_empty() -> None:
    rc, out, err = run_jq(["-n", ".", "-"], input_text="")
    assert rc == 0
    assert json.loads(out) is None
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F13: file + missing_file -> error
# ---------------------------------------------------------------------------
def test_file_missing_error() -> None:
    rc, out, err = run_jq([".", fixture_path("nonexistent.json")])
    assert rc == 2
    assert out.strip() == ""
    assert_stderr_matches(err, r"could not open|no such file")


# ---------------------------------------------------------------------------
# F14: file + invalid_json -> parse error
# ---------------------------------------------------------------------------
def test_file_invalid_json_parse_error() -> None:
    rc, out, err = run_jq([".", fixture_path("invalid.json")])
    assert rc != 0
    assert out.strip() == ""
    assert_stderr_matches(err, r"parse error")


# ---------------------------------------------------------------------------
# F15: stdin + invalid_json -> parse error
# ---------------------------------------------------------------------------
def test_stdin_invalid_json_parse_error() -> None:
    content = read_fixture("invalid.json")
    rc, out, err = run_jq([".", "-"], input_text=content)
    assert rc != 0
    assert out.strip() == ""
    assert_stderr_matches(err, r"parse error")


# ---------------------------------------------------------------------------
# F16: file + invalid_json + -R -> raw-input bypasses JSON parsing
# ---------------------------------------------------------------------------
def test_file_invalid_json_raw_input_bypasses_parse() -> None:
    rc, out, err = run_jq(["-R", ".", fixture_path("invalid.json")])
    assert rc == 0
    result = json.loads(out)
    assert isinstance(result, str)
    assert err.strip() == ""


# ---------------------------------------------------------------------------
# F17: file + empty + default mode
# ---------------------------------------------------------------------------
def test_file_empty_default() -> None:
    rc, out, err = run_jq([".", fixture_path("empty.json")])
    assert rc == 0
    assert out.strip() == ""


# ---------------------------------------------------------------------------
# F18: file + empty + -s (slurp)
# ---------------------------------------------------------------------------
def test_file_empty_slurp() -> None:
    rc, out, err = run_jq(["-s", ".", fixture_path("empty.json")])
    assert rc == 0
    assert json.loads(out) == []
    assert err.strip() == ""
