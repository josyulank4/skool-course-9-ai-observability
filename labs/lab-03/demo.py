#!/usr/bin/env python3
"""Lab 3 — Emit, Validate, Redact.

The lab program for the logline package: it executes the package's
own demo (`python3 -m logline.emit` from the repository root) —
the same code, the same output, that the Udemy Course 9 Lesson
9 hands-on session built. At the lab-03-start tag this
file is a scaffold; at lab-03 it is complete, and validate.py
pins its first and last output lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from logline.emit import main  # noqa: E402

if __name__ == "__main__":
    main()
