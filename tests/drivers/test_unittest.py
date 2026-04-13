from __future__ import annotations

import os

from tests.helpers import decode_output, run_with

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures", "unittest")


def fixture(name: str) -> str:
    return os.path.join(FIXTURES, name)


def test_passing() -> None:
    proc = run_with("unittest", fixture("test_passing.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"
    assert data["tests"] == 2
    assert data["passed"] == 2
    assert "failed" not in data


def test_failing() -> None:
    proc = run_with("unittest", fixture("test_failing.py"))
    data = decode_output(proc)
    assert data["result"] == "failed"
    assert data["failed"] == 1
    assert data["failures"][0]["message"] != ""


def test_line_number() -> None:
    proc = run_with("unittest", fixture("test_failing.py"))
    data = decode_output(proc)
    assert data["failures"][0]["line"] == 6


def test_error() -> None:
    proc = run_with("unittest", fixture("test_error.py"))
    data = decode_output(proc)
    assert data["errors"] == 1
    detail = data["error_details"][0]
    assert "file" in detail
    assert "line" in detail
    assert "message" in detail


def test_skipped() -> None:
    proc = run_with("unittest", fixture("test_skipped.py"))
    data = decode_output(proc)
    assert data["skipped"] == 1
    assert "failures" not in data


def test_multiple_failures() -> None:
    proc = run_with("unittest", fixture("test_multiple_failures.py"))
    data = decode_output(proc)
    assert data["failed"] == 2
    assert data["errors"] == 1
    assert len(data["failures"]) == 2


def test_no_agent() -> None:
    proc = run_with("unittest", fixture("test_passing.py"), with_agent=False)
    assert '{"result":' not in proc.stdout


def test_duration() -> None:
    proc = run_with("unittest", fixture("test_passing.py"))
    data = decode_output(proc)
    assert "duration_ms" in data
    assert data["duration_ms"] >= 0
