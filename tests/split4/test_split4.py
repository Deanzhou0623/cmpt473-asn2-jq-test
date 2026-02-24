import json
import os
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common.run_jq import run_jq

FIXTURE_DIR = Path(__file__).parent / "fixtures"

def get_fixture_path(name):
    return str(FIXTURE_DIR / name)

def test_select_numbers():
    """F01: select( . > 1 ) on num_array [3, 1, 2, 2]"""
    # jq 'map(select(. > 1))' fixtures/numbers.json -> [3, 2, 2]
    # Note: select usually operates on the stream, so map(select) or just .[] | select
    rc, stdout, stderr = run_jq(["map(select(. > 1))", get_fixture_path("numbers.json")])
    assert rc == 0
    assert json.loads(stdout) == [3, 2, 2]

def test_map_missing_keys():
    """F02: map(.id) on obj_array with missing keys"""
    # [{"id": 1}, {"id": 2}, {"id": 1}, {"other": 3}] -> [1, 2, 1, null]
    rc, stdout, stderr = run_jq(["map(.id)", get_fixture_path("objects.json")])
    assert rc == 0
    assert json.loads(stdout) == [1, 2, 1, None]

def test_sort_numbers():
    """F03: sort on unsorted num_array [3, 1, 2, 2]"""
    rc, stdout, stderr = run_jq(["sort", get_fixture_path("numbers.json")])
    assert rc == 0
    assert json.loads(stdout) == [1, 2, 2, 3]

def test_group_by_objects():
    """F04: group_by(.id) on objects with duplicates"""
    # [{"id": 1}, {"id": 2}, {"id": 1}, {"other": 3}]
    # grouped by .id: [[{"id": 1}, {"id": 1}], [{"id": 2}], [{"other": 3}]]
    rc, stdout, stderr = run_jq(["group_by(.id)", get_fixture_path("objects.json")])
    assert rc == 0
    result = json.loads(stdout)
    expected = [
        [{"other": 3}],
        [{"id": 1}, {"id": 1}],
        [{"id": 2}],
    ]
    assert result == expected

def test_unique_mixed():
    """F05: unique on mixed_array [1, "a", 1, null]"""
    rc, stdout, stderr = run_jq(["unique", get_fixture_path("mixed.json")])
    assert rc == 0
    # [null, 1, "a"]
    assert json.loads(stdout) == [None, 1, "a"]

def test_add_numbers():
    """F06: add on [3, 1, 2, 2] -> 8"""
    rc, stdout, stderr = run_jq(["add", get_fixture_path("numbers.json")])
    assert rc == 0
    assert json.loads(stdout) == 8

def test_length_string():
    """F07: length on "hello" -> 5"""
    rc, stdout, stderr = run_jq(["length", get_fixture_path("string.json")])
    assert rc == 0
    assert json.loads(stdout) == 5

def test_select_missing_keys():
    """F08: select(.id == 1) on obj_array"""
    rc, stdout, stderr = run_jq(["map(select(.id == 1))", get_fixture_path("objects.json")])
    assert rc == 0
    assert json.loads(stdout) == [{"id": 1}, {"id": 1}]

def test_map_mixed():
    """F09: map(type) on mixed_array [1, "a", 1, null]"""
    rc, stdout, stderr = run_jq(["map(type)", get_fixture_path("mixed.json")])
    assert rc == 0
    assert json.loads(stdout) == ["number", "string", "number", "null"]

def test_sort_empty():
    """F10: sort on []"""
    rc, stdout, stderr = run_jq(["sort", get_fixture_path("empty.json")])
    assert rc == 0
    assert json.loads(stdout) == []

def test_group_by_numbers():
    """F11: group_by(.) on unsorted numbers [3, 1, 2, 2]"""
    rc, stdout, stderr = run_jq(["group_by(.)", get_fixture_path("numbers.json")])
    assert rc == 0
    # [[1], [2, 2], [3]]
    assert json.loads(stdout) == [[1], [2, 2], [3]]

def test_unique_objects():
    """F12: unique on objects (no duplicates in this sense if we consider whole object)"""
    # [{"id": 1}, {"id": 2}, {"id": 1}, {"other": 3}] -> [{"id": 1}, {"id": 2}, {"other": 3}]
    assert rc == 0
    expected_result = [
        {"id": 1},
        {"id": 2},
        {"other": 3}
    ]
    assert json.loads(stdout) == expected_result
def test_add_empty():
    """F13: add on [] -> null"""
    rc, stdout, stderr = run_jq(["add", get_fixture_path("empty.json")])
    assert rc == 0
    assert json.loads(stdout) == None

def test_length_object():
    """F14: length on {"a": 1, "b": 2} -> 2"""
    rc, stdout, stderr = run_jq(["length", get_fixture_path("object_simple.json")])
    assert rc == 0
    assert json.loads(stdout) == 2

def test_length_null():
    """F15: length on null -> 0 (in recent jq) or error"""
    rc, stdout, stderr = run_jq(["length", get_fixture_path("null.json")])
    # jq 1.6+ returns 0 for length on null
    if rc == 0:
        assert json.loads(stdout) == 0
    else:
        assert "cannot be applied to: null" in stderr
