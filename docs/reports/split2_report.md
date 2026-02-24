# Split 2 Report (Output Formatting + Encoding)

## Environment

- Date: 2026-02-22 23:18:12 Pacific Standard Time
- OS: Windows-11-10.0.26100-SP0
- Python version: 3.12.10
- jq version: jq-1.8.1

## Test Suite Summary

- Test path: `tests/split2/test_split2.py`
- ACTS model: `docs/acts/split2/split2_acts_model.md`
- Constraint model: `docs/acts/split2/split2_constraints.md`
- Pairwise frame file: `docs/acts/split2/split2_pairwise_frames.csv` (30 frames, F01–F30)
- Frame set source: ACTS export converted via `docs/acts/split2/convert_acts_output_to_frames.py`
- Coverage strength: 2-way (pairwise)
- Frames generated: 30
- Total pytest tests run: 30
- Passed: 30
- Failed: 0
- Skipped: 0

*(Re-run `python -m pytest tests/split2 -q` after regenerating the frame CSV to refresh pass/fail counts.)*

## Coverage Notes

- Scope covered: `-c`, `-r`, `-j`, and `--raw-output0` output semantics.
- Partition dimensions covered:
  - output mode,
  - output type,
  - string content class (plain/quote+backslash/unicode/embedded newline),
  - result cardinality (single/multiple).
- Oracle style: exact `stdout` byte comparisons, empty `stderr`, and return code checks.

## Frame-to-Test Traceability

All generated pairwise frames (`F01`-`F30`) are executed by a parameterized test:

- `test_split2_frame` in `tests/split2/test_split2.py`

Each frame row in `docs/acts/split2/split2_pairwise_frames.csv` maps to one concrete test invocation.

## Bugs Found

No confirmed jq defects were found in this run.

Observed platform-specific detail:

- On Windows, jq output newline bytes are `CRLF` (`0x0D 0x0A`) rather than `LF` (`0x0A`) for text-mode writes; assertions were made byte-accurate for the active platform.

## Observations and Conclusions

- The generated split2 suite achieved pairwise coverage across the constrained category-partition model.
- All 30 generated tests passed.
- Output formatting behavior matched the expected mode-specific rules:
  - compact JSON (`-c`),
  - raw string output (`-r`),
  - joined output without record newline (`-j`),
  - NUL-terminated raw output (`--raw-output0`).
