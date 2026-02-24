# Split 4 Category-Partition Constraints

This file documents the logical constraints applied to the input space to ensure only meaningful and valid test frames are generated.

## Constraints

| ID | Constraint | Rationale |
| --- | --- | --- |
| C1 | `(filter_type = sort \|\| filter_type = group_by \|\| filter_type = unique \|\| filter_type = add \|\| filter_type = map \|\| filter_type = select) => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed \|\| input_data_type = array_empty \|\| input_data_type = object_simple)` | These filters operate on arrays or object_simple; scalars and null are out of scope |
| C2 | `(filter_type = sort \|\| filter_type = group_by \|\| filter_type = unique) => (data_property = sorted \|\| data_property = unsorted \|\| data_property = has_duplicates)` | Ordering and dedup behavior is only defined for sortable data |
| C3 | `data_property = missing_keys => (input_data_type = array_object \|\| input_data_type = object_simple)` | Missing-key behavior applies to object arrays or simple objects |
| C4 | `filter_type = length => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed \|\| input_data_type = array_empty \|\| input_data_type = scalar_string \|\| input_data_type = object_simple \|\| input_data_type = null)` | `length` is defined for arrays, strings, objects, and null; scalar_number is excluded |
| C5 | `filter_type = add => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed \|\| input_data_type = array_empty)` | `add` reduces arrays; scalar reduction is out of scope |
| C6 | `(data_property = unsorted \|\| data_property = has_duplicates) => (input_data_type = array_numeric \|\| input_data_type = array_object \|\| input_data_type = array_mixed)` | Ordering and duplicate states apply only to non-empty arrays (implicit constraint) |
| C7 | `(input_data_type = scalar_string \|\| input_data_type = scalar_number \|\| input_data_type = null \|\| input_data_type = array_empty) => data_property = sorted` | Scalar types, null, and empty_array have no meaningful ordering or duplicate state (implicit constraint) |

**Note:** C1–C5 are the primary constraints from the spec. C6–C7 are implicit constraints added to prevent nonsensical `data_property` pairings for types that have no ordering or duplicate state.

**Note on `scalar_number`:** This value is listed in the model per spec but is excluded by both C1 (all array/object filters exclude it) and C4 (length excludes it). ACTS generates 0 frames with `scalar_number` because no filter type can validly pair with it.

## ACTS Input File

The constraints above are encoded in `docs/acts/split4/split4_acts_input.txt` in ACTS 3.0 syntax and were used to generate `docs/acts/split4/split4_pairwise_frames.csv` (38 pairwise frames).
