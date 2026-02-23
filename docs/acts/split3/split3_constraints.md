# Split 3 Category-Partition Constraints

This file mirrors the constraints used in `docs/spec/split3.md` and the ACTS model.

## Categories

- `input_file_state` = {`valid`, `invalid_json`, `empty`, `missing`, `no_read_permission`}
- `filter_kind` = {`dot`, `invalid_program`, `field_a`, `field_b`, `field_c`, `field_missing`, `empty_filter`}
- `exit_status_flag` = {`off`, `on`}

## Constraints

- C1: `input_file_state != valid => filter_kind = dot`
- C2: `input_file_state != valid => exit_status_flag = off`
- C3: `filter_kind = invalid_program => input_file_state = valid`
- C4: `filter_kind in {field_a, field_b, field_c, field_missing, empty_filter} => input_file_state = valid and exit_status_flag = on`

## Expected Oracle Dimensions

Each concrete test generated from these frames must assert:

- return code class (`0`, `1`, or other nonzero)
- stderr pattern (regex/contains)
- stdout emptiness (empty/non-empty)
