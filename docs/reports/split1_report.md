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
- Frames executed: 11
- Total pytest tests run: 11
- Passed: 11, Failed: 0, Skipped: 0

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

All frames in `docs/acts/split1/split1_pairwise_frames.csv` are executed
by the single parameterized test `test_split1_frame` in
`tests/split1/test_split1.py`. Each CSV row encodes:

- the ACTS-derived parameter values (`input_source`, `input_content`, `raw_input`, `slurp`, `null_input`),
- the expected return-code class (`expect_rc`),
- the expected stdout classification (`expect_stdout`),
- and the expected stderr pattern (`expect_stderr_pattern`).

Pytest parametrization uses the `frame_id` column (F01–F11) for readable
test IDs in the output.

## Bugs Found

No bugs were found in jq-1.6 for the input modes and file ingestion behaviors tested.

## Observations and Conclusions

1. **File vs stdin equivalence**: jq produces identical output for the same content whether read from a file or piped via stdin, confirming input source transparency.
2. **`-R` as parse error bypass**: the `-R` flag reliably prevents JSON parse errors by treating all input as raw strings, even for malformed JSON (F16).
3. **`-R -s` combination**: correctly concatenates all input lines (including newlines) into a single JSON string value, as documented.
4. **`-n` independence**: null-input mode correctly ignores all input content and source, outputting `null` regardless.
5. **Empty file handling**: jq produces no output (exit 0) in default mode and `[]` with `-s`, both consistent with documented behavior.
6. **Error exit codes**: missing file consistently returns exit code 2; invalid JSON returns exit code 4 in jq-1.6 (documented as nonzero for portability).
