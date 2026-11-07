# Solution brief: bring quiet responders back, keep the 60-second ping wait

**For:** Helen Achebe · **From:** Rook Dispatch PM · **Date:** 7 Nov 2026 · **Status:** draft for discussion

## The problem

Since 4.2, a ping moves to the next responder after 60 seconds instead of 90.
Some responders need a little over a minute to reach their phone: on the stairs,
gloves on, one boot on. Those pings now count as *missed*, and the routing code
treats a miss exactly like saying no. The score never recovers on its own, so a
few bad days push someone to the bottom of the list, where they're rarely asked
again. Four responders (Farlight, The Undertow, Vesper, Meteor Mite) went from
about 12 pings a week to about 1. Their home-area work moved to responders from
other areas, and ten others now carry the load (up to 21 pings a week). Handlers
see "my responder's phone has gone quiet" and have no way to see why.

**Changing a number won't fix it.** In testing, going back to 90 seconds without
anything else brings slow responders back to only about 2 pings a week, because
their scores are already at the bottom. Whatever we pick needs a fresh start.

## What we'd build

1. **The ping stays open after 60 seconds.** At 60 seconds we still ask the next
   person, so no callout waits longer than it does today. But the first person's
   ping stays on their phone as **"Still open: tap to take"** for up to 3 minutes.
   The first yes gets the job.
2. **Being late isn't the same as saying no.**

   | What happened | Today | Proposed |
   | --- | --- | --- |
   | Took it (on time or late) | +0.08 | +0.08 |
   | Said no, at any point | −0.12 | −0.12 |
   | Never answered | −0.12 | −0.12 |
   | Someone else took it first | −0.12 | **No change** |

   A no always costs, so nobody gains by waiting a minute and then declining.
3. **A fresh start for everyone.** At launch, every score goes back to neutral
   (0.5). Without it, the fix does almost nothing for the people already at the
   bottom.
4. **What the responder sees.**
   - **On launch day, to everyone who went quiet:** *"We changed how missed pings
     count, and your standing has been reset. You'll start getting callouts again."*
     Kip told us "Mite thinks Mite's been forgotten." This message is the answer to that.
   - After 60 seconds: *"Someone else is being asked too. Still open: tap to take."*
   - If someone else takes it, the screen updates quietly, with no second buzz:
     *"Covered by another responder. This doesn't count against you."* That
     includes the case where two people tap at almost the same moment.
   - **A weekly line in the app, with the reason:** *"You were offered 3 callouts
     this week (usually 11). You turned down 1 and didn't answer 1 in time."*
     Turning a ping down and missing it are told apart, the same way Dispatch
     records them.
5. **What a handler like Kip sees.** Kip looks after Meteor Mite, who went quiet,
   and The Gale, who went from about 13 to 21 pings a week. In his words, one is
   "dead quiet" next to one "on fire".
   - **A quiet-responder alert:** "Meteor Mite has had 1 ping in 7 days (usual: 11)."
     It fires when a responder drops below half their 4-week average.
   - **The reason, in plain words:** "3 of the last 4 pings were answered after the
     first minute." Not a score.
   - **What brings them back:** "Their standing was reset on [launch date]. Each
     callout they take moves them up. Missing one no longer pushes them down."
   - **The other half, which this doesn't fix:** The Gale stays busy. See cost 4.

**Coming back to the old note in the code.** Years ago, someone left a note in
the code (`history.py`) asking whether a score should drift back toward neutral on
its own. Our answer is two parts. First, a miss isn't a no, and the code shouldn't
treat them the same. Second, scores shouldn't drift back automatically: in testing,
that let a responder who mostly says no creep back up the list. A one-time fresh
start, plus a fair way to score lateness, does the job instead.

**Why this instead of going back to 90 seconds:** with a fresh start, both fill
callouts equally fast (about 50 seconds). But we don't know how long responders
really take to answer. If it's more than 90 seconds, going back to 90 fails
again. This proposal keeps working because the ping stays open.

## What we need

| Who | Decision or work |
| --- | --- |
| **Helen** | Pick this or going back to 90s plus a fresh start. Accept slower time-to-accept (cost 3), which conflicts with requirement B3 as written. Decide whether this replaces the "Ping timeout tuning" roadmap item. |
| Wen | Confirm the live system matches the code, and that scores *can* be reset. Today they're kept only in memory. Size the work. Add the scoring rules to the automated tests. |
| Marcus | Approve the scoring change. `config.py` says to tell him before any change. Agree the rollout and rollback trigger (cost 8). |
| Ravi | Add a "covered" outcome and log seconds-to-answer before launch (see cost 1). |
| Sofia | Design the phone wording and the console alert. Test it with 3 handlers, including Kip. The clickable prototype comes next. |
| Nadia | Support briefing and reply templates before release day (cost 9). |

