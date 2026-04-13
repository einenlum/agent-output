from __future__ import annotations

import json
import os
import re
import subprocess


def run_with(
    runner: str,
    fixture_path: str,
    *,
    with_agent: bool = True,
    extra_args: tuple[str, ...] = (),
) -> subprocess.CompletedProcess:
    env = {**os.environ}
    if with_agent:
        env["AI_AGENT"] = "1"
    else:
        env.pop("AI_AGENT", None)
    cmd = ["python", "-m", runner, fixture_path, *extra_args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def decode_output(proc: subprocess.CompletedProcess) -> dict:
    out = re.sub(r"\x1b\[[0-9;]*m", "", proc.stdout)
    match = re.search(r'(\{"result":.+)', out, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    raise ValueError(f"No JSON found.\nstdout: {proc.stdout}\nstderr: {proc.stderr}")
