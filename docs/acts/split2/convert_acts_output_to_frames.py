from __future__ import annotations

import argparse
import csv
from pathlib import Path


FRAME_FIELDS = [
    "frame_id",
    "output_mode",
    "output_type",
    "string_content_class",
    "result_cardinality",
    "expect_rc",
    "expect_stderr",
    "expect_stdout_rule",
    "pytest_test",
    "result",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert ACTS exported CSV to split2_pairwise_frames.csv format."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("docs/acts/split2/Split2_Output_Formatting-output.csv"),
        help="Path to ACTS exported CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/acts/split2/split2_pairwise_frames.csv"),
        help="Path to output frames CSV.",
    )
    return parser.parse_args()


def non_comment_lines(path: Path) -> list[str]:
    lines: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            lines.append(line)
    return lines


def convert_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    frames: list[dict[str, str]] = []
    for idx, row in enumerate(source_rows, start=1):
        frames.append(
            {
                "frame_id": f"F{idx:02d}",
                "output_mode": row["output_mode"],
                "output_type": row["output_type"],
                "string_content_class": row["string_content_class"],
                "result_cardinality": row["result_cardinality"],
                "expect_rc": "0",
                "expect_stderr": "empty",
                "expect_stdout_rule": "exact_bytes",
                "pytest_test": "test_split2_frame",
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
