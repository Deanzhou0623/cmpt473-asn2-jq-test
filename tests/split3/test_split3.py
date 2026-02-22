import re
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common.run_jq import run_jq


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def fixture_path(name: str) -> str:
    return str(FIXTURES_DIR / name)


def test_invalid_json_returns_error_and_parse_message() -> None:
    rc, _out, err = run_jq([".", fixture_path("invalid.json")])

    assert rc != 0
    assert re.search(r"parse", err, flags=re.IGNORECASE)


def test_invalid_filter_returns_compile_or_syntax_error() -> None:
    rc, _out, err = run_jq([".[", fixture_path("valid.json")])

    assert rc != 0
    assert re.search(r"compile|syntax", err, flags=re.IGNORECASE)


def test_missing_file_returns_open_error() -> None:
    missing = str(FIXTURES_DIR / "does_not_exist.json")
    rc, _out, err = run_jq([".", missing])

    assert rc != 0
    assert re.search(r"could\s+not\s+open|no\s+such\s+file", err, flags=re.IGNORECASE)


def test_exit_status_e_truthy_value_returns_zero() -> None:
    rc, out, _err = run_jq(["-e", ".a", fixture_path("valid.json")])

    assert rc == 0
    assert out.strip() != ""


def test_exit_status_e_missing_value_returns_nonzero() -> None:
    rc, _out, _err = run_jq(["-e", ".missing", fixture_path("valid.json")])

    assert rc != 0


def test_exit_status_e_false_returns_one() -> None:
    rc, _out, _err = run_jq(["-e", ".c", fixture_path("valid.json")])

    assert rc == 1


def test_exit_status_e_null_returns_one() -> None:
    rc, _out, _err = run_jq(["-e", ".b", fixture_path("valid.json")])

    assert rc == 1
