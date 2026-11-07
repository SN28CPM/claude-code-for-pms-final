# Release 4.2: acceptance criteria from the data, and the test result

**Project:** Jedi Order · **Date:** 7 Nov 2026 · **Data:** `rook.pings`, `rook.callouts`, `rook.support_tickets`, 29 Jun – 6 Sep 2026

## How the criteria were set

The data gives us six normal weeks before 4.2 (29 Jun – 9 Aug). For each measure,
the criterion is: **stay within the range of those six weeks.** The worst week
before 4.2 sets the limit, so ordinary week-to-week wobble passes and a real change
fails. 4.2 is then tested week by week on the four weeks after release. The release
week (from 10 Aug) includes two days before 4.2 shipped on Wednesday 12 Aug.

These replace the placeholder thresholds in `dispatch-4.2-requirements.md`, where the
data allows. The same criteria can test the fix.

## Acceptance criteria

| ID | Criterion | Before 4.2 (6 weeks) | Pass if, every week | Source |
| --- | --- | --- | --- | --- |
| AC1 | Acceptance rate (pings taken) | 76.8% avg (75.0–77.9%) | ≥ 75% | pings |
| AC2 | Missed pings (no answer in time) | 2.3% avg (1.2–3.4%) | ≤ 3.5% | pings |
| AC3 | Turned-down pings | 20.9% avg (20.0–22.2%) | ≤ 23% | pings |
| AC4 | Callouts nobody took | 5.1% avg (2.9–8.3%) | ≤ 8.3% each week, and ≤ 6% over 4 weeks | callouts + pings |
| AC5 | Pings needed per callout | 1.22–1.26 | ≤ 1.26 | pings |
| AC6 | Time to reach the responder who takes it (callouts needing 2+ pings, median) | 17–29 s | ≤ 29 s | pings (sent times) |
| AC7 | No responder falls below half their own usual weekly pings | all 16 steady | nobody below 50% | pings, per responder |
| AC8 | No responder takes on more than 1.5× their usual weekly pings | all 16 steady | nobody above 150% | pings, per responder |
| AC9 | Callout-related tickets ("gone before I could answer" + "quiet responder") | 0–1 a week | ≤ 1 a week | support_tickets |

AC6 measures what 4.2 promised: "pings that go unanswered move to the next responder
sooner". It's the time from the first ping to the ping that the eventual taker
receives. It can't include their answer time, which isn't recorded.

## Test result: 4.2 fails 8 of 9

| ID | Week of 10 Aug (release) | 17 Aug | 24 Aug | 31 Aug | Result |
| --- | --- | --- | --- | --- | --- |
| AC1 Acceptance ≥ 75% | 54.2% ✗ | 65.8% ✗ | 66.7% ✗ | 72.7% ✗ | **Fail** |
| AC2 Missed ≤ 3.5% | 21.5% ✗ | 17.7% ✗ | 14.8% ✗ | 12.7% ✗ | **Fail** |
| AC3 Turned down ≤ 23% | 24.3% ✗ | 16.5% ✓ | 18.5% ✓ | 14.5% ✓ | **Pass** after the release week |
| AC4 Nobody took it ≤ 8.3% | 12.7% ✗ | 14.0% ✗ | 12.9% ✗ | 5.5% ✓ | **Fail** (4-week total 11.2%, limit 6%) |
| AC5 Pings per callout ≤ 1.26 | 1.61 ✗ | 1.31 ✗ | 1.31 ✗ | 1.30 ✗ | **Fail** |
| AC6 Reach the taker ≤ 29 s | 61 s ✗ | 61 s ✗ | 61 s ✗ | 40 s ✗ | **Fail** |
| AC7 Nobody below 50% | | | | 4 responders ✗ | **Fail** |
| AC8 Nobody above 150% | | | | 2 responders ✗ | **Fail** |
| AC9 Callout tickets ≤ 1/wk | 7 ✗ | 11 ✗ | 15 ✗ | 10 ✗ | **Fail** |

AC7 and AC8 compare 24 Aug – 6 Sep against the six weeks before 4.2:

| Responder | Usual pings/wk | 24 Aug – 6 Sep | Share of usual |
| --- | --- | --- | --- |
| Farlight | 12.0 | 0.5 | **4%** ✗ |
| The Undertow | 12.0 | 1.0 | **8%** ✗ |
| Vesper | 13.8 | 1.5 | **11%** ✗ |
| Meteor Mite | 11.2 | 1.5 | **13%** ✗ |
| Corporal Ashgrove · Halfmoon | 10.0 · 11.0 | 7.0 · 8.0 | 70% · 73% |
| Ten others | 6.2–15.0 | 8.0–20.5 | 122–146% |
| Sgt. Falkirk | 10.0 | 15.5 | **155%** ✗ |
| The Gale | 13.0 | 20.5 | **158%** ✗ |

## What the test says

- **4.2 missed its own goal.** It cut the ping wait so callouts would move on
  sooner. Instead, reaching the responder who takes the job went from a median of
  about 26 seconds to 61 (AC6). Before 4.2, most pass-ons were quick turn-downs.
  After it, most are misses that use up the full 60 seconds.
- **The damage is misses, not refusals.** Turn-downs went back inside their normal
  range after the release week (AC3). Every miss-related measure failed.
- **The effect is getting smaller but hasn't gone away.** By 31 Aug, acceptance
  (72.7%) and missed pings (12.7%) were improving, and unfilled callouts were back
  in range. But the four quiet responders were still at 4–13% of their usual pings.
  That points to the scoring problem, not a passing dip.

## What couldn't be tested

- **Time-to-accept:** the pings table doesn't record how long a responder took to
  answer.
- **Whether wide-area responders gained, which was 4.2's purpose:** the data has
  no travel times and doesn't mark who is a wide-area responder.
- **Coverage gaps:** callouts don't record which skills they needed.

**One more thing to check, not a criterion:** callouts per week fell from 137–144
before 4.2 to 110–127 after. Rook doesn't control how many callouts come in, so this
isn't a pass or fail. But it could be August seasonality, or handlers going around
Dispatch. Ask Ravi and Nadia.
