# Routing scenarios: results

Baseline = weeks (2, 3, 4) on 4.1 rules. After = weeks (6, 7, 8) on the scenario's rules.

| Scenario | Acceptance | Missed share | Median secs to accept | Median secs to fill callout | Unfilled | Slow cohort pings/wk | Quick cohort pings/wk | Busiest / quietest | Outer-area share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline (4.1, wks 2-4) | 79% | 4% | 43 | 50 | 0.0% | 15.6 | 21.1 | 31.7x | 38% |
| v4.1 | 82% | 3% | 40 | 48 | 0.0% | 14.9 | 21.0 | 28.7x | 35% |
| v4.2-current | 80% | 6% | 28 | 33 | 0.0% | 1.3 | 27.8 | 31.0x | 33% |
| fix-a-timeout-90 | 81% | 3% | 42 | 53 | 0.0% | 17.1 | 20.8 | 12.7x | 40% |
| fix-b-missed-not-penalized | 61% | 29% | 30 | 48 | 0.0% | 17.7 | 26.1 | 3.0x | 33% |
| fix-c-score-eases-back | 79% | 8% | 28 | 33 | 0.0% | 2.5 | 27.4 | 15.3x | 32% |
| fix-d-b-plus-c | 68% | 21% | 28 | 41 | 0.0% | 11.2 | 27.3 | 4.9x | 33% |

## Acceptance criteria

| Scenario | AC1 slow cohort >= 80% of baseline | AC2 nobody willing (>= 3/wk at baseline) < 50% of own baseline | AC3 acceptance >= baseline - 2 pts | AC4 unfilled <= baseline + 1 pt | AC5 outer share >= 4.2's | AC6 disengaged gets <= 2 pings/wk |
| --- | --- | --- | --- | --- | --- | --- |
| v4.1 | PASS (96%) | FAIL (TEST-11 at 33%) | PASS (82% vs 79%) | PASS (0.0% vs 0.0%) | PASS (35%) | PASS (0.0) |
| v4.2-current | FAIL (9%) | FAIL (TEST-09 at 4%) | PASS (80% vs 79%) | PASS (0.0% vs 0.0%) | PASS (33%) | PASS (0.3) |
| fix-a-timeout-90 | PASS (110%) | PASS (TEST-09 at 66%) | PASS (81% vs 79%) | PASS (0.0% vs 0.0%) | PASS (40%) | PASS (0.7) |
| fix-b-missed-not-penalized | PASS (113%) | PASS (TEST-11 at 89%) | FAIL (61% vs 79%) | PASS (0.0% vs 0.0%) | PASS (33%) | PASS (1.0) |
| fix-c-score-eases-back | FAIL (16%) | FAIL (TEST-09 at 8%) | PASS (79% vs 79%) | PASS (0.0% vs 0.0%) | FAIL (32%) | PASS (1.3) |
| fix-d-b-plus-c | FAIL (72%) | FAIL (TEST-11 at 41%) | FAIL (68% vs 79%) | PASS (0.0% vs 0.0%) | PASS (33%) | PASS (1.7) |

## Pings per week by responder (baseline -> after)

| Responder | Cohort | Area | v4.1 | v4.2-current | fix-a-timeout-90 | fix-b-missed-not-penalized | fix-c-score-eases-back | fix-d-b-plus-c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-01 | quick | central | 17 -> 29 | 17 -> 31 | 17 -> 25 | 17 -> 30 | 17 -> 31 | 17 -> 31 |
| TEST-02 | quick | central | 25 -> 20 | 25 -> 29 | 25 -> 19 | 25 -> 26 | 25 -> 28 | 25 -> 28 |
| TEST-03 | quick | outer | 21 -> 14 | 21 -> 24 | 21 -> 18 | 21 -> 22 | 21 -> 23 | 21 -> 23 |
| TEST-04 | steady | central | 0 -> 0 | 0 -> 22 | 0 -> 2 | 0 -> 21 | 0 -> 23 | 0 -> 19 |
| TEST-05 | steady | outer | 17 -> 15 | 17 -> 17 | 17 -> 13 | 17 -> 16 | 17 -> 16 | 17 -> 17 |
| TEST-06 | steady | outer | 2 -> 9 | 2 -> 16 | 2 -> 5 | 2 -> 14 | 2 -> 15 | 2 -> 13 |
| TEST-07 | steady | central | 32 -> 25 | 32 -> 31 | 32 -> 22 | 32 -> 28 | 32 -> 30 | 32 -> 29 |
| TEST-08 | slow | central | 6 -> 25 | 6 -> 1 | 6 -> 20 | 6 -> 10 | 6 -> 2 | 6 -> 6 |
| TEST-09 | slow | central | 24 -> 12 | 24 -> 1 | 24 -> 16 | 24 -> 24 | 24 -> 2 | 24 -> 19 |
| TEST-10 | slow | outer | 8 -> 15 | 8 -> 2 | 8 -> 12 | 8 -> 14 | 8 -> 3 | 8 -> 9 |
| TEST-11 | slow | outer | 25 -> 8 | 25 -> 2 | 25 -> 20 | 25 -> 22 | 25 -> 3 | 25 -> 10 |
| TEST-12 | disengaged | central | 0 -> 0 | 0 -> 0 | 0 -> 1 | 0 -> 1 | 0 -> 1 | 0 -> 2 |
