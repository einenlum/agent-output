from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING

from agent_output.drivers.base import Driver

if TYPE_CHECKING:
    import pytest


class PytestDriver(Driver):
    def __init__(self) -> None:
        self._passed: int = 0
        self._failed: int = 0
        self._skipped: int = 0
        self._xfailed: int = 0
        self._xpassed: int = 0
        self._errors: int = 0
        self._warnings: int = 0
        self._failures: list[dict] = []
        self._error_details: list[dict] = []
        self._start_time: float = time.monotonic()

    def collect(self, report: pytest.TestReport) -> None:
        if report.when == "call":
            self._collect_call(report)
            return
        if report.when in ("setup", "teardown"):
            self._collect_setup_teardown(report)

    def _collect_call(self, report: pytest.TestReport) -> None:
        wasxfail = hasattr(report, "wasxfail")
        if report.outcome == "passed":
            self._collect_passed(report, wasxfail)
            return
        if report.outcome == "failed":
            self._collect_failed(report)
            return
        if report.outcome == "skipped":
            self._collect_skipped(wasxfail)

    def _collect_passed(self, report: pytest.TestReport, wasxfail: bool) -> None:
        if wasxfail:
            self._xpassed += 1
            return
        self._passed += 1

    def collect_warning(self) -> None:
        self._warnings += 1

    def _collect_failed(self, report: pytest.TestReport) -> None:
        self._failed += 1
        self._failures.append(_extract_failure(report))

    def _collect_skipped(self, wasxfail: bool) -> None:
        if wasxfail:
            self._xfailed += 1
            return
        self._skipped += 1

    def _collect_setup_teardown(self, report: pytest.TestReport) -> None:
        if report.outcome == "failed":
            self._errors += 1
            self._error_details.append(_extract_failure(report))
        elif report.outcome == "skipped" and report.when == "setup":
            self._skipped += 1

    def build_result(self) -> dict | None:
        total = self._passed + self._failed + self._skipped + self._xfailed + self._xpassed
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
        if self._warnings:
            data["warnings"] = self._warnings
        if self._xfailed:
            data["xfailed"] = self._xfailed
        if self._xpassed:
            data["xpassed"] = self._xpassed
        data["duration_ms"] = duration_ms

        return data


def _extract_failure(report: pytest.TestReport) -> dict:
    crash = getattr(report.longrepr, "reprcrash", None)
    if crash:
        return {
            "test": report.nodeid,
            "file": str(report.fspath),
            "line": crash.lineno,
            "message": crash.message,
        }
    m = re.search(r"(\S+\.py):(\d+):\s*(.+)", str(report.longrepr))
    if m:
        return {
            "test": report.nodeid,
            "file": m.group(1),
            "line": int(m.group(2)),
            "message": m.group(3),
        }
    return {
        "test": report.nodeid,
        "file": str(report.fspath),
        "line": 0,
        "message": str(report.longrepr),
    }
