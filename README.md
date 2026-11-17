# AI Observability in Production — Skool Course 9 companion code

The working code for **Skool Course 9 — AI Observability in Production** (community: *AI Agents in Production*). Eleven companion packages on one shared telemetry module (`obscommon.py`), plus thirteen hands-on labs. Python standard library only — no installs, no network, deterministic output: every number in this course reproduces exactly, on every machine, on every run.

Run any demo:

```bash
python3 -m blindspot.baseline   # a section demo (from the repo root)
python3 labs/lab-02/demo.py     # the same demo as a lab
python3 labs/lab-01/demo.py     # Lab 1: the observability tour
python3 validate.py             # check the whole repo
```

## Course map

Thirty-nine theory lessons in thirteen sections, plus thirteen hands-on labs. Eleven sections ship one demo package each; the labs are those demos in start/finish form (see *How the labs work*), plus the authored tour and the capstone review.

| Section | Package | Demo | What it proves |
|---|---|---|---|
| 1. Introduction | `labs/lab-01/` | `observability-tour` | one dataset, eleven watchers, and the map of everything after |
| 2. Why AI Systems Fail Silently | `blindspot/` | `blindspot` | infrastructure stays green while answer quality falls off a cliff |
| 3. Log Everything That Matters | `logline/` | `logline` | events emitted, validated, and stripped of the planted secret |
| 4. Follow Every Request | `traceweave/` | `traceweave` | one request as a span tree, and the failed tool call named |
| 5. Prompts Are Production Code | `promptwatch/` | `promptwatch` | two prompt versions diffed, graded, and one regression flagged |
| 6. Eval Harnesses in Production | `judgeaudit/` | `judgeaudit` | the judge graded against human labels, its bias measured in the open |
| 7. Cost and Token Tracking | `tokenledger/` | `tokenledger` | a week of traffic attributed, and the retry storm priced |
| 8. Buy Back Your p99 | `p99hunt/` | `p99hunt` | the stage that owns the p99 named from the traces — not the model |
| 9. Catching Silent Decay | `decayradar/` | `decayradar` | two windows compared; the radar fires on decay, silent on health |
| 10. Page Only When It Matters | `pagewise/` | `pagewise` | naive paging versus burn-rate paging on the same incident history |
| 11. Debugging RAG Pipelines | — | — | no demo lesson in this section — the evidence kit is a method, graded inside the capstone |
| 12. Debugging Multi-Agent Systems | `culprit/` | `culprit` | the fleet's first failing agent found by measurement, not seniority |
| 13. Ship It | `watchstack/` | `watchstack` | the whole course in one stack, shipped with its warnings named |

## Theory lessons

### Introduction (`introduction/`)

- Lesson 1 — Welcome: Green Dashboards, Wrong Answers (Udemy Lesson 1)
- Lesson 2 — Course Map and the One Story (Udemy Lesson 2)

### Why AI Systems Fail Silently (`blindspot/`)

- Lesson 3 — The Observability Gap (Udemy Lesson 3)
- Lesson 4 — Signals Worth Keeping (Udemy Lesson 4)
- Lesson 5 — The Business Case for Watching (Udemy Lesson 6)

### Log Everything That Matters (`logline/`)

- Lesson 6 — Structured Telemetry for LLM Apps (Udemy Lesson 7)
- Lesson 7 — What Must Never Be Logged (Udemy Lesson 8)
- Lesson 8 — Telemetry at Scale (Udemy Lesson 10)

### Follow Every Request (`traceweave/`)

- Lesson 9 — Tracing Agent Workflows (Udemy Lesson 11)
- Lesson 10 — Reading a Trace Like a Detective (Udemy Lesson 12)
- Lesson 11 — Tracing in the Real Stack (Udemy Lesson 14)

### Prompts Are Production Code (`promptwatch/`)

- Lesson 12 — The Prompt Is a Deployable (Udemy Lesson 15)
- Lesson 13 — Monitoring Prompts and Responses (Udemy Lesson 16)
- Lesson 14 — Prompt Incidents and Rollback (Udemy Lesson 18)

### Eval Harnesses in Production (`judgeaudit/`)

- Lesson 15 — From Release Gate to Always-On (Udemy Lesson 19)
- Lesson 16 — Judging the Judge (Udemy Lesson 20)
- Lesson 17 — Eval Operations Over Time (Udemy Lesson 22)

### Cost and Token Tracking (`tokenledger/`)

