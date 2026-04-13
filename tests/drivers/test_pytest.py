from __future__ import annotations

import os

from tests.helpers import decode_output, run_with

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures", "pytest")


def fixture(name: str) -> str:
    return os.path.join(FIXTURES, name)


def test_passing() -> None:
    proc = run_with("pytest", fixture("test_passing.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"
    assert data["tests"] == 2
    assert data["passed"] == 2
    assert "failed" not in data


def test_failing() -> None:
    proc = run_with("pytest", fixture("test_failing.py"))
    data = decode_output(proc)
    assert data["result"] == "failed"
    assert data["failed"] == 1
    assert data["failures"][0]["message"] != ""


def test_line_number() -> None:
    proc = run_with("pytest", fixture("test_failing.py"))
    data = decode_output(proc)
    assert data["failures"][0]["line"] == 2


def test_error() -> None:
    proc = run_with("pytest", fixture("test_error.py"))
    data = decode_output(proc)
    assert data["errors"] == 1
    detail = data["error_details"][0]
    assert "file" in detail
    assert "line" in detail
    assert "message" in detail


def test_skipped() -> None:
    proc = run_with("pytest", fixture("test_skipped.py"))
    data = decode_output(proc)
    assert data["skipped"] == 1
    assert "failures" not in data


def test_xfail() -> None:
    proc = run_with("pytest", fixture("test_xfail.py"))
    data = decode_output(proc)
    assert data["xfailed"] == 1


def test_xpass() -> None:
    proc = run_with("pytest", fixture("test_xfail.py"))
    data = decode_output(proc)
    assert data["xpassed"] == 1


def test_parametrize() -> None:
    proc = run_with("pytest", fixture("test_parametrize.py"))
    data = decode_output(proc)
    assert data["tests"] == 5
    assert data["failed"] == 3


def test_multiple_failures() -> None:
    proc = run_with("pytest", fixture("test_multiple_failures.py"))
    data = decode_output(proc)
    assert data["failed"] == 2
    assert data["errors"] == 1
    assert len(data["failures"]) == 2


def test_stdout_noise() -> None:
    proc = run_with("pytest", fixture("test_stdout_noise.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"


def test_stdout_large() -> None:
    proc = run_with("pytest", fixture("test_stdout_large.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"


def test_unicode() -> None:
    proc = run_with("pytest", fixture("test_unicode.py"))
    data = decode_output(proc)
    assert data["result"] == "failed"
    assert data["failures"][0]["message"] != ""


def test_no_agent() -> None:
    proc = run_with("pytest", fixture("test_passing.py"), with_agent=False)
    assert '{"result":' not in proc.stdout


def test_warnings() -> None:
    proc = run_with("pytest", fixture("test_warnings.py"))
    data = decode_output(proc)
    assert data.get("warnings", 0) > 0


def test_duration() -> None:
    proc = run_with("pytest", fixture("test_passing.py"))
    data = decode_output(proc)
    assert "duration_ms" in data
    assert data["duration_ms"] > 0
