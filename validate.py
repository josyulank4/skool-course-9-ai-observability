#!/usr/bin/env python3
"""Validate the Skool Course 9 companion repository.

Run from the repository root:  python3 validate.py

Checks: repository structure, the shared dataset's determinism,
one behaviour check per companion package (the package's real
API, exercised in-process), one run check per lab (the lab
program executed; first and last output lines pinned to the
verified runs), the lab tag scheme's documentation, a
no-hardcoded-secrets scan, and a documentation check. Exits
non-zero on the first failure.
"""
from __future__ import annotations

import contextlib
import io
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
RESULTS: list[tuple[str, bool, str]] = []

PACKAGES = {
    "blindspot": "baseline", "logline": "emit", "traceweave": "trace",
    "promptwatch": "registry", "judgeaudit": "audit",
    "tokenledger": "ledger", "p99hunt": "profile",
    "decayradar": "drift", "pagewise": "alerts", "culprit": "blame",
    "watchstack": "stack",
}
LAB_DIRS = [f"lab-{i:02d}" for i in range(1, 14)]

# (lab folder, expected first line, expected last line) — pinned to
# the verified runs of the finished lab programs.
LAB_RUNS = [
    ("lab-01",
     "observability-tour: one dataset, eleven watchers",
     "observability-tour demo: OK"),
    ("lab-02",
     "before silent model change: error rate 0.010, p95 latency "
     "1987.0 ms, mean quality 0.850, hallucination rate 0.025",
     "blindspot demo complete"),
    ("lab-03",
     '{"input_tokens": 412, "model": "chat-small", '
     '"output_tokens": 233, "quality": 0.91, "request_id": '
     '"req-0001", "tenant": "acme", "total_ms": 1180.4}',
     "logline demo complete"),
    ("lab-04",
     "span agent-request          kind=root      start     0.0 ms  "
     "dur 2140.0 ms  ok",
     "traceweave demo complete"),
    ("lab-05", "prompt diff v3 -> v4:", "promptwatch demo complete"),
    ("lab-06",
     "a01: human=pass judge=0.91 (pass) words=142 AGREE",
     "judgeaudit demo complete"),
    ("lab-07", "requests: 240 (base 200 + retries 40)",
     "tokenledger demo complete"),
    ("lab-08", "requests profiled: 500", "p99hunt demo complete"),
    ("lab-09",
     "baseline window: mean quality 0.850, hallucination rate 0.025",
     "decayradar demo complete"),
    ("lab-10", "SLO: 0.999 over 1,000,000 monthly requests",
     "pagewise demo complete"),
    ("lab-11",
     "agent router     depends_on=-          check 'intent "
     "classified': 0.94 pass — intent: refund question",
     "culprit demo complete"),
    ("lab-12", "== support-chat observability report ==",
     "watchstack demo complete"),
    ("lab-13", "== capstone review: ship the watchtower ==",
     "watchstack review complete"),
]


def check(name):
    def deco(fn):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            RESULTS.append((name, False, str(exc)))
            print(f"FAIL {name}: {exc}")
        else:
            RESULTS.append((name, True, ""))
            print(f"PASS {name}")
        return fn
    return deco


