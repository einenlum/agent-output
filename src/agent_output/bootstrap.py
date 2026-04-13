from __future__ import annotations

import os
import sys

from agent_output.agent_detector import detect
from agent_output.execution import Execution


def _is_skip_context(argv: list[str]) -> bool:
    skip_flags = {"--version", "--help", "-h"}
    return bool(skip_flags & set(argv)) or "AGENT_OUTPUT_DISABLE" in os.environ


agent = detect()
if agent and not _is_skip_context(sys.argv):
    Execution.start(agent, sys.argv)
