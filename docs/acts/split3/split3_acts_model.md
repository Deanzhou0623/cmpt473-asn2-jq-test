# Split 3 ACTS Model (Pairwise)

Use this model in ACTS (strength = 2, i.e., pairwise).

## Parameters

| Name | Type | Values |
| --- | --- | --- |
| `input_file_state` | enum | `valid`, `invalid_json`, `empty`, `missing`, `no_read_permission` |
| `filter_kind` | enum | `dot`, `invalid_program`, `field_a`, `field_b`, `field_c`, `field_missing`, `empty_filter` |
| `exit_status_flag` | enum | `off`, `on` |

## Constraints (Model-Level)

Enter these constraints in ACTS (adjust operator syntax if your ACTS build requires it):

1. `(input_file_state != valid) => (filter_kind = dot)`
2. `(input_file_state != valid) => (exit_status_flag = off)`
3. `(filter_kind = invalid_program) => (input_file_state = valid)`
4. `(filter_kind = field_a OR filter_kind = field_b OR filter_kind = field_c OR filter_kind = field_missing OR filter_kind = empty_filter) => (input_file_state = valid AND exit_status_flag = on)`

## Mapping to Concrete CLI

- `input_file_state=valid` -> `tests/split3/fixtures/valid.json`
- `input_file_state=invalid_json` -> `tests/split3/fixtures/invalid.json`
- `input_file_state=empty` -> `tests/split3/fixtures/empty.json`
- `input_file_state=missing` -> `tests/split3/fixtures/does_not_exist.json`
- `input_file_state=no_read_permission` -> temp file + `chmod 000` in test

- `filter_kind=dot` -> `.`
- `filter_kind=invalid_program` -> `.[ `
- `filter_kind=field_a` -> `.a`
- `filter_kind=field_b` -> `.b`
- `filter_kind=field_c` -> `.c`
- `filter_kind=field_missing` -> `.missing`
- `filter_kind=empty_filter` -> `empty`

- `exit_status_flag=off` -> no `-e`
- `exit_status_flag=on` -> include `-e`

## Expected Exit-Code Classes

- Compile error -> `3`
- Missing/permission file errors -> `2`
- With `-e`: truthy -> `0`, `false/null` -> `1`, no output -> `4`
- Parse errors -> nonzero (value may vary by jq build)

## Generated Frame Set

- Pairwise frame set used by this repo is recorded in `docs/acts/split3/split3_pairwise_frames.csv`.
