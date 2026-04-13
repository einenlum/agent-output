from __future__ import annotations

from ai_agent_detector import detect as _detect
from ai_agent_detector import Agent


def detect() -> Agent | None:
    return _detect()
