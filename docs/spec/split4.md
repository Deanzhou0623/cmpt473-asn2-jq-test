# Split 4 Spec (Transform/Computation Filters)

## Component Under Test

`jq` transformation filters and aggregations:

- `select(boolean_expression)`
- `map(filter)`
- `sort`
- `group_by(filter)`
- `unique`
- `add`
- `length`

## Scope

This split exercises how the above filters behave on representative input shapes and data properties:

1. Filtering arrays of numbers and objects with missing keys (`select`).
2. Mapping over arrays to extract fields or compute derived values (`map`).
3. Ordering arrays that may be unsorted or empty (`sort`).
4. Grouping unsorted arrays of numbers or objects by key (`group_by`).
5. Deduplicating sorted/unsorted arrays containing duplicates and mixed types (`unique`).
6. Reducing arrays of numbers and empty arrays (`add`).
7. Measuring length of strings, objects, arrays, and the edge case `null` (`length`).

## Behavior Rules (Spec Paragraph)

- `select`: Emits only elements where the predicate is truthy; when wrapped in `map`, preserves array shape for passing items.
- `map`: Applies the filter to each element; missing object keys evaluate to `null`.
- `sort`: Produces a globally sorted array using jq's default ordering rules.
- `group_by`: Requires sortable keys; jq sorts first, then groups consecutive equal keys into subarrays.
- `unique`: Sorts then removes duplicates, returning a sorted, deduped array.
- `add`: Reduces an array—sums numbers; concatenates strings; merges arrays/objects; `[]` yields `null`.
- `length`: Returns count for arrays, character count for strings, and key count for objects; jq ≥1.6 returns `0` for `null` (older builds may raise an error—tests accept either rc=0 with 0 or an error message).

## Category-Partition Model

### Parameters / Categories

| Category | Choices |
| --- | --- |
| `filter_type` | `select`, `map`, `sort`, `group_by`, `unique`, `add`, `length` |
| `input_data_type` | `array_numeric`, `array_object`, `array_mixed`, `array_empty`, `scalar_string`, `scalar_number`, `object_simple`, `null` |
| `data_property` | `sorted`, `unsorted`, `has_duplicates`, `missing_keys` |

### Constraints

| ID | Constraint | Rationale |
| --- | --- | --- |
| C1 | `filter_type in {sort, group_by, unique, add, map, select} => input_data_type` is an array variant (or `object_simple` for field extraction). | These filters operate on streams/arrays; scalar inputs are out of scope for these cases. |
| C2 | `filter_type in {sort, group_by, unique} => data_property in {sorted, unsorted, has_duplicates}` | Ordering and dedup behavior only matter for arrays. |
| C3 | `data_property = missing_keys => input_data_type in {array_object, object_simple}` | Missing-key behavior applies to objects. |
| C4 | `filter_type = length => input_data_type in {array_numeric, array_object, array_mixed, array_empty, scalar_string, object_simple, null}` | Length is defined for arrays/strings/objects and the `null` edge case; numeric scalar length is excluded. |
| C5 | `filter_type = add => input_data_type in {array_numeric, array_object, array_mixed, array_empty}` | `add` reduces arrays; scalars are not reduced in this split. |

## Oracle Model

Each test asserts:

- Process return code (`0` for successful transforms; `length(null)` tolerates either `0` with result `0` or a version-specific error).
- `stdout` parsed with `json.loads` for structural equality of results (ordering asserted where jq guarantees it, e.g., `sort`, `group_by`, `unique`).
- `stderr` expected to be empty for successful transforms; only `length(null)` allows version-specific error text.

## References

- jq manual (core filters): https://jqlang.org/manual/
- Sorting, grouping, uniqueness semantics: https://jqlang.org/manual/#sorting-arrays
- Reduction and length: https://jqlang.org/manual/#addition
- Selection and mapping: https://jqlang.org/manual/#conditionals-and-comparisons

## Notes

- Pairwise frames are generated with ACTS (`docs/acts/split4/split4_pairwise_frames.csv`) from the category model above.
- Mixed-type ordering and `length(null)` behaviors vary slightly by jq version; tests accept documented variants.
