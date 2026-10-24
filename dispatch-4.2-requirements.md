# Rook Dispatch: post-4.2 recovery requirements

| | |
| --- | --- |
| Status | Draft, for review |
| Owner | PM, Rook Dispatch |
| Approver | Helen Achebe, Director of Product |
| Reviewers | Marcus Oyelaran (Eng Manager), Wen Li (Staff Engineer), Sofia Marino (Design), Nadia Hoffmann (Support), Ravi Menon (Data) |
| Date | 24 October 2026 |
| Sources | Rook wiki (Releases, Q3 roadmap, Glossary, Team directory, Product briefs, 4.2 comment thread), Priya's handoff, Helen's request |

## 1. Background

Release 4.2 shipped on 12 August 2026 with two changes to the callout cycle:

- Proximity is weighted more heavily than recent acceptance history when ranking responders.
- The ping wait dropped from 90 to 60 seconds.

Since then, fewer pings are being taken, and callout tickets are running about 3x normal.
Support sees two themes:

- About 2/3 of tickets: the responder's phone "never goes off".
- About 1/3 of tickets: the ping was "gone before I could answer".

Helen has asked that nobody ships a code change until there's a one-pager on what we'd build,
seen from the point of view of a handler like Kip and of a responder who has gone quiet.

The cause of the drop has not been established. This document deliberately does not assume one.
Workstream A establishes the facts. Workstreams B and C act on them.

## 2. Goals

1. Restore acceptance rate and time-to-accept to their pre-4.2 levels without undoing the
   wide-area responders' gain from 4.2.
2. Bring callout ticket volume back to its normal range.
3. Make routing decisions visible and explainable to handlers and responders.
4. Leave Dispatch with a written routing spec and a roadmap that has owners.

## 3. Non-goals

- Reverting 4.2 wholesale. The proximity change was a long-standing responder ask.
- Shipping a one-line settings change as the fix (per Helen).
- Storing or inferring responder legal identities (Security Policy 4.1).
- Requisition Approval Chains delivery. It's covered only as a scoping follow-up in §7.

## 4. Workstream A: Establish the facts

### A1. Acceptance baseline and trend
The real weekly numbers (owned by Ravi) for the 12 weeks before and the 10 weeks after
12 Aug 2026, compared with the same weeks in prior years.

**Acceptance criteria**
- [ ] Weekly acceptance rate, time-to-accept, and pings missed vs turned down, each before and
      after 4.2.
- [ ] The same metrics for August–October of at least one prior year, to test the seasonal
      explanation.
- [ ] Coverage gaps reported separately from low acceptance.
- [ ] Results broken down by responder segment: wide-area vs dense-area, and by recent
      acceptance band.
- [ ] Ravi signs off on the numbers, and they replace the "rough" figures in all discussions.

### A2. "Phone never goes off" explained
**Acceptance criteria**
- [ ] For a sample of at least 20 responders named in "never goes off" tickets (handled
      without identity data), we can show whether Dispatch sent them pings after 12 Aug, how
      many, and where they ranked.
- [ ] The finding is written up in plain language and agreed by Wen and Marcus.
- [ ] Each finding is classified as one of: working as designed, unintended behaviour, or
      delivery failure.

### A3. Decision on Marcus's open question
Should the 4.2 ranking change apply in the same way to responders who have been turning jobs down?

**Acceptance criteria**
- [ ] Helen makes the call and records it, with the reasoning, in the routing spec (C1).
- [ ] If the answer is that the current behaviour wasn't intended, a B-workstream requirement
      is opened for it.

### A4. Ping wait review
**Acceptance criteria**
- [ ] The distribution of seconds-to-answer for taken pings, before and after 4.2, shows what
      share of answers took 60–90 seconds.
- [ ] The decision on the ping wait (keep it, change it, or make it vary) is recorded with data
      attached.

## 5. Workstream B: Product changes (designed from A's findings)

Design is led by Sofia, and the one-pager plus a clickable prototype go to Helen before any build.

### B1. Handler visibility
A handler can see when, and why, a responder they look after is getting fewer pings.

