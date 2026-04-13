import subprocess
import sys


def test_with_subprocess() -> None:
    # Subprocess writes to the same stdout (no capture_output).
    # Its output should not corrupt the parent's JSON.
    subprocess.run(
        [sys.executable, "-c", "print('noise from subprocess')"],
    )
    assert True
