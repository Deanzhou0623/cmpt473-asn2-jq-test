import csv
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common.run_jq import run_jq_bytes


THIS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = THIS_DIR / "fixtures"
FRAMES_CSV = Path(__file__).resolve().parents[2] / "docs" / "acts" / "split2" / "split2_pairwise_frames.csv"
VALUES_JSON = FIXTURES_DIR / "values.json"

MODE_FLAG = {
    "default": [],
    "compact": ["-c"],
    "raw": ["-r"],
    "join": ["-j"],
    "raw0": ["--raw-output0"],
}


def load_frames() -> list[dict[str, str]]:
    with FRAMES_CSV.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_values() -> dict:
    with VALUES_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def filter_for_frame(frame: dict[str, str]) -> str:
    output_type = frame["output_type"]
    string_class = frame["string_content_class"]
    cardinality = frame["result_cardinality"]

    if output_type == "string":
        single_map = {
            "plain": ".plain",
            "quote_backslash": ".quote_backslash",
            "unicode": ".unicode",
            "embedded_newline": ".embedded_newline",
        }
        multi_map = {
            "plain": ".multi_strings[]",
            "quote_backslash": ".multi_quote_backslash[]",
            "unicode": ".multi_unicode[]",
            "embedded_newline": ".multi_embedded_newline[]",
        }
        return single_map[string_class] if cardinality == "single" else multi_map[string_class]

    single_map = {
        "number": ".number",
        "object": ".object",
        "array": ".array",
        "bool": ".bool",
        "null": ".null",
    }
    multi_map = {
        "number": ".multi_numbers[]",
        "object": ".multi_objects[]",
        "array": ".multi_arrays[]",
        "bool": ".multi_bools[]",
        "null": ".multi_nulls[]",
    }
    return single_map[output_type] if cardinality == "single" else multi_map[output_type]


def values_for_frame(frame: dict[str, str], values_doc: dict) -> list:
    output_type = frame["output_type"]
    string_class = frame["string_content_class"]
    cardinality = frame["result_cardinality"]

    if output_type == "string":
        single_map = {
            "plain": values_doc["plain"],
            "quote_backslash": values_doc["quote_backslash"],
            "unicode": values_doc["unicode"],
            "embedded_newline": values_doc["embedded_newline"],
        }
        multi_map = {
            "plain": values_doc["multi_strings"],
            "quote_backslash": values_doc["multi_quote_backslash"],
            "unicode": values_doc["multi_unicode"],
            "embedded_newline": values_doc["multi_embedded_newline"],
        }
        return [single_map[string_class]] if cardinality == "single" else list(multi_map[string_class])

    single_map = {
        "number": values_doc["number"],
        "object": values_doc["object"],
        "array": values_doc["array"],
        "bool": values_doc["bool"],
        "null": values_doc["null"],
    }
    multi_map = {
        "number": values_doc["multi_numbers"],
        "object": values_doc["multi_objects"],
        "array": values_doc["multi_arrays"],
        "bool": values_doc["multi_bools"],
        "null": values_doc["multi_nulls"],
    }
    return [single_map[output_type]] if cardinality == "single" else list(multi_map[output_type])


def render_json(value: object, compact: bool) -> bytes:
    if compact:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    else:
        text = json.dumps(value, ensure_ascii=False, indent=2)
    return text.encode("utf-8")


def platform_text_bytes(text: str) -> bytes:
    # jq stdout is written in text mode on Windows, so LF bytes become CRLF.
    return text.encode("utf-8").replace(b"\n", os.linesep.encode("ascii"))


def expected_stdout_bytes(frame: dict[str, str], produced_values: list) -> bytes:
    mode = frame["output_mode"]
    if mode == "default":
        nl = os.linesep.encode("ascii")
        return b"".join(render_json(v, compact=False).replace(b"\n", nl) + nl for v in produced_values)
    if mode == "compact":
        nl = os.linesep.encode("ascii")
        return b"".join(render_json(v, compact=True).replace(b"\n", nl) + nl for v in produced_values)
    if mode == "raw":
        nl = os.linesep.encode("ascii")
        return b"".join(platform_text_bytes(str(v)) + nl for v in produced_values)
    if mode == "join":
        return b"".join(platform_text_bytes(str(v)) for v in produced_values)
    if mode == "raw0":
        return b"".join(platform_text_bytes(str(v)) + b"\x00" for v in produced_values)
    raise AssertionError(f"unsupported output mode: {mode}")


@pytest.mark.parametrize("frame", load_frames(), ids=lambda f: f["frame_id"])
def test_split2_frame(frame: dict[str, str]) -> None:
    values_doc = load_values()
    jq_filter = filter_for_frame(frame)
    jq_args = [*MODE_FLAG[frame["output_mode"]], jq_filter, str(VALUES_JSON)]

    rc, out, err = run_jq_bytes(jq_args)

    expected = expected_stdout_bytes(frame, values_for_frame(frame, values_doc))
    assert rc == 0, f"frame={frame['frame_id']} rc={rc} stderr={err!r}"
    assert err == b"", f"frame={frame['frame_id']} stderr={err!r}"
    assert out == expected, (
        f"frame={frame['frame_id']} mode={frame['output_mode']} "
        f"expected={expected!r} actual={out!r}"
    )
