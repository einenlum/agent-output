from __future__ import annotations

from abc import ABC, abstractmethod


class Driver(ABC):
    @abstractmethod
    def build_result(self) -> dict | None: ...


def resolve_driver(argv: list[str]) -> Driver | None:
    joined = " ".join(argv)
    if "pytest" in joined or "py.test" in joined:
        from agent_output.drivers.pytest_driver import PytestDriver

        return PytestDriver()
    if "unittest" in joined:
        from agent_output.drivers.unittest_driver import UnittestDriver

        return UnittestDriver()
    return None
