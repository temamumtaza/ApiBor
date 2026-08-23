"""Generate a stable, local-only fingerprint for this machine.

The raw platform identifiers are used only inside the current process. The
public function returns a truncated SHA-256 digest, so callers never need to
store or display the underlying hardware identifiers.
"""

from __future__ import annotations

import hashlib
import platform
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

_FINGERPRINT_DOMAIN = b"apibor-machine-fingerprint-v1\0"
_FINGERPRINT_LENGTH = 32


def _read_first_line(path: Path) -> str:
    """Read the first non-empty line from a text file when available."""

    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value:
                return value
    except (OSError, UnicodeError):
        pass
    return ""


def _run_command(command: tuple[str, ...]) -> str:
    """Return command output, or an empty string if the command is unavailable."""

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _linux_machine_id() -> str:
    """Read Linux's stable machine identifier when present."""

    if not sys.platform.startswith("linux"):
        return ""
    for path in (Path("/etc/machine-id"), Path("/var/lib/dbus/machine-id")):
        value = _read_first_line(path)
        if value:
            return value
    return ""


def _macos_platform_uuid() -> str:
    """Read macOS's platform UUID without exposing it to the caller."""

    if sys.platform != "darwin":
        return ""
    output = _run_command(("ioreg", "-rd1", "-c", "IOPlatformExpertDevice"))
    for line in output.splitlines():
        if "IOPlatformUUID" not in line:
            continue
        _, separator, value = line.partition("=")
        if separator:
            return value.strip().strip('"')
    return ""


def _windows_machine_guid() -> str:
    """Read Windows' machine GUID when running on Windows."""

    if sys.platform != "win32":
        return ""
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "MachineGuid")
    except (ImportError, OSError):
        return ""
    return str(value).strip()


def _identity_parts() -> tuple[str, ...]:
    """Collect the smallest stable identity available on the current OS."""

    os_identifier = (
        _linux_machine_id() or _macos_platform_uuid() or _windows_machine_guid()
    )
    if os_identifier:
        return (f"os-machine-id={os_identifier}",)

    # Fallback for platforms where no OS-provided machine ID is available.
    fallback = (
        f"system={platform.system()}",
        f"node={platform.node()}",
        f"machine={platform.machine()}",
        f"processor={platform.processor()}",
    )
    return tuple(value for value in fallback if value.split("=", 1)[1].strip())


def _fingerprint_from_parts(parts: Iterable[str]) -> str:
    """Hash identity parts into the public fingerprint format."""

    normalized = tuple(value.strip() for value in parts if value.strip())
    if not normalized:
        raise RuntimeError("No machine identity is available")
    payload = _FINGERPRINT_DOMAIN + "\n".join(normalized).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:_FINGERPRINT_LENGTH].upper()


def get_machine_fingerprint() -> str:
    """Return an automatically generated, stable local machine fingerprint."""

    return _fingerprint_from_parts(_identity_parts())
