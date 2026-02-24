"""Shared helper for invoking jq in tests."""

from __future__ import annotations

import subprocess


def run_jq(
    args: list[str], input_text: str | None = None, timeout: int = 5
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
    except FileNotFoundError:
        return 127, "", "jq executable not found"


def run_jq_bytes(
    args: list[str], input_bytes: bytes | None = None, timeout: int = 5
) -> tuple[int, bytes, bytes]:
    """Run jq with args and optional stdin bytes.

    Returns: (returncode, stdout_bytes, stderr_bytes)
    """
    cmd = ["jq", *args]
    try:
        completed = subprocess.run(
            cmd,
            input=input_bytes,
            text=False,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, bytes) else b""
        stderr = exc.stderr if isinstance(exc.stderr, bytes) else b""
        timeout_msg = f"jq timed out after {timeout}s".encode("utf-8")
        return 124, stdout, (stderr + b"\n" if stderr else b"") + timeout_msg
    except FileNotFoundError:
        return 127, b"", b"jq executable not found"
