#!/usr/bin/env python3
"""Lab 11 — Localise the Fault.

The lab program for the culprit package: it executes the package's
own demo (`python3 -m culprit.blame` from the repository root) —
the same code, the same output, that the Udemy Course 9 Lesson
45 hands-on session built. At the lab-11-start tag this
file is a scaffold; at lab-11 it is complete, and validate.py
pins its first and last output lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from culprit.blame import main  # noqa: E402

if __name__ == "__main__":
    main()
