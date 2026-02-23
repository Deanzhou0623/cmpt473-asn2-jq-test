# Split 3 Report (Error Handling + `-e` Exit Status)

## Environment

- Date: 2026-02-22 20:45:23 PST
- OS: Darwin 24.6.0 (arm64)
- Python version: 3.10.11
- jq version: jq-1.7.1-apple

## Test Suite Summary

- Test path: `tests/split3/test_split3.py`
- ACTS model: `docs/acts/split3/split3_acts_model.md`
- Pairwise frame file: `docs/acts/split3/split3_pairwise_frames.csv`
- Coverage strength: 2-way (pairwise)
- Frames executed: 11
- Total pytest tests run: 11
- Passed: 11
- Failed: 0
- Skipped: 0

## Coverage Notes

- Focused behaviors: invalid JSON, empty input behavior, invalid filter, missing file, permission denied, and `-e` exit-status semantics.
- Oracle dimensions: return code, stderr pattern, stdout empty/non-empty.
- Stderr checks are pattern-based (`parse`, `compile|syntax`, `could not open|no such file`, `permission|denied`) for portability across OS/jq wording.

## Frame-to-Test Traceability

| Frame | Pytest Test | Outcome |
| --- | --- | --- |
| F01 | `test_invalid_json_file_returns_parse_error_and_no_stdout` | Pass |
| F02 | `test_empty_json_file_returns_parse_error_and_no_stdout` | Pass |
| F03 | `test_invalid_filter_returns_compile_or_syntax_error_and_no_stdout` | Pass |
| F04 | `test_missing_file_returns_open_error_and_no_stdout` | Pass |
| F05 | `test_permission_denied_returns_error` | Pass |
| F06 | `test_exit_status_truthy_output_returns_zero_nonempty_stdout_empty_stderr` | Pass |
| F07 | `test_exit_status_missing_returns_one_and_quiet_stderr` | Pass |
| F08 | `test_exit_status_false_returns_one` | Pass |
| F09 | `test_exit_status_null_returns_one` | Pass |
| F10 | `test_exit_status_no_output_empty_filter_returns_four` | Pass |
| F11 | `test_exit_status_invalid_filter_returns_three_and_compile_error` | Pass |

## Bugs Found

No confirmed jq defects were found in this run.

Observed version-specific detail:

- Malformed JSON (`invalid.json`) returned parse error with exit code `5` on jq-1.7.1-apple; test oracle intentionally checks nonzero + parse-pattern for portability.

## Observations and Conclusions

- Exit-code behavior aligns with jq manual for the tested classes: file/system errors `2`, compile errors `3`, `-e` false/null `1`, and `-e` no-output `4`.
- Split 3 now has complete traceability from category/constraints -> pairwise frames -> automated execution results.
