# Split 2 Spec (Output Formatting and Encoding)

## Component Under Test

`jq` command-line output rendering behavior for formatting/encoding options:

- `-c` / `--compact-output`
- `-r` / `--raw-output`
- `-j` / `--join-output`
- `--raw-output0`

The tested component boundary is jq invocation (CLI flags + filter + JSON input) to process outputs
(`stdout`, `stderr`, exit status), focusing on output byte formatting and terminators.

## Scope

This split validates:

1. Compact rendering (`-c`) for JSON values.
2. Raw string rendering (`-r`) without JSON string quoting.
3. Joined output (`-j`) with newline suppression between results.
4. Raw NUL-terminated output (`--raw-output0`) for string results.
5. Escaping/encoding behavior for quotes, backslashes, unicode, and embedded newlines.
6. Type coverage: string, number, object, array, bool, null.

## Input/Output Specification

### Inputs

- **CLI options**: one of `default`, `-c`, `-r`, `-j`, `--raw-output0`.
- **Filter program shape**: filters that produce single or multiple results and selected JSON types.
- **JSON fixture content**:
  - plain strings,
  - strings with quote/backslash escapes,
  - unicode strings,
  - strings containing embedded newline,
  - non-string values (number/object/array/bool/null).
- **Environment**: jq binary version and OS/runtime (captured in report).

### Outputs

- **`stdout` bytes** (primary oracle):
  - exact bytes for quoting/escaping representation,
  - exact record separators (`0x0A` newline vs `0x00` NUL),
  - exact concatenation behavior for multi-result output.
- **`stderr`**:
  - expected empty for valid in-scope formatting cases.
- **exit code**:
  - expected `0` for valid in-scope formatting cases.

## Category-Partition Inputs for Split 2

### Categories

- `output_mode` = `{default, compact, raw, join, raw0}`
- `output_type` = `{string, number, object, array, bool, null}`
- `string_content_class` = `{plain, quote_backslash, unicode, embedded_newline, not_applicable}`
- `result_cardinality` = `{single, multiple}`

### Consistency Constraints

- `string_content_class != not_applicable => output_type = string`
- `output_type = string => string_content_class != not_applicable`
- `output_mode in {raw, join, raw0} => output_type = string`

## Oracle Model

Each generated test frame must assert:

- exact `stdout` bytes,
- stderr class (empty/non-empty),
- return-code class.

## References

- jq manual (invocation/options): https://jqlang.org/manual/
- jq manual option behavior (`-c`, `-r`, `-j`, `--raw-output0`): https://jqlang.org/manual/#invoking-jq
- jq upstream source (implementation rationale):
  - `src/main.c` (option parsing and output-mode control)
  - `src/jv_print.c` (JSON/string rendering and escaping)
