"""Tests for the automatic local machine fingerprint."""

import pytest

from machine_fingerprint import _fingerprint_from_parts


def test_fingerprint_is_deterministic_and_normalized() -> None:
    """Equivalent identity parts produce the same uppercase fingerprint."""

    first = _fingerprint_from_parts((" os-machine-id=abc ", "system=Darwin"))
    second = _fingerprint_from_parts(("os-machine-id=abc", "system=Darwin"))

    assert first == second
    assert len(first) == 32
    assert first.isupper()


def test_fingerprint_changes_when_identity_changes() -> None:
    """Different identity inputs do not share the same fingerprint."""

    assert _fingerprint_from_parts(("machine-a",)) != _fingerprint_from_parts(
        ("machine-b",)
    )


def test_empty_identity_is_rejected() -> None:
    """A missing identity fails explicitly instead of creating an empty ID."""

    with pytest.raises(RuntimeError, match="No machine identity"):
        _fingerprint_from_parts(("", "  "))
