# Split 4 ACTS Model

## Parameters

| Name | Type | Values |
| --- | --- | --- |
| `filter` | enum | `select`, `map`, `sort`, `group_by`, `unique`, `add`, `length` |
| `input_type` | enum | `num_array`, `obj_array`, `mixed_array`, `empty_array`, `string`, `object`, `null` |
| `input_state` | enum | `sorted`, `unsorted`, `duplicates`, `missing_keys`, `normal` |

## Constraints

1. `(filter == "sort" || filter == "unique" || filter == "group_by") => (input_type == "num_array" || input_type == "obj_array" || input_type == "mixed_array" || input_type == "empty_array")`
2. `(input_state == "missing_keys") => (input_type == "obj_array")`
3. `(input_state == "sorted" || input_state == "unsorted" || input_state == "duplicates") => (input_type == "num_array" || input_type == "obj_array" || input_type == "mixed_array")`
4. `(filter == "add") => (input_type == "num_array" || input_type == "obj_array" || input_type == "mixed_array" || input_type == "empty_array")` (add usually expects an array to sum)
5. `(filter == "length") => (input_type == "num_array" || input_type == "obj_array" || input_type == "mixed_array" || input_type == "empty_array" || input_type == "string" || input_type == "object")`
6. `(input_type == "null" || input_type == "empty_array") => (input_state == "normal")`

## Mapping to Concrete CLI / Fixtures

- `filter=select` -> `select(.id > 1)` or `select(. > 1)`
- `filter=map` -> `map(. + 1)` or `map(.id)`
- `filter=sort` -> `sort`
- `filter=group_by` -> `group_by(.id)` or `group_by(.)`
- `filter=unique` -> `unique`
- `filter=add` -> `add`
- `filter=length` -> `length`

- `input_type=num_array` + `input_state=sorted` -> `[1, 2, 3]`
- `input_type=num_array` + `input_state=unsorted` -> `[3, 1, 2]`
- `input_type=num_array` + `input_state=duplicates` -> `[1, 2, 2, 3]`
- `input_type=obj_array` + `input_state=missing_keys` -> `[{"id":1}, {"other":2}]`
- ... etc.
