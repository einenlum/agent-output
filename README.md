# agent-output

[![CI](https://github.com/Einenlum/agent-output/actions/workflows/ci.yml/badge.svg)](https://github.com/Einenlum/agent-output/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/agent-output)](https://pypi.org/project/agent-output/)
[![Python](https://img.shields.io/pypi/pyversions/agent-output)](https://pypi.org/project/agent-output/)
[![License](https://img.shields.io/pypi/l/agent-output)](LICENSE)

Drastically reduce token consumption when running `pytest` or `unittest` inside an AI agent.

Heavily inspired by [Nuno Maduro](https://github.com/nunomaduro)'s [Pao](https://github.com/nunomaduro/pao) for PHP.

---

## The problem

When an AI agent (Claude, Copilot, Cursor, …) runs your test suite, it reads the full terminal output to understand what happened. A typical pytest run for a medium-sized project can easily produce hundreds of lines:

```
============================= test session starts ==============================
platform linux -- Python 3.13.0, pytest-8.3.0, pluggy-1.5.0
rootdir: /home/user/myproject
collected 42 items

tests/test_auth.py .......                                               [ 16%]
tests/test_api.py ....F..                                                [ 33%]
...
=========================== short test summary info ============================
FAILED tests/test_api.py::test_create_user - AssertionError: expected 201, got 400
========================= 1 failed, 41 passed in 3.42s =========================
```

Every character of that output consumes tokens from the agent's context window. On large test suites this waste is significant, and it crowds out space for the actual code the agent needs to read and write.

## The solution

**agent-output** replaces the entire human-readable terminal output with a single compact JSON line — but *only* when a test run is happening inside an AI agent environment. Regular developer sessions are completely unaffected.

When tests fail, the agent gets the overall result, counts, and precise failure locations — nothing else:

```json
{
  "result": "failed",
  "tests": 42,
  "passed": 41,
  "failed": 1,
  "failures": [
    {
      "test": "tests/test_api.py::test_create_user",
      "file": "tests/test_api.py",
      "line": 14,
      "message": "AssertionError: expected 201, got 400"
    }
  ],
  "duration_ms": 3421
}
```

When everything passes, there's nothing to report beyond the essentials:

```json
{
  "result": "passed",
  "tests": 42,
  "passed": 42,
  "duration_ms": 2187
}
```

Only fields that carry information are included — zero-count fields are omitted entirely.

## How it works

### Agent detection

agent-output uses [ai-agent-detector](https://github.com/Einenlum/ai-agent-detector) to determine whether the current process is running inside an AI agent. Detection is automatic; no configuration is required.

You can also force agent mode by setting `AI_AGENT=1` in your environment, or disable it entirely with `AGENT_OUTPUT_DISABLE=1`.

### Zero-config bootstrap

The package installs a `.pth` file into your Python environment's `site-packages`. Python processes this file at interpreter startup, which imports `agent_output.bootstrap` before any user code runs — so the plugin activates without any changes to your project.

### pytest integration

When `pytest` is detected in `sys.argv`, agent-output registers itself as a pytest plugin and **unregisters the default terminal reporter**. It collects every `TestReport` event and, on process exit, serialises the full summary to a single JSON line on stdout.

Captured fields: `result`, `tests`, `passed`, `failed`, `failures` (with file, line, message), `errors`, `error_details`, `skipped`, `warnings`, `xfailed`, `xpassed`, `duration_ms`.

### unittest integration

When `unittest` is detected, agent-output monkey-patches `unittest.TextTestRunner` with a silent runner backed by a custom `TestResult` subclass that accumulates the same statistics. The JSON summary is emitted on process exit via `atexit`.

## Installation

```bash
pip install agent-output
```

That's it. No `conftest.py` changes, no `pytest.ini` options, no import statements.

## Output format

All fields except `result`, `tests`, `passed`, and `duration_ms` are omitted when their count is zero.

| Field           | Type                      | Description                                     |
|-----------------|---------------------------|-------------------------------------------------|
| `result`        | `"passed"` \| `"failed"` | Overall outcome                                 |
| `tests`         | int                       | Total number of tests collected                 |
| `passed`        | int                       | Tests that passed                               |
| `failed`        | int                       | Tests that failed                               |
| `failures`      | list                      | Per-failure details (test, file, line, message) |
| `errors`        | int                       | Setup/teardown errors                           |
| `error_details` | list                      | Per-error details                               |
| `skipped`       | int                       | Skipped tests                                   |
| `warnings`      | int                       | Warnings recorded during the run                |
| `xfailed`       | int                       | Expected failures                               |
| `xpassed`       | int                       | Unexpected passes                               |
| `duration_ms`   | int                       | Wall-clock duration of the run in milliseconds  |

## Disabling

Set `AGENT_OUTPUT_DISABLE=1` to suppress agent-output even when an agent is detected. Useful in CI or any context where you want normal output regardless.

## Requirements

- Python 3.11+
- pytest 8.0+ (optional — unittest works without pytest)

## Credits

This project is heavily inspired by [Pao](https://github.com/nunomaduro/pao) by [Nuno Maduro](https://github.com/nunomaduro), which applies the same idea to PHP's Artisan test runner.

## Author

Yann Rabiller ([@einenlum](https://github.com/Einenlum/)) | [blog](https://www.einenlum.com) | [From PHP to Python](https://fromphptopython.com)

## License

MIT
