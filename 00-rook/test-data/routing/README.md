# Routing test data

Synthetic test data for checking proposed fixes to the post-4.2 drop in pings
before anything ships. It goes with requirements B3/B4 in
`dispatch-4.2-requirements.md`. Every responder is made up (TEST-01 to TEST-12).
No real responder records are used.

## What's here

| File | What it is |
| --- | --- |
| `responders.csv` | 12 test responders. Each has an answer-speed cohort, an area (central or outer, where outer means wide-area), a location, capability tags, and the chance they'd say yes when they answer |
| `callouts.csv` | 8 weeks of callouts (20 a day, 1,120 in total), each with a time, location and required tag |
| `responses.csv` | For every callout and responder: whether they're available, travel minutes, seconds to answer (blank means no answer), and whether they'd take it |
| `generate.py` | Rebuilds the three CSVs. It's seeded, so it gives the same data every run |
| `simulate.py` | Runs the data through the real `routing.py` and `history.py` from `00-rook/code/dispatch-routing`, once per scenario |
| `out/pings_<scenario>.csv` | The resulting pings, with the same columns as the `rook.pings` table: `callout_number, responder, sent_at, outcome` |
| `out/summary.md` | Metrics, acceptance-criteria pass/fail, and pings per week for each responder |

Run it from this folder:

```
python3 generate.py
python3 simulate.py
```

## How the data is built

The responders are designed to isolate one variable: **how fast they answer**.
- Everyone who answers says yes 85% of the time.
- They differ only in answer speed:
  - **quick**: about 18s
  - **steady**: about 42s
  - **slow**: about 70s. This is the "on the stairs" or "one boot on" responder from the
    interviews. Nearly always inside 90 seconds, mostly past 60.
  - **disengaged** (TEST-12): answers fast but says yes only 25% of the time. A fix
    must *not* push this responder back up the list.
- There's a 3% chance of no answer at all (out of signal), and each responder is
  available 75% of the time.

`responses.csv` is fixed in advance. So every scenario faces the same callouts and the
same people answering the same way, and only the routing rules change. Every scenario runs
weeks 1–4 on 4.1 rules, then switches for weeks 5–8, the way 4.2 landed on 12 August.

## Scenarios

| Scenario | Ping wait | Weights (proximity / acceptance) | Missed ping lowers score? | Score eases back toward neutral? |
| --- | --- | --- | --- | --- |
| v4.1 | 90s | 0.45 / 0.40 | yes | no |
| v4.2-current | 60s | 0.60 / 0.25 | yes | no |
| fix-a-timeout-90 | 90s | 0.60 / 0.25 | yes | no |
| fix-b-missed-not-penalized | 60s | 0.60 / 0.25 | no (turned down still does) | no |
| fix-c-score-eases-back | 60s | 0.60 / 0.25 | yes | yes, 10% a day (the 2019 TODO in `history.py`) |
| fix-d-b-plus-c | 60s | 0.60 / 0.25 | no | yes |

## Acceptance criteria checked

The thresholds are placeholders for the team to agree, not decided targets.

- **AC1**: Slow-cohort pings per week are at least 80% of the 4.1 baseline.
- **AC2**: No willing responder (3 or more pings a week at baseline) drops below 50% of their own baseline.
- **AC3**: Acceptance rate is no more than 2 points below the baseline.
- **AC4**: Unfilled callouts are no more than 1 point above the baseline.
- **AC5**: The outer-area (wide-area) share of taken callouts is at or above 4.2's, so we keep the 4.2 win.
- **AC6**: The disengaged responder gets no more than 2 pings a week.

## Results from the current data

These cover weeks 6–8 against a 4.1 baseline in weeks 2–4. Full tables are in `out/summary.md`.

| Scenario | Slow cohort pings/wk (baseline 15.6) | Acceptance (baseline 79%) | Median secs to fill a callout (baseline 50) | AC1–6 |
| --- | --- | --- | --- | --- |
| v4.2-current | **1.3** | 80% | 33 | Fails AC1, AC2 |
| fix-a-timeout-90 | 17.1 | 81% | 53 | **Passes all** |
| fix-b-missed-not-penalized | 17.7 | **61%** | 48 | Fails AC3 |
| fix-c-score-eases-back | 2.5 | 79% | 33 | Fails AC1, AC2, AC5 |
| fix-d-b-plus-c | 11.2 | 68% | 41 | Fails AC1, AC2, AC3 |

What it shows:
- **The current 4.2 rules reproduce the pattern in the tickets.** The slow cohort falls from
  about 16 pings a week to about 1, while the quick cohort rises from 21 to 28. That's the
  same "dead quiet next to on fire" split that Kip described.
- **Restoring the 90-second ping wait, and keeping the 4.2 weights, passes every check.** It
  also keeps the outer-area share (40%) above 4.2's.
- **Not penalizing missed pings brings slow responders back, but they keep missing at 60
  seconds.** Acceptance drops to 61%, and 29% of pings are missed.
- **Easing scores back toward neutral on its own barely helps.** A responder who keeps
  missing just drops again.

## Limits

- This is one seeded run, so the numbers for individual responders swing a lot from run to run.
  Even the unchanged 4.1 run fails AC2 for one responder, because a responder who sinks to
  the bottom is rarely asked again (there's no easing back). Trust the cohort-level
  results more than any single responder's.
- The answer speeds and availability are assumptions, not measured. The real `pings`
  table doesn't record how many seconds a responder took to answer. That number is what
  requirement A4 asks for, and it should replace the assumed speeds here once we have it.
- This tests the ranking rules only. It doesn't test phone delivery, the console, or the
  handler and responder visibility work (B1/B2).
