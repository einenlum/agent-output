from __future__ import annotations

from typing import TYPE_CHECKING

from agent_output.execution import Execution

if TYPE_CHECKING:
    import pytest
    from _pytest.terminal import TerminalReporter


def pytest_configure(config: pytest.Config) -> None:
    if Execution.running():
        config.pluginmanager.register(AgentOutputPlugin())


class AgentOutputPlugin:
    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        Execution.current().driver.collect(report)

    def pytest_terminal_summary(
        self,
        terminalreporter: TerminalReporter,
        exitstatus: pytest.ExitCode,
        config: pytest.Config,
    ) -> None:
        terminalreporter.stats.clear()