def expect(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def expect_true(cond, label):
    if not cond:
        raise AssertionError(label)


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


# ---------------------------------------------------------------- structure

@check("structure: root files, 11 packages, 13 lab folders")
def _():
    for f in ("README.md", "validate.py", "LICENSE", "obscommon.py"):
        expect_true((ROOT / f).is_file(), f"missing root file {f}")
    for pkg, mod in PACKAGES.items():
        expect_true((ROOT / pkg / "__init__.py").is_file(),
                    f"missing {pkg}/__init__.py")
        expect_true((ROOT / pkg / f"{mod}.py").is_file(),
                    f"missing {pkg}/{mod}.py")
        expect_true((ROOT / pkg / "README.md").is_file(),
                    f"missing {pkg}/README.md")
    for d in LAB_DIRS:
        expect_true((ROOT / "labs" / d / "demo.py").is_file(),
                    f"missing labs/{d}/demo.py")
        expect_true((ROOT / "labs" / d / "README.md").is_file(),
                    f"missing labs/{d}/README.md")


@check("obscommon: the shared dataset is deterministic and priced")
def _():
    import obscommon
    a = obscommon.gen_events(n=200, seed=42)
    b = obscommon.gen_events(n=200, seed=42)
    expect(a, b, "same seed must give the same events, forever")
    expect(len(a), 200, "dataset size")
    expect({e["tenant"] for e in a}, set(obscommon.TENANTS), "tenants")
    expect(round(obscommon.mean([e["quality"] for e in a]), 3), 0.850,
           "baseline mean quality")
    expect_true(all(obscommon.cost_usd(e) > 0 for e in a),
                "every request carries a price")


# ---------------------------------------------------------------- behaviour

@check("blindspot: infra stays green while quality falls off a cliff")
def _():
    from blindspot.baseline import snapshot
    from obscommon import gen_events
    b = quiet(snapshot, "b", gen_events(n=200, seed=42))
    a = quiet(snapshot, "a", gen_events(n=200, seed=42,
                                        quality_shift=-0.32,
                                        halluc_rate=0.22))
    expect(a["error_rate"] - b["error_rate"], 0.0, "error rate moved")
    expect(round(a["mean_quality"] - b["mean_quality"], 3), -0.320,
           "quality drop")
    expect(round(b["halluc_rate"], 3), 0.025, "baseline hallucination")
    expect(round(a["halluc_rate"], 3), 0.195, "decayed hallucination")


@check("logline: events validate; the planted secret never lands")
def _():
    from logline.emit import make_events, redact_event, validate_event
    evs = make_events()
    expect(len(evs), 3, "event count")
    for ev in evs:
        expect(validate_event(ev), [], f"schema errors in {ev}")
    expect_true(validate_event({}) != [], "empty event must fail schema")
    planted = evs[1]["api_key"]  # the lesson's fake key fixture
    hits = 0
    for ev in evs:
        clean, h = redact_event(ev)
        hits += h
        expect_true(planted not in str(clean),
                    "the planted key value survived redaction")
        expect_true("jane.doe@example.com" not in str(clean),
                    "the planted email survived redaction")
    expect(redact_event(evs[1])[0]["api_key"], "[REDACTED]",
           "the key field itself is masked")
    expect(hits, 2, "redaction hits (one key, one email)")


@check("traceweave: the tree names its slowest and its failed span")
def _():
    from traceweave.trace import (build_trace, critical_path_ms,
                                  failed_spans, slowest_span, total_ms)
    spans = build_trace()
    expect(total_ms(spans), 2140.0, "trace total")
    expect(slowest_span(spans)["name"], "llm-plan", "slowest span")
    expect([s["name"] for s in failed_spans(spans)],
           ["tool:billing_lookup"], "failed spans")
    expect_true(0 < critical_path_ms(spans) <= total_ms(spans),
                "critical path inside the total")


@check("promptwatch: v4 regresses past the gate and is held")
def _():
    from promptwatch.registry import QUALITY_GATE_DROP, compare, diff_versions, REGISTRY
    c = compare()
    expect(round(c["v3_quality"], 2), 0.89, "v3 quality")
    expect(round(c["v4_quality"], 2), 0.72, "v4 quality")
    expect_true(c["v3_quality"] - c["v4_quality"] >= QUALITY_GATE_DROP,
                "the drop must trip the quality gate")
    removed, added = diff_versions(REGISTRY["v3"], REGISTRY["v4"])
    expect_true(removed and added, "the diff must name lines both ways")


@check("judgeaudit: agreement measured; the verbosity bias is real")
def _():
    from judgeaudit.audit import audit
    r = audit()
    expect(r["agreement"], 0.75, "judge-human agreement")
    expect_true(r["verbose_wrong_mean"] > r["concise_right_mean"],
                "verbose wrong answers must outscore concise right ones")


@check("tokenledger: the storm is inside the bill, attributed")
def _():
    from obscommon import gen_events
    from tokenledger.ledger import ledger, retry_storm
    evs = gen_events(n=200, seed=42) + retry_storm()
    expect(len(evs), 240, "base + storm request count")
    led = ledger(evs)
    expect(round(led["total"], 4), 0.4083, "total token cost")
    expect(max(led["by_tenant"], key=led["by_tenant"].get), "globex",
           "top spender")
    expect(round(sum(led["by_feature"].values()), 4), 0.4083,
           "feature attribution reconciles with the total")


@check("p99hunt: generation owns the p99, not the model call's queue")
def _():
    from obscommon import STAGES, gen_events
    from p99hunt.profile import dominant_p99, profile
    prof = profile(gen_events(n=500, seed=42))
    expect(set(prof), set(STAGES), "profiled stages")
    expect(dominant_p99(prof), "generation_ms", "dominant p99 stage")


@check("decayradar: fires on decay, silent on a healthy window")
def _():
    from decayradar.drift import compare
    from obscommon import gen_events
    base = gen_events(n=200, seed=42)
    calm = compare(base, gen_events(n=200, seed=42))
    expect(calm["quality_drift"], False, "identical window must not fire")
    hot = compare(base, gen_events(n=200, seed=42, quality_shift=-0.18,
                                   halluc_rate=0.15))
    expect(hot["quality_drift"], True, "quality drift must fire")
    expect(hot["halluc_drift"], True, "hallucination drift must fire")
    expect(round(hot["quality_drop"], 2), 0.18, "measured quality drop")


@check("pagewise: burn-rate pages are exactly the real incidents")
def _():
    from pagewise.alerts import REAL_INCIDENTS, error_budget, simulate
    expect(round(error_budget(), 6), 1000.0,
           "monthly error budget at 99.9% SLO")
    sim = simulate()
    expect(set(sim["burn_pages"]), REAL_INCIDENTS, "burn-rate pages")
    expect(sim["burn_false"], [], "burn-rate false pages")
    expect(len(sim["naive_false"]), 4, "naive policy false pages")


@check("culprit: the first failure is the researcher, by measurement")
def _():
    from culprit.blame import downstream_of, first_failure, trace_graph
    ff = first_failure()
    expect(ff["agent"], "researcher", "first failing agent")
    expect(ff["score"], 0.21, "the failing check's score")
    expect(trace_graph()["researcher"], ["router"], "handoff chain")
    expect_true("drafter" in downstream_of("researcher"),
                "downstream agents are cleared, not blamed")


@check("watchstack: all checks pass; the review grades honestly")
def _():
    from watchstack.stack import review, run_checks
    checks, warnings = run_checks()
    expect(len(checks), 6, "stack check count")
    expect_true(all(ok for _, ok in checks), "every stack check passes")
    expect(len(warnings), 3, "warnings are named, not hidden")
    expect(quiet(review), (9, 13, 0),
           "checklist: 9 evidenced, 13 open, 0 blockers")


# ---------------------------------------------------------------- lab runs

def _lab_check(lab, first, last):
    @check(f"labs/{lab}: runs; first and last output lines pinned")
    def _():
        proc = subprocess.run(
            [sys.executable, str(ROOT / "labs" / lab / "demo.py")],
            capture_output=True, text=True, timeout=300, cwd=ROOT)
        if proc.returncode != 0:
            raise AssertionError(f"exit {proc.returncode}: "
                                 f"{proc.stderr.strip()[-300:]}")
        lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
        expect(lines[0], first, "first line")
        expect(lines[-1], last, "last line")


for _lab, _first, _last in LAB_RUNS:
    _lab_check(_lab, _first, _last)


# ---------------------------------------------------------------- hygiene

@check("tags: the lab start/finish scheme is documented in the README")
def _():
    readme = (ROOT / "README.md").read_text()
    for token in ("lab-01-start", "lab-13-start", "lab-01", "lab-13"):
        expect_true(token in readme, f"README does not name {token}")


@check("no hardcoded secrets in any program")
def _():
    # Credential-SHAPED values only: the logline package
    # legitimately NAMES secret keys ("api_key", "secret") — they
    # are the redaction list, not credentials — and it carries
    # ONE planted FAKE key fixture (an "sk-live-...-PLANTED-SECRET"
    # string that exists to be redacted on screen; it is not a
    # real credential and its hyphenated shape deliberately fails
    # the real-key patterns below). What must never appear is a
    # value shaped like a real key.
    import re as _re
    shapes = (_re.compile(r"sk-[A-Za-z0-9]{16,}"),
              _re.compile(r"gh[pous]_[A-Za-z0-9]{16,}"),
              _re.compile(r"AKIA[A-Z0-9]{16}"),
              _re.compile(r"xoxb-[A-Za-z0-9-]{10,}"),
              _re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"))
    for py in ROOT.rglob("*.py"):
        if py.name == "validate.py":
            continue
        text = py.read_text()
        for shape in shapes:
            expect_true(not shape.search(text),
                        f"credential-shaped value {shape.pattern!r} "
                        f"found in {py.name}")


@check("documentation: README maps every package, lab and lesson")
def _():
    readme = (ROOT / "README.md").read_text()
    for pkg in PACKAGES:
        expect_true(pkg in readme, f"README does not name {pkg}")
    for d in LAB_DIRS:
        expect_true(f"labs/{d}" in readme, f"README does not name labs/{d}")
    expect_true(readme.count("Lesson") >= 39,
                "README must list the 39 theory lessons by name")


def main() -> int:
    failed = [n for n, ok, _ in RESULTS if not ok]
    print()
    if failed:
        print(f"VALIDATION FAILED ({len(RESULTS) - len(failed)}/"
              f"{len(RESULTS)} passed): {failed}")
        return 1
    print(f"ALL CHECKS PASSED ({len(RESULTS)}/{len(RESULTS)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
