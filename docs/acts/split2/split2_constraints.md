# Split 2 Category-Partition Constraints

This file mirrors the constraints in `docs/spec/split2.md` and the Split 2 ACTS model.

## Categories

- `output_mode` = {`default`, `compact`, `raw`, `join`, `raw0`}
- `output_type` = {`string`, `number`, `object`, `array`, `bool`, `null`}
- `string_content_class` = {`plain`, `quote_backslash`, `unicode`, `embedded_newline`, `not_applicable`}
- `result_cardinality` = {`single`, `multiple`}

## Constraints

- C1: `string_content_class != not_applicable => output_type = string`
- C2: `output_type != string => string_content_class = not_applicable`
- C3: `output_type = string => string_content_class != not_applicable`
- C4: `output_mode in {raw, join, raw0} => output_type = string`
- C5: `output_mode = raw0 => output_type = string`

## Oracle Dimensions

Each concrete test generated from these frames asserts:

- exact `stdout` bytes,
- return code class (`0` vs nonzero),
- stderr class (typically empty for valid Split 2 cases).
