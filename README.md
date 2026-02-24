# CMPT 473 Assignment 2 — jq Functional Testing

This repository contains a complete functional test suite for [`jq`](https://jqlang.github.io/jq/), the lightweight command-line JSON processor. The project applies **Input Space Partitioning** and **Combinatorial Test Frame Generation (ACTS, 2-way pairwise)** across four independently scoped test splits.

---

## Program Under Test

- **Program:** `jq` — a command-line JSON processor
- **Specification:** [jq Manual](https://jqlang.github.io/jq/manual/)
- **Tested versions:** jq-1.6, jq-1.7.1-apple, jq-1.8.1 (results cross-validated across platforms)

---

## Team Contributions

| Split | Owner | GitHub | Scope |
|-------|-------|--------|-------|
| Split 1 | Jeffrey Wang | `jeffrey` | Input modes & file ingestion (`-R`, `-s`, `-n`, file vs stdin) |
| Split 2 | Tommy Duong (`tda49`) | `tommy` | Output formatting & encoding (`-c`, `-r`, `-j`, `--raw-output0`) |
| Split 3 | Dean Zhou (`dza68`) | `dean` | Error handling & exit status (`-e`, parse errors, missing file, permission denied) |
| Split 4 | Ronny Rok | `ronney` | Transform/computation filters (`select`, `map`, `sort`, `group_by`, `unique`, `add`, `length`) |

---

## Repository Layout

```
.
├── docs/
│   ├── acts/
│   │   ├── split1/          # Jeffrey: ACTS model, constraints, pairwise frames (18 frames)
│   │   ├── split2/          # Tommy:   ACTS model, constraints, pairwise frames (30 frames)
│   │   ├── split3/          # Dean:    ACTS model, constraints, pairwise frames (12 frames)
│   │   └── split4/          # Ronny:   ACTS model, constraints, pairwise frames (15 frames)
│   ├── reports/
│   │   ├── split1_report.md
│   │   ├── split2_report.md
│   │   ├── split3_report.md
│   │   └── split4_report.md
│   └── spec/
│       ├── split1.md
│       ├── split2.md
│       ├── split3.md
│       └── split4.md
├── tests/
│   ├── common/
│   │   └── run_jq.py        # Shared helper: subprocess wrapper for jq
│   ├── split1/              # 18 tests (Jeffrey)
│   ├── split2/              # 30 tests (Tommy)
│   ├── split3/              # 12 tests (Dean)
│   └── split4/              # 15 tests (Ronny)
├── __MACOSX/ACTS3.0/        # ACTS 3.0 tool used for pairwise frame generation
├── requirements.txt
└── README.md
```

---

## Split Summaries

### Split 1 — Input Modes & File Ingestion (Jeffrey Wang)

**Scope:** Input reading behavior under different source and mode combinations.

- File path argument vs `-` (stdin)
- `-R` / `--raw-input`: treat input as raw text lines (no JSON parsing)
- `-s` / `--slurp`: aggregate all inputs into a JSON array (or string with `-R`)
- `-n` / `--null-input`: run filter without consuming input

**ACTS model:** 5 parameters → 18 pairwise frames
**Tests:** 18 (all pass)
**Bugs found:** None

---

### Split 2 — Output Formatting & Encoding (Tommy Duong)

**Scope:** Output formatting options and byte-level correctness.

- `-c` / `--compact-output`: compact JSON (no pretty-printing)
- `-r` / `--raw-output`: strings printed without JSON quoting
- `-j` / `--join-output`: suppressed record-separating newlines
- `--raw-output0`: NUL-terminated raw output

**ACTS model:** 4 parameters → 30 pairwise frames
**Tests:** 30 (all pass) — exact `stdout` byte comparisons including newline/NUL
**Bugs found:** None (platform note: Windows jq uses CRLF line endings)

---

### Split 3 — Error Handling & Exit Status (Dean Zhou)

**Scope:** Failure behavior, exit codes, and stderr correctness, including the `-e` flag.

- Invalid JSON → parse error on stderr, nonzero exit
- Invalid filter program → compile/syntax error on stderr, exit code 3
- Missing file / permission denied → file-open error on stderr, exit code 2
- `-e` / `--exit-status` semantics: truthy → 0, false/null → 1, no output → 4

**ACTS model:** 3 parameters → 12 pairwise frames (generated with ACTS 3.0 jar)
**Tests:** 12 (all pass)
**Bugs found:** None (version note: jq-1.7.1-apple returns exit code `5` for malformed JSON; oracles use nonzero for portability)

---

### Split 4 — Transform/Computation Filters (Ronny Rok)

**Scope:** Core transformation builtins on representative JSON inputs.

- Filters tested: `select`, `map`, `sort`, `group_by`, `unique`, `add`, `length`
- Input types: numeric arrays, object arrays, mixed arrays, empty arrays, strings, objects, null

**ACTS model:** 3 parameters → 15 pairwise frames
**Tests:** 15 (all pass)
**Bugs found:** None

---

## Overall Test Results

| Split | Tests | Passed | Failed | Skipped |
|-------|-------|--------|--------|---------|
| Split 1 | 18 | 18 | 0 | 0 |
| Split 2 | 30 | 30 | 0 | 0 |
| Split 3 | 12 | 12 | 0 | 0 |
| Split 4 | 15 | 15 | 0 | 0 |
| **Total** | **75** | **75** | **0** | **0** |

---

## Prerequisites

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install `jq`:

```bash
# macOS (Homebrew)
brew install jq

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y jq
```

---

## Run Tests

Run all tests:

```bash
pytest
```

Run a single split:

```bash
pytest -q tests/split1
pytest -q tests/split2
pytest -q tests/split3
pytest -q tests/split4
```

Run with verbose output:

```bash
pytest -v
```

---

## ACTS Pairwise Frame Generation

Test frames were generated using **ACTS 3.0** (available at `__MACOSX/ACTS3.0/acts_3.0.jar`) with 2-way (pairwise) coverage strength. Example command for Split 3:

```bash
java -Dalgo=ipog -Ddoi=2 -Doutput=csv -Dmode=scratch \
     -Dchandler=forbiddentuples -Dcheck=on \
     -jar __MACOSX/ACTS3.0/acts_3.0.jar \
     docs/acts/split3/split3_acts_input.txt \
     docs/acts/split3/split3_pairwise_from_macosx.csv
```

Each split's ACTS input model is in `docs/acts/split{N}/split{N}_acts_input.txt` (where present) and the resulting pairwise frames in `split{N}_pairwise_frames.csv`.
