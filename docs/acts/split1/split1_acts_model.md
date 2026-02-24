# Split 1 ACTS Model (Pairwise)

## Parameters

| Name | Type | Values |
| --- | --- | --- |
| `input_source` | enum | `file`, `stdin` |
| `input_content` | enum | `valid_json`, `multi_json`, `plain_text`, `empty`, `invalid_json`, `missing_file` |
| `raw_input` | enum | `off`, `on` |
| `slurp` | enum | `off`, `on` |
| `null_input` | enum | `off`, `on` |

## Constraints (Model-Level)

1. `(input_content = missing_file) => (input_source = file)`
2. `(null_input = on) => (raw_input = off AND slurp = off)`
3. `(null_input = on) => (input_content = valid_json OR input_content = empty)`
4. `(input_content = missing_file) => (raw_input = off AND slurp = off AND null_input = off)`

## Mapping to Concrete CLI

- `input_source = file` -> pass fixture file path as argument
- `input_source = stdin` -> pass content via `input_text` parameter (pipe to stdin)
- `input_content = valid_json` -> `tests/split1/fixtures/valid.json`
- `input_content = multi_json` -> `tests/split1/fixtures/multi.json`
- `input_content = plain_text` -> `tests/split1/fixtures/plain.txt`
- `input_content = empty` -> `tests/split1/fixtures/empty.json`
- `input_content = invalid_json` -> `tests/split1/fixtures/invalid.json`
- `input_content = missing_file` -> `tests/split1/fixtures/nonexistent.json`
- `raw_input = off` -> no `-R` flag
- `raw_input = on` -> include `-R`
- `slurp = off` -> no `-s` flag
- `slurp = on` -> include `-s`
- `null_input = off` -> no `-n` flag
- `null_input = on` -> include `-n`

## Expected Output Classes

- **Normal JSON**: parsed and output with default formatting, rc=0
- **Multi-JSON**: each value output separately, rc=0
- **Raw input (`-R`)**: each line as a quoted JSON string, rc=0
- **Slurp (`-s`)**: all values in one array, rc=0
- **Raw + Slurp (`-R -s`)**: all lines as one concatenated string, rc=0
- **Null input (`-n`)**: `null` output, rc=0
- **Missing file**: rc=2, stderr contains "Could not open" or "No such file"
- **Parse error** (invalid JSON without `-R`): rc=nonzero, stderr contains "parse error"
- **Empty file**: no output (default), `[]` (with `-s`), no output (with `-R`)

## Generated Frame Set

See `split1_pairwise_frames.csv` for the complete set of pairwise-generated test frames.
