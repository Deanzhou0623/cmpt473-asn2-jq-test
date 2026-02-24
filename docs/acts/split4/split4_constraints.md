# Split 4 Category-Partition Constraints

This file documents the logical constraints applied to the input space to ensure only meaningful and valid test frames are generated.

## Constraints

| ID | Constraint | Rationale |
| --- | --- | --- |
| C1 | `(filter = sort \|\| filter = unique \|\| filter = group_by) => input_type is array` | `sort`, `unique`, and `group_by` require an array as input; applying them to scalars or null is undefined in scope |
| C2 | `(filter = select \|\| filter = map) => input_type is array` | `select` and `map` iterate over array elements; scalar inputs are out of scope for this split |
| C3 | `filter = add => input_type is array` | `add` reduces an array to a single value; scalar reduction is out of scope |
| C4 | `filter = length => input_type in {array, string, object, null}` | `length` is well-defined for these types; numeric scalar length is excluded |
| C5 | `input_state = missing_keys => input_type = obj_array` | The missing-key property only applies to arrays of objects where a field access returns null for some elements |
| C6 | `(input_state = unsorted \|\| input_state = duplicates) => input_type in {num_array, obj_array, mixed_array}` | Ordering and duplicate states only apply to non-empty arrays; empty arrays have no meaningful ordering |
| C7 | `(input_type = string \|\| input_type = object \|\| input_type = null \|\| input_type = empty_array) => input_state = normal` | Scalar types, null, and empty arrays have no ordering or duplicate state; only `normal` applies |

## ACTS Input File

The constraints above are encoded in `docs/acts/split4/split4_acts_input.txt` in ACTS 3.0 syntax and were used to generate `docs/acts/split4/split4_pairwise_frames.csv` (34 pairwise frames).
