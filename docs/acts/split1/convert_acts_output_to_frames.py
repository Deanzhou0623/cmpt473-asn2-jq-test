from __future__ import annotations

import argparse
import csv
from pathlib import Path


FRAME_FIELDS = [
    "frame_id",
    "input_source",
    "input_content",
    "raw_input",
    "slurp",
    "null_input",
    "expect_rc",
    "expect_stdout",
    "expect_stderr_pattern",
    "pytest_test",
    "result",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert ACTS exported CSV to split1_pairwise_frames.csv format."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("docs/acts/split1/acts_generated.csv"),
        help="Path to ACTS exported CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/acts/split1/split1_pairwise_frames.csv"),
        help="Path to output frames CSV.",
    )
    return parser.parse_args()


def non_comment_lines(path: Path) -> "Iterator[str]":
    with path.open("r", encoding="utf-8", newline="") as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith("#"):
                continue
            yield line


def classify_expectations(row: dict[str, str]) -> tuple[str, str, str]:
    """
    Map a split1 parameter row to (expect_rc, expect_stdout, expect_stderr_pattern).
    """
    input_content = row["input_content"]
    raw_input = row["raw_input"]
    slurp = row["slurp"]
    null_input = row["null_input"]

    raw_on = raw_input == "on"
    slurp_on = slurp == "on"
    null_on = null_input == "on"

    # File-open error path
    if input_content == "missing_file":
        return "2", "empty", r"could not open|no such file"

    # Null-input path: jq ignores the input stream and passes null to the filter.
    if null_on:
        return "0", "null", "empty"

    # Parse-error paths (invalid JSON or plain-text without -R).
    if (input_content in {"invalid_json", "plain_text"}) and not raw_on:
        return "nonzero", "empty", r"parse error"

    # All remaining cases are successful executions.
    expect_rc = "0"
    expect_stderr_pattern = "empty"

    # Successful stdout classification.
    if input_content == "valid_json":
        if not raw_on and not slurp_on:
            return expect_rc, "json_object", expect_stderr_pattern
        if not raw_on and slurp_on:
            return expect_rc, "array_of_one", expect_stderr_pattern
        if raw_on and not slurp_on:
            return expect_rc, "quoted_lines", expect_stderr_pattern
        if raw_on and slurp_on:
            return expect_rc, "concatenated_string", expect_stderr_pattern

    if input_content == "multi_json":
        if not raw_on and not slurp_on:
            return expect_rc, "multi_json_values", expect_stderr_pattern
        if not raw_on and slurp_on:
            return expect_rc, "array_of_two", expect_stderr_pattern
        if raw_on and not slurp_on:
            return expect_rc, "quoted_lines", expect_stderr_pattern
        if raw_on and slurp_on:
            return expect_rc, "concatenated_string", expect_stderr_pattern

    if input_content == "plain_text":
        # parse-error cases without -R were handled above
        if raw_on and not slurp_on:
            return expect_rc, "quoted_lines", expect_stderr_pattern
        if raw_on and slurp_on:
            return expect_rc, "concatenated_string", expect_stderr_pattern

    if input_content == "empty":
        if not raw_on and not slurp_on:
            return expect_rc, "empty", expect_stderr_pattern
        if not raw_on and slurp_on:
            return expect_rc, "empty_array", expect_stderr_pattern
        if raw_on and not slurp_on:
            # No lines to read -> no output.
            return expect_rc, "empty", expect_stderr_pattern
        if raw_on and slurp_on:
            # Concatenation of zero lines is the empty string.
            return expect_rc, "concatenated_string", expect_stderr_pattern

    if input_content == "invalid_json" and raw_on and slurp_on:
        # Raw + slurp over invalid JSON treats it as text and concatenates;
        # there is no parse error in this mode.
        return "0", "concatenated_string", "empty"

    raise ValueError(f"Unhandled combination for row: {row}")


def convert_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    frames: list[dict[str, str]] = []
    for idx, row in enumerate(source_rows, start=1):
        expect_rc, expect_stdout, expect_stderr_pattern = classify_expectations(row)
        frames.append(
            {
                "frame_id": f"F{idx:02d}",
                "input_source": row["input_source"],
                "input_content": row["input_content"],
                "raw_input": row["raw_input"],
                "slurp": row["slurp"],
                "null_input": row["null_input"],
                "expect_rc": expect_rc,
                "expect_stdout": expect_stdout,
                "expect_stderr_pattern": expect_stderr_pattern,
                "pytest_test": "test_split1_frame",
                "result": "",
            }
        )
    return frames


def write_frames(path: Path, frames: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FRAME_FIELDS)
        writer.writeheader()
        writer.writerows(frames)


def main() -> int:
    args = parse_args()
    clean_lines = non_comment_lines(args.input)
    rows = list(csv.DictReader(clean_lines))
    frames = convert_rows(rows)
    write_frames(args.output, frames)
    print(f"Wrote {len(frames)} frames to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

