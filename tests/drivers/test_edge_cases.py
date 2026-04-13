from __future__ import annotations

import os

from tests.helpers import decode_output, run_with

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures", "pytest")


def fixture(name: str) -> str:
    return os.path.join(FIXTURES, name)


def test_pytest_large_output() -> None:
    proc = run_with("pytest", fixture("test_stdout_large.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"
    assert data["tests"] == 1


def test_pytest_binary_stdout() -> None:
    proc = run_with("pytest", fixture("test_binary_stdout.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"
    assert data["tests"] == 1


def test_pytest_unicode_emoji() -> None:
    proc = run_with("pytest", fixture("test_unicode_names.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"
    assert data["tests"] == 5


def test_agent_output_disable() -> None:
    proc = run_with("pytest", fixture("test_passing.py"), with_agent=False)
    assert '{"result":' not in proc.stdout


def test_subprocess_in_test() -> None:
    proc = run_with("pytest", fixture("test_subprocess_call.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"
    assert data["tests"] == 1


def test_output_buffering() -> None:
    proc = run_with("pytest", fixture("test_redirect_stdout.py"))
    data = decode_output(proc)
    assert data["result"] == "passed"
    assert data["tests"] == 1
