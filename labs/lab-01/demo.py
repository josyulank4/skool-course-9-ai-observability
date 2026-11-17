#!/usr/bin/env python3
"""Lab 1 — the observability tour (authored for Skool Course 9).

One genuine first run across the whole companion repo: the shared
telemetry dataset from obscommon.py, then ONE small real check per
package family — the same functions the later labs build in full.
Nothing here is a mock: every line printed is computed by the
course's own packages, on the course's own data, at run time.

Run from the repository root:  python3 labs/lab-01/demo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from obscommon import FEATURES, TENANTS, gen_events, mean  # noqa: E402
from blindspot.baseline import snapshot  # noqa: E402
from logline.emit import make_events, redact_event, validate_event  # noqa: E402
from traceweave.trace import build_trace, failed_spans, slowest_span, total_ms  # noqa: E402
from promptwatch.registry import compare as prompt_compare  # noqa: E402
from judgeaudit.audit import audit  # noqa: E402
from tokenledger.ledger import ledger, retry_storm  # noqa: E402
from p99hunt.profile import dominant_p99, profile  # noqa: E402
from decayradar.drift import compare as drift_compare  # noqa: E402
from pagewise.alerts import simulate  # noqa: E402
from culprit.blame import first_failure  # noqa: E402
from watchstack.stack import run_checks  # noqa: E402


def main() -> None:
    print("observability-tour: one dataset, eleven watchers")

    events = gen_events(n=200, seed=42)
    print(f"dataset: {len(events)} support-chat requests, tenants "
          f"{'/'.join(TENANTS)}, features {'/'.join(FEATURES)}")
    print(f"dataset: mean quality {mean([e['quality'] for e in events]):.3f}, "
          f"every request priced from the shared token table")

    before = snapshot("tour blindspot before", events)
    after = snapshot("tour blindspot after",
                     gen_events(n=200, seed=42, quality_shift=-0.32,
                                halluc_rate=0.22))
    print(f"tour blindspot: infra moved {after['error_rate'] - before['error_rate']:+.3f} "
          f"while quality moved {after['mean_quality'] - before['mean_quality']:+.3f} "
          "— the gap, in one line")

    raw = make_events()
    hits = 0
    for ev in raw:
        assert validate_event(ev) == [], f"tour event failed schema: {ev}"
        _, h = redact_event(ev)
        hits += h
    print(f"tour logline: {len(raw)} events schema-valid, {hits} planted "
          "secrets/PII redacted before storage")

    spans = build_trace()
    failed = failed_spans(spans)
    print(f"tour traceweave: one request, {len(spans)} spans, "
          f"{total_ms(spans):.0f} ms end to end; slowest span "
          f"{slowest_span(spans)['name']}; failed span "
          f"{failed[0]['name'] if failed else 'none'}")

    pc = prompt_compare()
    print(f"tour promptwatch: prompt v3 quality {pc['v3_quality']:.2f} vs "
          f"v4 {pc['v4_quality']:.2f} — the regression is real, the "
          "registry holds v4")

    ja = audit()
    print(f"tour judgeaudit: judge agrees with humans {ja['agreement']:.0%} "
          f"of the time; verbose wrong answers average "
          f"{ja['verbose_wrong_mean']:.2f} vs concise right "
          f"{ja['concise_right_mean']:.2f} — the bias, measured")

    led = ledger(events + retry_storm())
    top = max(led["by_tenant"], key=led["by_tenant"].get)
    print(f"tour tokenledger: {len(events) + len(retry_storm())} requests, "
          f"${led['total']:.4f} total; top tenant {top} "
          f"${led['by_tenant'][top]:.4f} (the retry storm is inside)")

    prof = profile(gen_events(n=500, seed=42))
    print(f"tour p99hunt: 500 requests profiled by stage; the p99 is "
          f"owned by {dominant_p99(prof)}")

    drift = drift_compare(events, gen_events(n=200, seed=42,
                                             quality_shift=-0.18,
                                             halluc_rate=0.15))
    print(f"tour decayradar: quality drift {drift['quality_drift']}, "
          f"hallucination drift {drift['halluc_drift']} — the radar "
          "fires on the decayed window")

    sim = simulate()
    print(f"tour pagewise: naive paging {len(sim['naive_pages'])} pages "
          f"({len(sim['naive_false'])} false) vs burn-rate "
          f"{len(sim['burn_pages'])} pages ({len(sim['burn_false'])} "
          "false) on the same history")

    ff = first_failure()
    print(f"tour culprit: the fleet's first failure is {ff['agent']} — "
          f"check '{ff['check']}' scored {ff['score']:.2f}")

    checks, warnings = run_checks()
    print(f"tour watchstack: {sum(1 for _, ok in checks if ok)}/"
          f"{len(checks)} stack checks pass, {len(warnings)} warnings "
          "named, none hidden")

    print("observability-tour demo: OK")


if __name__ == "__main__":
    main()
