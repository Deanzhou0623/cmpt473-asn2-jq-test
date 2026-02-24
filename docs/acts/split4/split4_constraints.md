# Split 4 Category-Partition Constraints

This file summarizes the logical constraints applied to the input space to ensure meaningful and valid test frames.

## Constraints

- **C1 (Array dependency)**: Filters like `sort`, `unique`, and `group_by` require array inputs.
- **C2 (Key relevance)**: The `missing_keys` state only applies to arrays of objects or single objects where we are attempting to access a specific field.
- **C3 (Ordering relevance)**: `sorted` and `unsorted` states are primarily used to verify the stability and correctness of `sort` and `group_by` operations on arrays.
- **C4 (Additive compatibility)**: `add` is tested primarily with arrays (numbers, objects to merge, or strings to concatenate).
- **C5 (Length compatibility)**: `length` is not valid for `null` or raw numbers in many `jq` contexts, so we focus on types with a measurable "length" (arrays, objects, strings).
