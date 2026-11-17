#!/usr/bin/env python3
"""Lab 8 — Hunt the p99.

The lab program for the p99hunt package: it executes the package's
own demo (`python3 -m p99hunt.profile` from the repository root) —
the same code, the same output, that the Udemy Course 9 Lesson
29 hands-on session built. At the lab-08-start tag this
file is a scaffold; at lab-08 it is complete, and validate.py
pins its first and last output lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p99hunt.profile import main  # noqa: E402

if __name__ == "__main__":
    main()
