#!/usr/bin/env python3
"""Lab 13 — Capstone Review: Ship the Watchtower.

The review program (composed for Skool, on the Udemy Course 9
Lesson 51 model): where Lab 12 runs the whole watchstack report,
this program walks ONLY the production observability checklist —
watchstack's own review() — line by line against the running
stack, and prints the review verdict the evidence earns. Every
grade printed is computed by the package at run time: 22 items,
each EVIDENCED, OPEN, or a blocker, with the telemetry bill the
watching itself ran up.

Run from the repository root:  python3 labs/lab-13/demo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from watchstack.stack import review  # noqa: E402


def main() -> None:
    print("== capstone review: ship the watchtower ==")
    evidenced, opened, blockers = review()
    if blockers == 0:
        print("review verdict: SHIP — the stack ships; the "
              f"{opened} open obligations ship with it, named")
    else:
        print("review verdict: HOLD — measured items failed; the "
              "stack does not ship")
    print(f"review summary: {evidenced} evidenced, {opened} open, "
          f"{blockers} blockers")
    print("watchstack review complete")


if __name__ == "__main__":
    main()
