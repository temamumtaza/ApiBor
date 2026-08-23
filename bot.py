#!/usr/bin/env python3
"""botbor entry point.

The bot can be run directly; no machine activation or runtime license key is
required. The implementation remains in ``_core.py`` so it can also be
imported and tested independently.
"""

from pathlib import Path


CORE_PATH = Path(__file__).with_name("_core.py")


if not CORE_PATH.is_file():
    raise FileNotFoundError(f"Core file not found: {CORE_PATH}")


exec(
    compile(CORE_PATH.read_text(encoding="utf-8"), str(CORE_PATH), "exec"),
    globals(),
)
