# CMPT Assignment 2 - jq Functional Testing Scaffold

This repository is a team scaffold for CMPT Assignment 2 using `jq` as the Program Under Test (PUT).

## Team Split Layout

Each split is isolated so each teammate can work end-to-end in their own folder with minimal merge conflicts:

- `docs/spec/split1.md`, `tests/split1/`
- `docs/spec/split2.md`, `tests/split2/` (Tommy: formatting and encoding)
- `docs/spec/split3.md`, `tests/split3/` (Dean: error handling + `-e` exit status)
- `docs/spec/split4.md`, `tests/split4/`

ACTS models/frames and reports are also split-specific under `docs/acts/` and `docs/reports/`.

## Contributions

| Split | Owner | Scope |
| --- | --- | --- |
| Split 1 | TBD | Add spec, ACTS model/frames, tests, and report for Split 1 |
| Split 2 | Tommy Duong(tda49) | Formatting and encoding     |
| Split 3 | Dean Zhou(dza68) | Error handling + `-e` / `--exit-status` |
| Split 4 | TBD | Add spec, ACTS model/frames, tests, and report for Split 4 |

Update owner names once all team members are finalized.

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

## Run Tests

Run all tests:

```bash
pytest
```

Run Split 3 tests only:

```bash
pytest -q tests/split3
```
