# Keeping the 60-second ping wait: results

Same test data and baseline as summary.md. Ping wait is 60s in every scenario except the 4.1 baseline and the fix-a reference.

| Scenario | Acceptance | Missed share | Median secs to fill callout | Unfilled | Slow cohort pings/wk | Quick cohort pings/wk | Outer-area share | Disengaged pings/wk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline (4.1, wks 2-4) | 79% | 4% | 50 | 0.0% | 15.6 | 21.1 | 38% | 0.3 |
| v4.1 | 82% | 3% | 48 | 0.0% | 14.9 | 21.0 | 35% | 0.0 |
| v4.2-current | 80% | 6% | 33 | 0.0% | 1.3 | 27.8 | 33% | 0.3 |
| fix-a-timeout-90 (reference) | 81% | 3% | 53 | 0.0% | 17.1 | 20.8 | 40% | 0.7 |
| e1-late-answers-free | 62% | 28% | 48 | 0.0% | 16.8 | 25.8 | 34% | 0.7 |
| e2-ping-stays-open | 63% | 25% | 58 | 0.0% | 23.0 | 25.6 | 40% | 0.7 |
| e3-stays-open-plus-ease-back | 62% | 26% | 60 | 0.0% | 23.3 | 24.3 | 42% | 1.3 |
| e4-stays-open-late-no-costs | 64% | 24% | 52 | 0.0% | 20.3 | 26.7 | 37% | 0.7 |
| e4-from-floored-no-reset | 80% | 7% | 36 | 0.0% | 2.1 | 25.6 | 34% | 1.0 |
| e4-from-floored-with-reset | 66% | 20% | 48 | 0.0% | 16.6 | 25.4 | 41% | 1.0 |

## Acceptance criteria (same as summary.md)

| Scenario | AC1 slow cohort | AC2 nobody willing < 50% | AC3 acceptance | AC4 unfilled | AC5 outer share | AC6 disengaged |
| --- | --- | --- | --- | --- | --- | --- |
| v4.1 | PASS (96%) | FAIL (TEST-11 at 33%) | PASS (82% vs 79%) | PASS (0.0%) | PASS (35%) | PASS (0.0) |
| v4.2-current | FAIL (9%) | FAIL (TEST-09 at 4%) | PASS (80% vs 79%) | PASS (0.0%) | PASS (33%) | PASS (0.3) |
| fix-a-timeout-90 (reference) | PASS (110%) | PASS (TEST-09 at 66%) | PASS (81% vs 79%) | PASS (0.0%) | PASS (40%) | PASS (0.7) |
| e1-late-answers-free | PASS (108%) | PASS (TEST-11 at 77%) | FAIL (62% vs 79%) | PASS (0.0%) | PASS (34%) | PASS (0.7) |
| e2-ping-stays-open | PASS (148%) | PASS (TEST-07 at 88%) | FAIL (63% vs 79%) | PASS (0.0%) | PASS (40%) | PASS (0.7) |
| e3-stays-open-plus-ease-back | PASS (150%) | PASS (TEST-07 at 61%) | FAIL (62% vs 79%) | PASS (0.0%) | PASS (42%) | PASS (1.3) |
| e4-stays-open-late-no-costs | PASS (130%) | PASS (TEST-11 at 91%) | FAIL (64% vs 79%) | PASS (0.0%) | PASS (37%) | PASS (0.7) |
| e4-from-floored-no-reset | FAIL (13%) | FAIL (TEST-09 at 0%) | PASS (80% vs 79%) | PASS (0.0%) | PASS (34%) | PASS (1.0) |
| e4-from-floored-with-reset | PASS (106%) | PASS (TEST-11 at 60%) | FAIL (66% vs 79%) | PASS (0.0%) | PASS (41%) | PASS (1.0) |

## Pings per week by responder (baseline -> after)

| Responder | Cohort | v4.1 | v4.2-current | fix-a-timeout-90 (reference) | e1-late-answers-free | e2-ping-stays-open | e3-stays-open-plus-ease-back | e4-stays-open-late-no-costs | e4-from-floored-no-reset | e4-from-floored-with-reset |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-01 | quick | 17 -> 29 | 17 -> 31 | 17 -> 25 | 17 -> 28 | 17 -> 30 | 17 -> 30 | 17 -> 29 | 17 -> 26 | 17 -> 27 |
| TEST-02 | quick | 25 -> 20 | 25 -> 29 | 25 -> 19 | 25 -> 27 | 25 -> 23 | 25 -> 20 | 25 -> 27 | 25 -> 28 | 25 -> 26 |
| TEST-03 | quick | 21 -> 14 | 21 -> 24 | 21 -> 18 | 21 -> 23 | 21 -> 23 | 21 -> 23 | 21 -> 24 | 21 -> 23 | 21 -> 23 |
| TEST-04 | steady | 0 -> 0 | 0 -> 22 | 0 -> 2 | 0 -> 21 | 0 -> 3 | 0 -> 12 | 0 -> 4 | 0 -> 27 | 0 -> 3 |
| TEST-05 | steady | 17 -> 15 | 17 -> 17 | 17 -> 13 | 17 -> 17 | 17 -> 16 | 17 -> 13 | 17 -> 16 | 17 -> 17 | 17 -> 18 |
| TEST-06 | steady | 2 -> 9 | 2 -> 16 | 2 -> 5 | 2 -> 14 | 2 -> 7 | 2 -> 13 | 2 -> 7 | 2 -> 14 | 2 -> 18 |
| TEST-07 | steady | 32 -> 25 | 32 -> 31 | 32 -> 22 | 32 -> 28 | 32 -> 28 | 32 -> 19 | 32 -> 29 | 32 -> 32 | 32 -> 29 |
| TEST-08 | slow | 6 -> 25 | 6 -> 1 | 6 -> 20 | 6 -> 10 | 6 -> 25 | 6 -> 26 | 6 -> 23 | 6 -> 0 | 6 -> 17 |
| TEST-09 | slow | 24 -> 12 | 24 -> 1 | 24 -> 16 | 24 -> 24 | 24 -> 27 | 24 -> 24 | 24 -> 24 | 24 -> 0 | 24 -> 23 |
| TEST-10 | slow | 8 -> 15 | 8 -> 2 | 8 -> 12 | 8 -> 14 | 8 -> 15 | 8 -> 17 | 8 -> 12 | 8 -> 0 | 8 -> 12 |
| TEST-11 | slow | 25 -> 8 | 25 -> 2 | 25 -> 20 | 25 -> 19 | 25 -> 25 | 25 -> 25 | 25 -> 23 | 25 -> 8 | 25 -> 15 |
| TEST-12 | disengaged | 0 -> 0 | 0 -> 0 | 0 -> 1 | 0 -> 1 | 0 -> 1 | 0 -> 1 | 0 -> 1 | 0 -> 1 | 0 -> 1 |
