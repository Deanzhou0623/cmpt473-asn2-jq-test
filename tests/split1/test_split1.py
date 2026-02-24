"""Split 1: Input modes & file ingestion tests for jq.

Tests cover file vs stdin input, -R (raw-input), -s (slurp),
-n (null-input), and error cases (missing file, invalid JSON).

Frames and expectations are generated via ACTS and
`docs/acts/split1/convert_acts_output_to_frames.py`.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common.run_jq import run_jq


THIS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = THIS_DIR / "fixtures"
FRAMES_CSV = THIS_DIR.parents[2] / "docs" / "acts" / "split1" / "split1_pairwise_frames.csv"


def fixture_path(name: str) -> str:
    return str(FIXTURES_DIR / name)


def read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


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


def load_frames() -> list[dict[str, str]]:
    with FRAMES_CSV.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_invocation(frame: dict[str, str]) -> tuple[list[str], str | None, str | None]:
    """Return (jq_args, input_text, fixture_name) for a given frame."""
    raw_input = frame["raw_input"]
    slurp = frame["slurp"]
    null_input = frame["null_input"]
    input_source = frame["input_source"]
    input_content = frame["input_content"]

    args: list[str] = []
    if raw_input == "on":
        args.append("-R")
    if slurp == "on":
        args.append("-s")
    if null_input == "on":
        args.append("-n")

    args.append(".")

    fixture_name: str | None
    if input_content == "valid_json":
        fixture_name = "valid.json"
    elif input_content == "multi_json":
        fixture_name = "multi.json"
    elif input_content == "plain_text":
        fixture_name = "plain.txt"
    elif input_content == "empty":
        fixture_name = "empty.json"
    elif input_content == "invalid_json":
        fixture_name = "invalid.json"
    elif input_content == "missing_file":
        fixture_name = "nonexistent.json"
    else:
        raise AssertionError(f"Unknown input_content: {input_content}")

    input_text: str | None = None
    if input_source == "file":
        # Pass the fixture path as positional argument (even when -n ignores it).
        args.append(fixture_path(fixture_name))
    elif input_source == "stdin":
        args.append("-")
        if input_content != "missing_file":
            input_text = read_fixture(fixture_name)
    else:
        raise AssertionError(f"Unknown input_source: {input_source}")

    return args, input_text, fixture_name


def assert_expectations(
    frame: dict[str, str], rc: int, out: str, err: str, fixture_name: str | None
) -> None:
    # Return code class
    expect_rc = frame["expect_rc"]
    if expect_rc == "0":
        assert rc == 0
    elif expect_rc == "2":
        assert rc == 2
    elif expect_rc == "nonzero":
        assert rc != 0
    else:
        raise AssertionError(f"Unsupported expect_rc: {expect_rc}")

    # Stderr expectations
    pattern = frame["expect_stderr_pattern"]
    if pattern == "empty":
        assert err.strip() == ""
    else:
        assert_stderr_matches(err, pattern)

    # Stdout expectations
    stdout_class = frame["expect_stdout"]

    if stdout_class == "json_object":
        assert json.loads(out) == {"a": 1, "b": "hello", "arr": [1, 2, 3]}
        return

    if stdout_class == "multi_json_values":
        values = parse_json_stream(out)
        assert values == [{"x": 1}, {"x": 2}]
        return

    if stdout_class == "array_of_one":
        assert json.loads(out) == [{"a": 1, "b": "hello", "arr": [1, 2, 3]}]
        return

    if stdout_class == "array_of_two":
        assert json.loads(out) == [{"x": 1}, {"x": 2}]
        return

    if stdout_class == "quoted_lines":
        assert fixture_name is not None
        expected_text = read_fixture(fixture_name)
        expected_lines = expected_text.splitlines()
        lines = [json.loads(line) for line in out.strip().split("\n")] if out.strip() else []
        assert lines == expected_lines
        return

    if stdout_class == "quoted_line":
        assert fixture_name is not None
        expected_text = read_fixture(fixture_name).rstrip("\n")
        result = json.loads(out)
        assert isinstance(result, str)
        assert result == expected_text
        return

    if stdout_class == "concatenated_string":
        assert fixture_name is not None
        expected_text = read_fixture(fixture_name)
        result = json.loads(out)
        assert result == expected_text
        return

    if stdout_class == "null":
        assert json.loads(out) is None
        return

    if stdout_class == "empty":
        assert out.strip() == ""
        return

    if stdout_class == "empty_array":
        assert json.loads(out) == []
        return

    raise AssertionError(f"Unsupported expect_stdout class: {stdout_class}")


@pytest.mark.parametrize("frame", load_frames(), ids=lambda f: f["frame_id"])
def test_split1_frame(frame: dict[str, str]) -> None:
    args, input_text, fixture_name = build_invocation(frame)
    rc, out, err = run_jq(args, input_text=input_text)
    assert_expectations(frame, rc, out, err, fixture_name)
