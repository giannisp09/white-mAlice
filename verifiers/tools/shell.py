import shlex
import subprocess
from typing import Dict, Any

def shell(command: str, timeout: int = 30) -> str:
    """
    Executes a shell command and returns its output (stdout or stderr).

    Args:
        command: The full command line to run (e.g. "ls -la /tmp").
        timeout: Seconds before we kill the process.

    Returns:
        stdout if the process exits cleanly, otherwise stderr.
    """
    try:
        # split for safety, avoid shell=True
        parts = shlex.split(command)
        proc = subprocess.run(
            parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        # prefer stdout unless empty
        output = proc.stdout.strip() or proc.stderr.strip()
        # truncate if excessively long
        if len(output) > 2000:
            return output[:2000] + "\n... (truncated)"
        return output
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout}s"
    except Exception as e:
        return f"Error: {str(e)}"