- Lesson 18 — Every Request Burns Money (Udemy Lesson 23)
- Lesson 19 — Budgets, Quotas, and Waste (Udemy Lesson 24)
- Lesson 20 — Cost Observability in the Stack (Udemy Lesson 26)

### Buy Back Your p99 (`p99hunt/`)

- Lesson 21 — Latency Has Anatomy (Udemy Lesson 27)
- Lesson 22 — Profiling the Pipeline (Udemy Lesson 28)
- Lesson 23 — Latency SLOs and Honest Speedups (Udemy Lesson 30)

### Catching Silent Decay (`decayradar/`)

- Lesson 24 — Drift Is the Default (Udemy Lesson 31)
- Lesson 25 — Hallucination Signals (Udemy Lesson 32)
- Lesson 26 — Responding to Decay (Udemy Lesson 34)

### Page Only When It Matters (`pagewise/`)

- Lesson 27 — SLOs for Nondeterministic Systems (Udemy Lesson 35)
- Lesson 28 — Alert Design That Respects the Pager (Udemy Lesson 36)
- Lesson 29 — Incident Practice for AI Systems (Udemy Lesson 38)

### Debugging RAG Pipelines (`rag-debugging/`)

- Lesson 30 — When Retrieval Goes Wrong (Udemy Lesson 39)
- Lesson 31 — The Evidence Kit for RAG (Udemy Lesson 40)
- Lesson 32 — Three RAG Postmortems (Udemy Lesson 41)
- Lesson 33 — Keeping RAG Honest Continuously (Udemy Lesson 42)

### Debugging Multi-Agent Systems (`culprit/`)

- Lesson 34 — Finding the Guilty Agent (Udemy Lesson 43)
- Lesson 35 — Per-Agent Telemetry (Udemy Lesson 44)
- Lesson 36 — Fleet Operations and Guardrails (Udemy Lesson 46)

### Ship It (`watchstack/`)

- Lesson 37 — Architecture of the Observability Stack (Udemy Lesson 47)
- Lesson 38 — Wiring the Support Service (Udemy Lesson 48)
- Lesson 39 — Alerts, SLOs, and the On-Call Contract (Udemy Lesson 49)

## Hands-On Labs: Build It Yourself

| Lab | Program | Source |
|---|---|---|
| Lab 1 | `observability-tour` (`labs/lab-01/`) | authored for Skool (the tour) |
| Lab 2 | `blindspot` (`labs/lab-02/`) | Udemy Lesson 5 DEMO |
| Lab 3 | `logline` (`labs/lab-03/`) | Udemy Lesson 9 DEMO |
| Lab 4 | `traceweave` (`labs/lab-04/`) | Udemy Lesson 13 DEMO |
| Lab 5 | `promptwatch` (`labs/lab-05/`) | Udemy Lesson 17 DEMO |
| Lab 6 | `judgeaudit` (`labs/lab-06/`) | Udemy Lesson 21 DEMO |
| Lab 7 | `tokenledger` (`labs/lab-07/`) | Udemy Lesson 25 DEMO |
| Lab 8 | `p99hunt` (`labs/lab-08/`) | Udemy Lesson 29 DEMO |
| Lab 9 | `decayradar` (`labs/lab-09/`) | Udemy Lesson 33 DEMO |
| Lab 10 | `pagewise` (`labs/lab-10/`) | Udemy Lesson 37 DEMO |
| Lab 11 | `culprit` (`labs/lab-11/`) | Udemy Lesson 45 DEMO |
| Lab 12 | `watchstack` (`labs/lab-12/`) | Udemy Lesson 50 DEMO |
| Lab 13 | `watchstack` (`labs/lab-13/`) | Udemy Lesson 51 DEMO (review) |

## How the labs work

Every lab exists twice in git: a **start tag** (`lab-01-start` … `lab-13-start`), where the program's structure and data are real but the core bodies are left to you, and the **finish tag** (`lab-01` … `lab-13`), where the program is complete and verified. You work at the start tag; you check yourself against the finish tag. Each lab's README pins the first and last output lines its finish state must print, and `validate.py` re-checks them whenever you ask.

## Provenance

Adapted for Skool from the Udemy Course 9 companion repo (https://github.com/josyulank4/ai-observability-course): the eleven packages and `obscommon.py` are copied verbatim — the code students ran on Udemy is the code they run here. The labs layer (start/finish tags, per-lab programs, the authored observability tour, and the capstone review program) is the Skool addition.
