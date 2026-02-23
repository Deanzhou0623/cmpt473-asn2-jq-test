# Split 3 Spec (Error Handling + `-e` Exit Status)

## Component Under Test

`jq` command-line invocation behavior for:

- Parse/runtime errors from malformed or unreadable input files.
- Compile-time errors from invalid filter syntax.
- Exit-status semantics with `-e` / `--exit-status`.

## Scope

This split covers the following scenarios:

1. Invalid JSON input (`invalid.json`).
2. Empty input file (`empty.json`) behavior (parse failure on some jq builds, no-input on others).
3. Invalid jq filter syntax.
4. Missing input file path.
5. Permission denied when reading input file.
6. `-e` behavior on:
   - truthy output (`.a`)
   - missing field (`.missing`)
   - `false` (`.c`)
   - `null` (`.b`)
   - no output (`empty`)

## Exit-Code Rules (Spec Paragraph)

For this split, the oracle treats jq status codes as:

- `0`: successful execution, and with `-e` the last result is neither `false` nor `null`.
- `1`: with `-e`, the last result is `false` or `null`.
- `2`: usage/system errors (including file-open errors such as missing file and permission denied).
- `3`: jq filter compile errors.
- `4`: with `-e`, no valid result was ever produced (for example, filter `empty`).

Notes on parse errors: jq builds may use other nonzero codes for parse failures (observed `5` on jq-1.7.1-apple for malformed JSON), so parse-error tests assert nonzero + stderr pattern instead of a single numeric code.

## Category-Partition Model

### Parameters / Categories

| Category | Choices |
| --- | --- |
| `input_file_state` | `valid`, `invalid_json`, `empty`, `missing`, `no_read_permission` |
| `filter_kind` | `dot`, `invalid_program`, `field_a`, `field_b`, `field_c`, `field_missing`, `empty_filter` |
| `exit_status_flag` | `off`, `on` |

### Constraints

| ID | Constraint | Rationale |
| --- | --- | --- |
| C1 | `input_file_state != valid => filter_kind = dot` | File-error and parse-error cases isolate file/input behavior without filter interaction noise. |
| C2 | `input_file_state != valid => exit_status_flag = off` | `-e` semantics are only meaningful when jq can read valid input and run a filter. |
| C3 | `filter_kind = invalid_program => input_file_state = valid` | Compile errors are modeled independently of file-open/parse failures. |
| C4 | `filter_kind in {field_a, field_b, field_c, field_missing, empty_filter} => input_file_state = valid and exit_status_flag = on` | These choices specifically target `-e` exit-status behavior. |

## Oracle Model

Each test asserts all three outputs:

- Process return code.
- `stderr` contains expected error pattern (for failures), using regex/pattern matching.
- `stdout` empty vs non-empty based on scenario.

Pattern-based assertions are used instead of exact error-text equality because jq wording may vary by OS/version.

## References

- jq manual (official): https://jqlang.org/manual/
- jq invocation/options (`-e`, `--exit-status`): https://jqlang.org/manual/#invoking-jq

## Notes

- This split intentionally focuses on failure modes and status signaling, not transformation correctness.
- Deterministic local fixtures are used; tests avoid network and timing dependencies.
