from __future__ import annotations

import os
import time
import traceback
import unittest
from types import TracebackType

from agent_output.drivers.base import Driver

_ExcInfo = (
    tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]
)
_UNITTEST_DIR = os.path.dirname(unittest.__file__) + os.sep


def _extract_location(tb: TracebackType) -> tuple[str, int]:
    frames = traceback.extract_tb(tb)
    for frame in reversed(frames):
        if not frame.filename.startswith("<") and not frame.filename.startswith(
            _UNITTEST_DIR
        ):
            return frame.filename, frame.lineno or 0
    last = frames[-1]
    return last.filename, last.lineno or 0


class AgentOutputTestResult(unittest.TestResult):
    def __init__(self, driver: UnittestDriver) -> None:
        super().__init__()
        self._driver = driver

    def addSuccess(self, test: unittest.TestCase) -> None:
        self._driver._passed += 1

    def addFailure(self, test: unittest.TestCase, err: _ExcInfo) -> None:
        self._driver._failed += 1
        _, exc_value, tb = err
        if tb is None or exc_value is None:
            return
        file, line = _extract_location(tb)
        self._driver._failures.append(
            {
                "test": str(test),
                "file": file,
                "line": line,
                "message": str(exc_value),
            }
        )

    def addError(self, test: unittest.TestCase, err: _ExcInfo) -> None:
        self._driver._errors += 1
        _, exc_value, tb = err
        if tb is None or exc_value is None:
            return
        file, line = _extract_location(tb)
        self._driver._error_details.append(
            {
                "test": str(test),
                "file": file,
                "line": line,
                "message": str(exc_value),
            }
        )

    def addSkip(self, test: unittest.TestCase, reason: str) -> None:
        self._driver._skipped += 1

    def addExpectedFailure(self, test: unittest.TestCase, err: _ExcInfo) -> None:
        self._driver._xfailed += 1

    def addUnexpectedSuccess(self, test: unittest.TestCase) -> None:
        self._driver._xpassed += 1


class UnittestDriver(Driver):
    def __init__(self) -> None:
        self._passed: int = 0
        self._failed: int = 0
        self._errors: int = 0
        self._skipped: int = 0
        self._xfailed: int = 0
        self._xpassed: int = 0
        self._failures: list[dict] = []
        self._error_details: list[dict] = []
        self._start_time: float = time.monotonic()
        self._patch()

    def _patch(self) -> None:
        import unittest.runner

        driver = self

        class _Runner:
            def __init__(self_inner, *args: object, **kwargs: object) -> None:
                pass

            def run(
                self_inner,
                test: unittest.TestSuite | unittest.TestCase,
            ) -> AgentOutputTestResult:
                result = AgentOutputTestResult(driver)
                test(result)
                return result

        unittest.TextTestRunner = _Runner  # type: ignore[misc, assignment]
        unittest.runner.TextTestRunner = _Runner  # type: ignore[misc, assignment]

    def build_result(self) -> dict | None:
        total = (
            self._passed + self._failed + self._skipped + self._xfailed + self._xpassed
        )
        duration_ms = int((time.monotonic() - self._start_time) * 1000)

        data: dict = {
            "result": "failed" if self._failed or self._errors else "passed",
            "tests": total,
            "passed": self._passed,
        }
        if self._failed:
            data["failed"] = self._failed
        if self._failures:
            data["failures"] = self._failures
        if self._errors:
            data["errors"] = self._errors
        if self._error_details:
            data["error_details"] = self._error_details
        if self._skipped:
            data["skipped"] = self._skipped
        if self._xfailed:
            data["xfailed"] = self._xfailed
        if self._xpassed:
            data["xpassed"] = self._xpassed
        data["duration_ms"] = duration_ms

        return data
