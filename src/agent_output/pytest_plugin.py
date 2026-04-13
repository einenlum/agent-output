from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from agent_output.drivers.pytest_driver import PytestDriver
from agent_output.execution import Execution

if TYPE_CHECKING:
    import warnings


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    if Execution.running():
        config.pluginmanager.unregister(name="terminalreporter")
        config.pluginmanager.register(AgentOutputPlugin())


class AgentOutputPlugin:
    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        driver = Execution.current().driver
        assert isinstance(driver, PytestDriver)
        driver.collect(report)

    def pytest_warning_recorded(
        self,
        warning_message: warnings.WarningMessage,
        when: str,
        nodeid: str,
        location: tuple[str, int, str] | None,
    ) -> None:
        Execution.current().driver.collect_warning()
