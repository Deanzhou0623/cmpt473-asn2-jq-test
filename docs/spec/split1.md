# Split 1 Spec (Input Modes & File Ingestion)

## Component Under Test

`jq` command-line input reading behavior, covering:

- File path argument vs stdin (`-`) as input source
- `-R` / `--raw-input`: read each line as a raw string instead of parsing JSON
- `-s` / `--slurp`: read all inputs into a single array (or single string with `-R`)
- `-n` / `--null-input`: run filter with `null` as input, ignoring any input stream

## Scope

1. Reading valid JSON from a file vs stdin — identical output expected
2. Reading multiple JSON values from a single input (newline-separated)
3. Raw input mode (`-R`): each input line becomes a JSON string
4. Slurp mode (`-s`): all JSON values collected into one array
5. Combined `-R -s`: all lines concatenated into one string
6. Null input (`-n`): filter receives `null`, input stream is ignored
7. Error: missing file path — nonzero exit + stderr message
8. Error: invalid JSON without `-R` — parse error + nonzero exit
9. Empty file behavior across modes

## Behavior Rules (Spec Paragraph)

Per the jq manual ("Invoking jq" and option descriptions):

- **Default mode**: jq reads JSON values from the input (file or stdin), applies the filter to each value independently, and outputs results separated by newlines.
- **`-R` (raw-input)**: each line of input is treated as a JSON string (no JSON parsing). Lines are fed to the filter one at a time.
- **`-s` (slurp)**: all input JSON values are read into a single array, which is then passed to the filter as one value.
- **`-R -s` combined**: all input lines are concatenated (with newlines) into a single JSON string, passed to the filter.
- **`-n` (null-input)**: the filter receives `null` as its input; no input is read from files or stdin.
- **File errors**: if a named file cannot be opened, jq prints an error to stderr and exits with code `2`.
- **Parse errors**: if input is not valid JSON (and `-R` is not used), jq prints a parse error to stderr and exits with a nonzero code.
- **Empty file**: produces no output in default mode (exit `0`); with `-s` produces `[]`.

## Category-Partition Model

### Parameters / Categories

| Category | Choices |
| --- | --- |
| `input_source` | `file`, `stdin` |
| `input_content` | `valid_json`, `multi_json`, `plain_text`, `empty`, `invalid_json`, `missing_file` |
| `raw_input` (`-R`) | `off`, `on` |
| `slurp` (`-s`) | `off`, `on` |
| `null_input` (`-n`) | `off`, `on` |

### Constraints

| ID | Constraint | Rationale |
| --- | --- | --- |
| C1 | `input_content = missing_file => input_source = file` | stdin cannot be "missing" |
| C2 | `null_input = on => raw_input = off AND slurp = off` | `-n` ignores input entirely, so `-R`/`-s` are irrelevant |
| C3 | `null_input = on => input_content in {valid_json, empty}` | with `-n` input content is ignored; restrict to avoid noise |
| C4 | `input_content = missing_file => raw_input = off AND slurp = off AND null_input = off` | isolate file-open error from flag interactions |
| C5 | `input_content = invalid_json AND raw_input = off => expect parse error` | `-R` bypasses JSON parsing, so errors only occur without it |

## Oracle Model

Each test asserts:

- **Return code**: `0` for success, `2` for file-open error, nonzero for parse errors
- **stdout**: expected content (JSON structure, raw strings, empty, or `null`)
- **stderr**: empty on success; contains error pattern on failure

## References

- jq manual: <https://jqlang.github.io/jq/manual/v1.6/>
- Options: `-R`, `-s`, `-n`, file/stdin behavior under "Invoking jq"

## Notes

- Tested against jq-1.6 on macOS (Darwin).
- Empty file in default mode produces no output and exit `0`.
- Invalid JSON exit code is `4` in jq-1.6 (may vary across versions).
