# Split 3 Spec (Error Handling + `-e` Exit Status)

## Scope Summary

Split 3 focuses on:

- Runtime error handling behavior (invalid JSON, invalid filter, missing file).
- `jq -e` / `--exit-status` semantics for truthy vs falsy/null results.
- Capturing and asserting exit code + stderr patterns in automated tests.

## Required References

- `jq` manual: `-e` / `--exit-status` behavior.
- `jq` manual: error reporting/diagnostics behavior for parsing and compilation failures.

Reference links:

- https://jqlang.org/manual/
- https://jqlang.org/manual/#invoking-jq
