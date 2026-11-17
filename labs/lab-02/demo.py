#!/usr/bin/env python3
"""Lab 2 — The Gap, Measured.

The lab program for the blindspot package: it executes the package's
own demo (`python3 -m blindspot.baseline` from the repository root) —
the same code, the same output, that the Udemy Course 9 Lesson
5 hands-on session built. At the lab-02-start tag this
file is a scaffold; at lab-02 it is complete, and validate.py
pins its first and last output lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from blindspot.baseline import main  # noqa: E402

if __name__ == "__main__":
    main()
