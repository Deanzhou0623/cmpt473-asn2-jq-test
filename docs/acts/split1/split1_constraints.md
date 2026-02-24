# Split 1 Constraints

## C1: Missing file requires file source

`input_content = missing_file => input_source = file`

**Rationale:** A "missing file" error can only occur when jq is given a file path argument. When reading from stdin, there is no file to be missing. This constraint isolates file-open error behavior.

## C2: Null input disables raw-input and slurp

`null_input = on => raw_input = off AND slurp = off`

**Rationale:** The `-n` flag causes jq to ignore all input and supply `null` to the filter. When `-n` is active, `-R` (raw-input) and `-s` (slurp) have no effect because no input is read. Combining them would not exercise any additional behavior and would create misleading test frames.

## C3: Null input restricts content choices

`null_input = on => input_content in {valid_json, empty}`

**Rationale:** Since `-n` ignores input entirely, the actual content type is irrelevant to the output. Restricting to `valid_json` and `empty` avoids generating frames where, for example, invalid JSON is present but never read — which would not test any meaningful behavior.

## C4: Missing file isolates error path

`input_content = missing_file => raw_input = off AND slurp = off AND null_input = off`

**Rationale:** When the file does not exist, jq fails immediately with a file-open error (exit code 2) before any input processing flags take effect. Testing `-R`, `-s`, or `-n` with a missing file would not exercise those flags and would conflate error sources.

## C5: Invalid JSON parse error expectation

`input_content = invalid_json AND raw_input = off => parse error expected`

**Rationale:** The `-R` flag bypasses JSON parsing by treating input as raw strings. Without `-R`, invalid JSON triggers a parse error. This constraint clarifies when parse errors are expected vs when `-R` prevents them.
