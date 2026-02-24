# Split 2 ACTS Model (Pairwise)

Use this model in ACTS with strength = 2 (pairwise).

## Parameters

| Name | Type | Values |
| --- | --- | --- |
| `output_mode` | enum | `default`, `compact`, `raw`, `join`, `raw0` |
| `output_type` | enum | `string`, `number`, `object`, `array`, `bool`, `null` |
| `string_content_class` | enum | `plain`, `quote_backslash`, `unicode`, `embedded_newline`, `not_applicable` |
| `result_cardinality` | enum | `single`, `multiple` |

## Constraints (Model-Level)

Enter these constraints in ACTS (adjust syntax if your ACTS build requires it):

1. `(string_content_class != not_applicable) => (output_type = string)`
2. `(output_type = string) => (string_content_class != not_applicable)`
3. `(output_mode = raw OR output_mode = join OR output_mode = raw0) => (output_type = string)`

## Mapping to Concrete jq Invocations

- `output_mode=default` -> no formatting flag
- `output_mode=compact` -> `-c`
- `output_mode=raw` -> `-r`
- `output_mode=join` -> `-j`
- `output_mode=raw0` -> `--raw-output0`

`output_type`, `string_content_class`, and `result_cardinality` map to deterministic filters and input fixtures in `tests/split2/test_split2.py`.

## Expected Oracle Dimensions

Each generated test frame asserts:

- exact `stdout` bytes (including separators),
- `stderr` class (empty/non-empty),
- return code class.

## Generated Frame Set

- Pairwise frame set for this split is recorded in `docs/acts/split2/split2_pairwise_frames.csv`.
