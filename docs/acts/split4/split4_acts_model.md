# Split 4 ACTS Model (Pairwise)

Use this model in ACTS with strength = 2 (pairwise).

## Parameters

| Name | Type | Values |
| --- | --- | --- |
| `filter` | enum | `select`, `map`, `sort`, `group_by`, `unique`, `add`, `length` |
| `input_type` | enum | `num_array`, `obj_array`, `mixed_array`, `empty_array`, `string`, `object`, `null` |
| `input_state` | enum | `normal`, `unsorted`, `duplicates`, `missing_keys` |

## Constraints (Model-Level)

| ID | Constraint | Rationale |
| --- | --- | --- |
| C1 | `(filter = sort \|\| filter = unique \|\| filter = group_by) => (input_type = num_array \|\| input_type = obj_array \|\| input_type = mixed_array \|\| input_type = empty_array)` | These filters operate on arrays only |
| C2 | `(filter = select \|\| filter = map) => (input_type = num_array \|\| input_type = obj_array \|\| input_type = mixed_array \|\| input_type = empty_array)` | `select` and `map` iterate over array elements |
| C3 | `filter = add => (input_type = num_array \|\| input_type = obj_array \|\| input_type = mixed_array \|\| input_type = empty_array)` | `add` reduces arrays; scalar input is out of scope |
| C4 | `filter = length => (input_type = num_array \|\| input_type = obj_array \|\| input_type = mixed_array \|\| input_type = empty_array \|\| input_type = string \|\| input_type = object \|\| input_type = null)` | `length` is defined for arrays, strings, objects, and null |
| C5 | `input_state = missing_keys => input_type = obj_array` | Missing-key behavior only applies to object arrays |
| C6 | `(input_state = unsorted \|\| input_state = duplicates) => (input_type = num_array \|\| input_type = obj_array \|\| input_type = mixed_array)` | Ordering/dedup states only apply to non-empty arrays |
| C7 | `(input_type = string \|\| input_type = object \|\| input_type = null \|\| input_type = empty_array) => input_state = normal` | Scalar and empty types have no meaningful ordering or duplicate state |

## Mapping to Concrete CLI / Fixtures

| Parameter Value | CLI / Fixture |
| --- | --- |
| `filter=select` | `map(select(. > 1))` or `map(select(.id == 1))` |
| `filter=map` | `map(.id)` or `map(type)` |
| `filter=sort` | `sort` |
| `filter=group_by` | `group_by(.)` or `group_by(.id)` |
| `filter=unique` | `unique` |
| `filter=add` | `add` |
| `filter=length` | `length` |
| `input_type=num_array` | `tests/split4/fixtures/numbers.json` — `[3, 1, 2, 2]` |
| `input_type=obj_array` | `tests/split4/fixtures/objects.json` — `[{"id":1},{"id":2},{"id":1},{"other":3}]` |
| `input_type=mixed_array` | `tests/split4/fixtures/mixed.json` — `[1, "a", 1, null]` |
| `input_type=empty_array` | `tests/split4/fixtures/empty.json` — `[]` |
| `input_type=string` | `tests/split4/fixtures/string.json` — `"hello"` |
| `input_type=object` | `tests/split4/fixtures/object_simple.json` — `{"a":1,"b":2}` |
| `input_type=null` | `tests/split4/fixtures/null.json` — `null` |
| `input_state=normal` | data as-is |
| `input_state=unsorted` | array in non-sorted order |
| `input_state=duplicates` | array contains duplicate values |
| `input_state=missing_keys` | object array where some objects lack the accessed key |

## ACTS Generation

- **ACTS input file:** `docs/acts/split4/split4_acts_input.txt`
- **ACTS jar:** `__MACOSX/ACTS3.0/acts_3.0.jar`
- **Generation command:**
  ```
  java -Dalgo=ipog -Ddoi=2 -Doutput=csv -Dmode=scratch -Dchandler=forbiddentuples -Dcheck=on \
       -jar __MACOSX/ACTS3.0/acts_3.0.jar \
       docs/acts/split4/split4_acts_input.txt \
       docs/acts/split4/split4_pairwise_frames.csv
  ```
- **Frames generated:** 34
- **Coverage:** 2-way pairwise, verified by ACTS

## Generated Frame Set

See `docs/acts/split4/split4_pairwise_frames.csv` for the complete ACTS-generated pairwise frame set.