---

## Appendix A: Test results

**How I tested:** synthetic data only, 12 made-up responders. Each run plays out 4
weeks on 4.1, then 4 weeks on 4.2 (scores collapse), then 4 weeks on the fix.
Numbers are medians over 20 random runs. Scripts and full results are in
`00-rook/test-data/routing/` (`stress_test.py`, `out/stress_test.md`). 12 scripted
rule checks in `test_rules.py` confirm the scoring table above.

| Fix | Slow responders, pings/wk (14.3 under 4.1) | Median secs to fill | Pings per callout | Acceptance per ping |
| --- | --- | --- | --- | --- |
| 4.2 left as is | 0.8 | 35 | 1.26 | 79% |
| Back to 90s | 2.2 | 37 | 1.22 | 82% |
| Back to 90s + fresh start | 15.6 | 50 | 1.22 | 82% |
| This proposal, no fresh start | 1.6 | 37 | 1.26 | 79% |
| **This proposal + fresh start** | **19.2** | **50** | **1.54** | **65%** |

**If responders are slower than we assumed** (slow responders' pings/wk, 10 runs each):

| Slow responders actually answer in… | ~70s | ~80s | ~100s | ~130s |
| --- | --- | --- | --- | --- |
| Back to 90s + fresh start | 14.9 | 8.0 | **1.1** | 0.9 |
| This proposal + fresh start | 18.0 | 15.9 | **14.4** | 10.6 |

**Also checked:**
- **Patchy signal (10% no answer) and only 30–50% of people free:** the proposal
  matches going back to 90s on unfilled callouts.
- **Gaming:** a responder who waits past 60s and then says no gets 0.7 pings a
  week. Under my first draft, where a late no was free, they got 6.2.
- **Letting scores ease back toward neutral over time:** adds nothing, and lets a
  disengaged responder creep back up. Left out.

## Appendix B: Costs and limits

1. **The acceptance rate will look worse even though nothing got worse.** About 1
   ping in 5 now ends as "covered by someone else". Acceptance counted per ping
   falls from about 79% to about 65%, but every callout still gets filled. Before
   launch, Ravi needs to report "covered" separately, or the headline dashboard
   will show a fall that didn't happen.
2. **More pings:** 1.54 per callout instead of 1.26. The extra ones update quietly
   rather than buzzing, but watch for complaints.
3. **Callouts fill more slowly than under 4.2 today:** about 50 seconds instead of
   35. The median time-to-accept goes from 29 to 42 seconds. That's the same as
   going back to 90 seconds plus a fresh start, and the same as 4.1 (43 seconds).
   4.2's speed came from skipping slow responders. **This breaks requirement B3 as
   written** ("time-to-accept doesn't get worse than its post-4.2 level"). Any fix
   that brings slow responders back will break it, so B3 should be re-baselined to 4.1.
4. **This doesn't relieve the busiest responders.** The busiest test responder
   stays at about 34 pings a week, against about 27 if we go back to 90s with a
   fresh start. That load comes from distance counting for 60% of the score. For
   Kip, The Gale stays busy. It needs its own fix (a weekly cap or a fairness rule)
   and is out of scope here.
5. **All the numbers come from made-up data.** Answer times are assumed, because
   the real `pings` table doesn't record seconds-to-answer. Logging it (requirement
   A4) is a prerequisite.
6. **Real unfilled callouts rose from 5.5% to 11% after 4.2.** The test data
   doesn't reproduce that, so getting it back to about 5% is a hope, not a
   prediction.
7. **No change to the availability record Rook Supply reads,** and no new
   identity data is collected.
8. **Rollout:** turn it on for one region first, then widen it. The rollback
   trigger is agreed with Marcus in advance, for example unfilled callouts above
   their pre-launch level for 3 days in a row. The fresh start can't be undone, so
   it happens once, at full launch.
9. **Support:** Nadia's team will get "why did my ping say *covered*?" and "why am
   I suddenly getting callouts again?". They need a briefing and reply templates
   before release day. The release notes should list what's deferred: the
   busiest-responder fix and Availability Confidence.

**Success after launch (targets are placeholders for the team to agree):**
- The four quiet responders are back above half their pre-4.2 volume within 4 weeks.
- Quiet-responder tickets fall to zero.
- Unfilled callouts head back toward 5%.
- A fair-load target for the busiest responders, set as part of the follow-up fix.
