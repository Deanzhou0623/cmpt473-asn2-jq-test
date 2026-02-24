# Split 1 Report (Input Modes & File Ingestion)

## Environment

- Date: 2026-02-23 18:48:57 PST
- OS: Darwin 24.5.0 (arm64)
- Python version: 3.12.4
- jq version: jq-1.6

## Test Suite Summary

- Test path: `tests/split1/test_split1.py`
- ACTS model: `docs/acts/split1/split1_acts_model.md`
- Pairwise frame file: `docs/acts/split1/split1_pairwise_frames.csv`
- Coverage strength: 2-way (pairwise)
- Frames executed: 18
- Total pytest tests run: 18
- Passed: 18, Failed: 0, Skipped: 0

## Coverage Notes

Tests cover all five parameter dimensions:

1. **Input source**: file path argument vs stdin pipe (7 stdin tests, 11 file tests)
2. **Input content**: valid JSON, multiple JSON values, plain text, empty file, invalid JSON, missing file
3. **Raw input (`-R`)**: on/off — verified that `-R` bypasses JSON parsing and treats lines as strings
4. **Slurp (`-s`)**: on/off — verified array aggregation and combined `-R -s` string concatenation
5. **Null input (`-n`)**: on/off — verified filter receives `null` regardless of input

Error paths tested:
- Missing file: exit code 2, stderr contains file-open error
- Invalid JSON (without `-R`): nonzero exit, stderr contains "parse error"
- Invalid JSON with `-R`: exit code 0, content treated as raw string (no parse error)

## Frame-to-Test Traceability

| Frame | Pytest Test | Outcome |
| --- | --- | --- |
| F01 | `test_file_valid_json_default` | Pass |
| F02 | `test_stdin_valid_json_default` | Pass |
| F03 | `test_file_multi_json_default` | Pass |
| F04 | `test_stdin_multi_json_default` | Pass |
| F05 | `test_file_plain_text_raw_input` | Pass |
| F06 | `test_stdin_plain_text_raw_input` | Pass |
| F07 | `test_file_valid_json_slurp` | Pass |
| F08 | `test_stdin_multi_json_slurp` | Pass |
| F09 | `test_file_plain_text_raw_slurp` | Pass |
| F10 | `test_stdin_valid_json_raw_slurp` | Pass |
| F11 | `test_file_null_input` | Pass |
| F12 | `test_stdin_null_input_empty` | Pass |
| F13 | `test_file_missing_error` | Pass |
| F14 | `test_file_invalid_json_parse_error` | Pass |
| F15 | `test_stdin_invalid_json_parse_error` | Pass |
| F16 | `test_file_invalid_json_raw_input_bypasses_parse` | Pass |
| F17 | `test_file_empty_default` | Pass |
| F18 | `test_file_empty_slurp` | Pass |

## Bugs Found

No bugs were found in jq-1.6 for the input modes and file ingestion behaviors tested.

## Observations and Conclusions

1. **File vs stdin equivalence**: jq produces identical output for the same content whether read from a file or piped via stdin, confirming input source transparency.
2. **`-R` as parse error bypass**: the `-R` flag reliably prevents JSON parse errors by treating all input as raw strings, even for malformed JSON (F16).
3. **`-R -s` combination**: correctly concatenates all input lines (including newlines) into a single JSON string value, as documented.
4. **`-n` independence**: null-input mode correctly ignores all input content and source, outputting `null` regardless.
5. **Empty file handling**: jq produces no output (exit 0) in default mode and `[]` with `-s`, both consistent with documented behavior.
6. **Error exit codes**: missing file consistently returns exit code 2; invalid JSON returns exit code 4 in jq-1.6 (documented as nonzero for portability).
