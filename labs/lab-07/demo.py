#!/usr/bin/env python3
"""Lab 7 — The Token Ledger.

The lab program for the tokenledger package: it executes the package's
own demo (`python3 -m tokenledger.ledger` from the repository root) —
the same code, the same output, that the Udemy Course 9 Lesson
25 hands-on session built. At the lab-07-start tag this
file is a scaffold; at lab-07 it is complete, and validate.py
pins its first and last output lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tokenledger.ledger import main  # noqa: E402

if __name__ == "__main__":
    main()
