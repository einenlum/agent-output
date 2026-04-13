from __future__ import annotations

import atexit
import json
import os
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_output.agent_detector import Agent
    from agent_output.drivers.base import Driver


class Execution:
    _instance: Execution | None = None

    def __init__(self, agent: Agent, driver: Driver) -> None:
        self.agent = agent
        self.driver = driver
        self.start_time = time.monotonic()

    @classmethod
    def start(cls, agent: Agent, argv: list[str]) -> None:
        from agent_output.drivers.base import resolve_driver

        driver = resolve_driver(argv)
        if driver is None:
            return
        cls._instance = cls(agent, driver)
        atexit.register(cls._shutdown)

    @classmethod
    def running(cls) -> bool:
        return cls._instance is not None

    @classmethod
    def current(cls) -> Execution:
        assert cls._instance is not None
        return cls._instance

    @classmethod
    def _shutdown(cls) -> None:
        if not cls.running():
            return
        result = cls.current().driver.build_result()
        if result:
            os.write(1, (json.dumps(result) + "\n").encode())
