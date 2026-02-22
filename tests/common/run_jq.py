"""Shared helper for invoking jq in tests."""

from __future__ import annotations

import subprocess
from typing import Optional


def run_jq(
    args: list[str], input_text: Optional[str] = None, timeout: int = 5
) -> tuple[int, str, str]:
    """Run jq with args and optional stdin text.

    Returns: (returncode, stdout, stderr)
    """
    cmd = ["jq", *args]
    try:
        completed = subprocess.run(
            cmd,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        stderr = (stderr + "\n" if stderr else "") + f"jq timed out after {timeout}s"
        return 124, stdout, stderr
