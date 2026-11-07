# Stress test results

Timeline: weeks 1-4 on 4.1, weeks 5-8 on 4.2, fix from week 9. Before = weeks 2-4, after = weeks 10-12. Numbers are medians over 20 random seeds, with the 10th–90th percentile range in brackets. Synthetic responders only.

## 1. Every fix, default assumptions (slow responders answer in about 70s)

Before (4.1): slow responders 14.3 (11.7–21.4) pings/wk, acceptance 82%, median fill 51s.

| Fix | Slow pings/wk | Quick pings/wk | Busiest responder/wk | Acceptance per ping | Unfilled | Median secs to fill | Pings per callout | Disengaged/wk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4.2 left as is | 0.8 (0.4–1.5) | 26.4 (23.8–28.4) | 34.8 (30.3–40.0) | 79% | 0.0% | 35 | 1.26 | 0.3 (0.0–1.0) |
| Back to 90s | 2.2 (0.6–6.3) | 23.6 (20.4–25.8) | 31.5 (28.0–37.0) | 82% | 0.0% | 37 | 1.22 | 0.0 (0.0–0.7) |
| Back to 90s + fresh start | 15.6 (9.3–18.2) | 17.9 (13.8–21.8) | 26.8 (22.3–32.7) | 82% | 0.0% | 50 | 1.22 | 0.3 (0.0–1.0) |
| 60s, late answers free | 0.9 (0.6–1.8) | 25.3 (23.2–27.4) | 33.3 (30.3–40.0) | 79% | 0.0% | 36 | 1.26 | 0.3 (0.0–1.0) |
| 60s, late answers free + fresh start | 7.9 (5.4–9.9) | 24.8 (22.2–28.7) | 33.5 (30.7–39.0) | 70% | 0.0% | 40 | 1.42 | 0.8 (0.0–1.3) |
| Proposal, no fresh start | 1.6 (0.8–5.7) | 24.6 (23.2–28.1) | 32.5 (30.3–38.7) | 79% | 0.0% | 37 | 1.26 | 0.3 (0.0–0.7) |
| Proposal + fresh start | 19.2 (13.6–22.8) | 22.1 (18.0–26.1) | 34.3 (28.3–37.0) | 65% | 0.0% | 50 | 1.54 | 0.7 (0.0–1.3) |
| Proposal + fresh start + ease-back | 17.7 (12.8–21.8) | 22.1 (17.3–27.0) | 33.7 (29.7–38.7) | 66% | 0.0% | 49 | 1.52 | 2.0 (1.0–3.7) |
| First draft (late no free) + fresh start | 22.8 (17.2–27.1) | 19.6 (14.8–23.0) | 32.8 (28.0–37.3) | 63% | 0.0% | 56 | 1.58 | 0.5 (0.0–1.3) |

### How often each acceptance check passes (out of 20 seeds)

| Fix | AC1 | AC2 | AC3 | AC4 | AC5 | AC6 |
| --- | --- | --- | --- | --- | --- | --- |
| 4.2 left as is | 0 | 0 | 9 | 20 | 20 | 20 |
| Back to 90s | 0 | 0 | 18 | 20 | 19 | 20 |
| Back to 90s + fresh start | 14 | 2 | 18 | 20 | 18 | 20 |
| 60s, late answers free | 0 | 0 | 9 | 20 | 15 | 20 |
| 60s, late answers free + fresh start | 3 | 1 | 0 | 20 | 15 | 20 |
| Proposal, no fresh start | 0 | 0 | 8 | 20 | 17 | 20 |
| Proposal + fresh start | 17 | 4 | 0 | 20 | 18 | 19 |
| Proposal + fresh start + ease-back | 19 | 4 | 0 | 20 | 18 | 11 |
| First draft (late no free) + fresh start | 20 | 2 | 0 | 20 | 18 | 20 |

AC1 slow cohort ≥ 80% of before · AC2 no willing responder below half their own before · AC3 acceptance per ping within 2 pts · AC4 unfilled within 1 pt · AC5 wide-area share ≥ 4.2's · AC6 disengaged ≤ 2 pings/wk

## 2. What if our guess about answer speed is wrong? (slow pings/wk after, 10 seeds)

| Slow responders answer in about… | 4.2 left as is | Back to 90s + fresh start | Proposal + fresh start | Proposal: median secs to fill |
| --- | --- | --- | --- | --- |
| 62s | 1.2 (0.8–1.5) | 14.8 (9.3–16.8) | 17.2 (10.8–23.0) | 48 |
| 70s | 1.1 (0.8–1.5) | 14.9 (9.3–16.7) | 18.0 (13.6–27.5) | 48 |
| 80s | 1.1 (0.8–1.4) | 8.0 (7.4–12.8) | 15.9 (9.8–26.2) | 48 |
| 100s | 1.1 (0.8–1.4) | 1.1 (0.8–1.3) | 14.4 (11.2–21.6) | 46 |
| 130s | 1.1 (0.8–1.4) | 0.9 (0.6–1.3) | 10.6 (7.5–17.6) | 42 |

## 3. Patchy signal and fewer people free (10 seeds)

| Condition | Fix | Slow pings/wk | Unfilled | Median secs to fill |
| --- | --- | --- | --- | --- |
| No answer 10% of the time | 4.2 left as is | 1.8 (1.2–2.4) | 0.4% | 38 |
| No answer 10% of the time | Back to 90s + fresh start | 16.1 (9.2–19.1) | 0.0% | 57 |
| No answer 10% of the time | Proposal + fresh start | 19.0 (17.1–25.2) | 0.0% | 58 |
| Only 50% of people free | 4.2 left as is | 2.5 (2.2–3.7) | 1.4% | 36 |
| Only 50% of people free | Back to 90s + fresh start | 14.3 (13.2–16.4) | 0.2% | 50 |
| Only 50% of people free | Proposal + fresh start | 16.4 (14.8–20.2) | 0.1% | 48 |
| Only 30% of people free | 4.2 left as is | 6.5 (5.6–7.6) | 8.9% | 35 |
| Only 30% of people free | Back to 90s + fresh start | 13.6 (11.9–14.4) | 2.8% | 48 |
| Only 30% of people free | Proposal + fresh start | 15.4 (14.1–17.2) | 2.7% | 48 |

## 4. Gaming check: a responder who waits past 60s, then mostly says no (10 seeds)

| Fix | Late-decliner pings/wk | Disengaged (quick no) pings/wk |
| --- | --- | --- |
| 4.2 left as is | 0.7 (0.0–0.7) | 0.3 (0.0–0.7) |
| First draft (late no free) + fresh start | 6.2 (1.7–14.0) | 0.3 (0.0–0.7) |
| Proposal + fresh start | 0.7 (0.3–1.0) | 0.7 (0.3–1.0) |