**Acceptance criteria**
- [ ] Given a responder whose ping count over the last 7 days is well below their usual level,
      the handler sees a notice in the console naming the main reason. The threshold is set
      from A1.
- [ ] The reason is shown in handler language (for example, "turned down or missed 4 recent
      pings"), not as a score.
- [ ] The handler sees what would restore the responder's position.
- [ ] Usability testing with at least 3 handlers (including Kip) shows that 3 out of 3 can
      explain why their responder went quiet.

### B2. Responder experience
A responder who has gone quiet understands why and isn't left guessing.

**Acceptance criteria**
- [ ] The responder can see in the phone app that they've had fewer pings recently, and the
      plain-language reason.
- [ ] Turning a ping down is distinguishable from missing it in what the responder is told,
      matching how Dispatch records them.
- [ ] No new identity data is collected.

### B3. Missed-ping experience (if A4 supports a change)
**Acceptance criteria**
- [ ] The share of "gone before I could answer" tickets falls by at least half within 4 weeks of release.
- [ ] Median time-to-accept doesn't get worse than its post-4.2 level.

### B4. Routing behaviour fix (only if A2/A3 find unintended behaviour)
**Acceptance criteria**
- [ ] The behaviour matches the decision recorded in A3, and is covered by automated tests.
- [ ] Wide-area responders' ping share stays at or above its post-4.2 level (from A1).
- [ ] Acceptance rate returns to the pre-4.2 baseline (from A1) within 6 weeks of release.
- [ ] Rollout is gradual, with a rollback trigger agreed in advance by Marcus and the PM.

### B5. Release gate (applies to B1–B4)
- [ ] Helen has approved the one-pager and prototype.
- [ ] Support has a briefing and macros before release day.
- [ ] Release notes list deferred items explicitly.

## 6. Workstream C: Foundations

### C1. Written routing spec
**Acceptance criteria**
- [ ] It describes each routing priority input (proximity, availability, capability match,
      recent acceptance history), how each is weighted, and how turned-down and missed pings
      affect the ranking.
- [ ] Wen reviews it for accuracy, and it lives in the wiki.
- [ ] It is updated in the same release as any routing change.

### C2. Roadmap hygiene
**Acceptance criteria**
- [ ] Every Q3 item has a current owner (none are owned by Priya).
- [ ] Availability Confidence is either re-committed with a target release or formally
      dropped, agreed with Helen.
- [ ] Ping timeout tuning is marked shipped or remaining scope is defined.
- [ ] The roadmap is reviewed after every release, and the review date is updated.

### C3. Support signal
**Acceptance criteria**
- [ ] Tickets are tagged "never goes off", "gone before answer" and "filter persistence", so
      Support and Product can track them separately each week.
- [ ] Nadia's weekly split is shared with the PM and Ravi.
- [ ] Ticket volume returns to the pre-4.2 normal range for 4 consecutive weeks.

## 7. Follow-ups (outside this fix)

- **Bulk Callout**: capture the time-to-full-coverage baseline the brief called for.
- **Handler Phone App**: define the baseline metric before it leaves exploration. It overlaps
  with B1 notifications.
- **Requisition Approval Chains**: phase 1 is the second sign-off over $2,000 only. The other
  ideas go to a separate brief.

## 8. Success metrics

| Metric | Target | Source |
| --- | --- | --- |
| Acceptance rate | Back at the pre-4.2 baseline | A1 (Ravi) |
| Time-to-accept | No worse than the pre-4.2 baseline | A1 |
| Wide-area responders' ping share | At or above post-4.2 level | A1 |
| Callout ticket volume | Normal range for 4 weeks in a row | C3 (Nadia) |
| Handlers who can explain a quiet responder | 3/3 in testing | B1 |

All baseline values are TBD until A1 is complete. No numbers have been assumed.

## 9. Open questions

1. Is the drop seasonal, caused by 4.2, or both? (A1, A2)
2. Was it intended that the 4.2 change applies the same way to responders who turn jobs down? (A3)
3. Which second item, besides Availability Confidence, was squeezed out of 4.2? (C2)
4. What is "normal" ticket volume? Nadia to confirm.
