# Split 4 ACTS Model (Pairwise)

Use this model in ACTS with strength = 2 (pairwise).

## Parameters

| Name | Type | Values |
| --- | --- | --- |
| `filter_type` | enum | `select`, `map`, `sort`, `group_by`, `unique`, `add`, `length` |
| `input_data_type` | enum | `array_numeric`, `array_object`, `array_mixed`, `array_empty`, `scalar_string`, `scalar_number`, `object_simple`, `null` |
| `data_property` | enum | `sorted`, `unsorted`, `has_duplicates`, `missing_keys` |

## Constraints (Model-Level)

| ID | Constraint | Rationale |
| --- | --- | --- |
| C1 | `(filter_type = sort \|\| filter_type = group_by \|\| filter_type = unique \|\| filter_type = add \|\| filter_type = map \|\| filter_type = select) => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed \|\| input_data_type = array_empty \|\| input_data_type = object_simple)` | These filters operate on arrays or object_simple; scalars and null are out of scope |
| C2 | `(filter_type = sort \|\| filter_type = group_by \|\| filter_type = unique) => (data_property = sorted \|\| data_property = unsorted \|\| data_property = has_duplicates)` | Ordering/dedup behavior only applies to sortable data |
| C3 | `data_property = missing_keys => (input_data_type = array_object \|\| input_data_type = object_simple)` | Missing-key behavior applies to object arrays or simple objects |
| C4 | `filter_type = length => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed \|\| input_data_type = array_empty \|\| input_data_type = scalar_string \|\| input_data_type = object_simple \|\| input_data_type = null)` | `length` is defined for arrays, strings, objects, and null; scalar_number excluded |
| C5 | `filter_type = add => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed \|\| input_data_type = array_empty)` | `add` reduces arrays; scalar reduction is not in scope |
| C6 | `(data_property = unsorted \|\| data_property = has_duplicates) => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed)` | Ordering/dedup states only apply to non-empty arrays (implicit) |
| C7 | `(input_data_type = scalar_string \|\| input_data_type = scalar_number \|\| input_data_type = null \|\| input_data_type = array_empty) => data_property = sorted` | Scalar types, null, and empty_array have no meaningful ordering or duplicate state (implicit) |

## Mapping to Concrete CLI / Fixtures

| Parameter Value | CLI / Fixture |
| --- | --- |
| `filter_type=select` | `map(select(. > 1))` or `map(select(.id == 1))` |
| `filter_type=map` | `map(.id)` or `map(type)` |
| `filter_type=sort` | `sort` |
| `filter_type=group_by` | `group_by(.)` or `group_by(.id)` |
| `filter_type=unique` | `unique` |
| `filter_type=add` | `add` |
| `filter_type=length` | `length` |
| `input_data_type=array_numeric` | `tests/split4/fixtures/numbers.json` — `[3, 1, 2, 2]` |
| `input_data_type=array_object` | `tests/split4/fixtures/objects.json` — `[{"id":1},{"id":2},{"id":1},{"other":3}]` |
| `input_data_type=array_mixed` | `tests/split4/fixtures/mixed.json` — `[1, "a", 1, null]` |
| `input_data_type=array_empty` | `tests/split4/fixtures/empty.json` — `[]` |
| `input_data_type=scalar_string` | `tests/split4/fixtures/string.json` — `"hello"` |
| `input_data_type=scalar_number` | *(excluded by C1 + C4 — no valid filter pairing)* |
| `input_data_type=object_simple` | `tests/split4/fixtures/object_simple.json` — `{"a":1,"b":2}` |
| `input_data_type=null` | `tests/split4/fixtures/null.json` — `null` |
| `data_property=sorted` | array already in sorted order (or default state for scalars/null) |
| `data_property=unsorted` | array in non-sorted order |
| `data_property=has_duplicates` | array contains duplicate values |
| `data_property=missing_keys` | object array where some objects lack the accessed key |

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
- **Frames generated:** 38
- **Coverage:** 2-way pairwise, verified by ACTS

## Generated Frame Set

See `docs/acts/split4/split4_pairwise_frames.csv` for the complete ACTS-generated pairwise frame set.
