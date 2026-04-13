from __future__ import annotations

from ai_agent_detector import Result
from ai_agent_detector import detect_agent as _detect_agent


def detect() -> Result | None:
    result = _detect_agent()
    if result.is_agent:
        return result
    return None
