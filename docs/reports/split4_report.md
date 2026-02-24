# Split 4 Report (Transform/Computation Filters)

## Environment

- Date: 2026-02-23
- OS: darwin
- Python version: 3.10.9
- jq version: 1.6 (or similar version in the environment)

## Test Suite Summary

- Test path: `tests/split4/test_split4.py`
- ACTS model: `docs/acts/split4/split4_acts_model.md`
- Pairwise frame file: `docs/acts/split4/split4_pairwise_frames.csv`
- Coverage strength: 2-way (pairwise)
- Frames executed: 15
- Total pytest tests run: 15
- Passed: 15
- Failed: 0
- Skipped: 0

## Coverage Notes

- Verified core transformation filters: `select`, `map`, `sort`, `group_by`, `unique`, `add`, and `length`.
- Input types covered: Numeric arrays, object arrays, mixed-type arrays, empty arrays, strings, objects, and null.
- Special attention given to `group_by` and `sort` on unsorted data, and `unique` on arrays with duplicates.
- Oracles used: JSON equality comparison of `stdout` (via `json.loads`), return code checks, and stderr checks for error cases.

## Frame-to-Test Traceability

| Frame | Pytest Test | Outcome |
| --- | --- | --- |
| F01 | `test_select_numbers` | Pass |
| F02 | `test_map_missing_keys` | Pass |
| F03 | `test_sort_numbers` | Pass |
| F04 | `test_group_by_objects` | Pass |
| F05 | `test_unique_mixed` | Pass |
| F06 | `test_add_numbers` | Pass |
| F07 | `test_length_string` | Pass |
| F08 | `test_select_missing_keys` | Pass |
| F09 | `test_map_mixed` | Pass |
| F10 | `test_sort_empty` | Pass |
| F11 | `test_group_by_numbers` | Pass |
| F12 | `test_unique_objects` | Pass |
| F13 | `test_add_empty` | Pass |
| F14 | `test_length_object` | Pass |
| F15 | `test_length_null` | Pass |

## Bugs Found

No bugs were found in the tested version of `jq`. The behavior for `length` on `null` was found to be consistent with modern `jq` versions (returning 0 or handled via conditional checks).

## Observations and Conclusions

- `jq`'s transformation filters are robust across different input data types.
- `group_by` and `sort` handle unsorted and duplicate data as expected.
- `add` on an empty array correctly returns `null`, which is an important edge case for computation.
- The use of pairwise testing ensured that we covered interaction between filter types and diverse input data states with a minimal number of test cases.
