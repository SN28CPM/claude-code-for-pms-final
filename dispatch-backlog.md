# Rook Dispatch: product backlog

Draft · PM, Rook Dispatch · 24 October 2026 · for review with Helen Achebe

**Sources**
- Q3 roadmap and Releases (wiki)
- Product briefs (wiki)
- Customer interviews, September 2026 (wiki)
- 4.2 comment thread (wiki)
- Priya's handoff
- Helen's request (`05-super-speed/director-request.txt`)
- `dispatch-4.2-requirements.md`

**Priority**
- **P0**: blocks understanding or fixing the post-4.2 drop.
- **P1**: next release candidate.
- **P2**: soon.
- **P3**: later or exploring.

**Effort** isn't estimated. That needs engineering input from Marcus and Wen. Owners shown
are suggestions, not agreed assignments.

## Deferred from 4.2

| ID | Item | Priority | Suggested owner | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| D-1 | **Availability Confidence**: show a confidence score alongside a responder's stated availability | P2 | PM + Helen | Committed to 4.2, didn't ship | The roadmap still calls it a Q3 commitment. Decide with Helen: re-commit to a release or drop it. Priya flagged this conversation as overdue. |
| D-2 | **Unnamed second item** Priya says was "squeezed out" of 4.2 | P1 (to identify) | PM | Unknown | Ask Helen or Marcus what it was. It may not be on the roadmap. |
| D-3 | **Ping timeout tuning**: confirm it's complete | P1 | PM | 60s cut shipped. The roadmap still says Committed | Mark it shipped, or define what's left. Tie it to the ping wait review (B-3). |

## Post-4.2 investigation (P0)

| ID | Item | Priority | Suggested owner | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| A-1 | Real weekly acceptance numbers before and after 4.2, vs prior years | P0 | Ravi Menon | Not started | Tests the seasonal explanation. Replaces the "rough" figures. Req A1. |
| A-2 | Explain the "phone never goes off" reports (2/3 of tickets) | P0 | Wen Li + Marcus | Not started | Req A2. |
| A-3 | Decide whether the 4.2 ranking change should treat responders who turn jobs down the same way | P0 | Helen (decision), Wen | Open since 14 Aug | Marcus's unanswered question. Req A3. |
| A-4 | Tag tickets by theme: "never goes off", "gone before answer", "filter persistence" | P0 | Nadia Hoffmann | Partly (Nadia tracks the split manually) | Req C3. |

## Product changes

| ID | Item | Priority | Suggested owner | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| B-1 | Handler sees when, and why, a responder is getting fewer pings | P1 | Sofia Marino | Helen wants a one-pager + prototype first | Kip, Dot (2/4); Helen's request. Req B1. |
| B-2 | Responder sees why they've gone quiet, in plain language | P1 | Sofia Marino | Not started | Kip: "Mite thinks Mite's been forgotten." Req B2. |
| B-3 | Ping wait review, plus the experience when a ping is missed | P1 | PM + Ravi | Waiting on A-1 data | Dot, Ambrose, Halloran (3/4); 1/3 of tickets. Req A4/B3. |
| B-4 | Routing behaviour fix, only if A-2 or A-3 finds unintended behaviour | P1 (conditional) | Wen Li | Blocked by A-2, A-3, and Helen's approval | Engineering says a small fix is ready. Helen wants the one-pager first. Req B4. |
| B-5 | Alert the handler, not just the responder, when a callout is live | P1 | Sofia Marino | Not started | Dot, Ambrose (+ Kip on sounds) (3/4). Overlaps with C-1. |
| B-6 | A different alert sound for each responder | P2 | Sofia Marino | Not started | Kip. |
| B-7 | Warn the user when saved filters reset, instead of resetting them silently | P2 | Marcus's team | Not started | Ambrose. A bug in a 4.2 feature. |
| B-8 | Larger text and status badges (engaged vs available) | P2 | Sofia Marino | Not started | Dot, Ambrose (2/4). |
| B-9 | Dark mode for the console | P2 | Sofia Marino | Logged repeatedly | Kip's top ask. |
| B-10 | Move the capability tag legend closer to hand | P3 | Sofia Marino | Not started | Ambrose; he called it "not urgent". |
| B-11 | Fewer click-throughs from the coverage view | P3 | Sofia Marino | Not started | Ambrose. |

## Foundations and housekeeping

| ID | Item | Priority | Suggested owner | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| F-1 | Written description of how Dispatch decides who gets pinged | P1 | PM + Wen Li | Missing | Priya's top ask. Req C1. |
| F-2 | Reassign Q3 roadmap owners (all still Priya) and re-review the roadmap | P1 | PM + Helen | Last reviewed 30 Jun | Req C2. |
| F-3 | Release notes list deferred items | P2 | PM | Not started | Today they're omitted. That's why D-1 and D-2 were hard to find. |
| F-4 | Time-to-full-coverage baseline for Bulk Callout | P3 | Ravi Menon | Missing since 4.1 | The brief asked for it before shipping. |

## Exploring (Q4)

| ID | Item | Priority | Suggested owner | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| C-1 | Handler phone app: notifications, status view, one-tap contact | P3 | Sofia Marino | Exploring, unstaffed | It needs a baseline metric before it moves on. Could deliver B-5. |
| C-2 | Shared cover between responders (mutual aid) | P3 | PM | Exploring | Not supported today. |

## Not Dispatch: hand to the Supply team

| ID | Item | Notes |
| --- | --- | --- |
| S-1 | Requisition approval chains (4.3, committed) | Phase 1 is the second sign-off over $2,000 only. Split the extra features out. The roadmap still lists Priya as owner. |
| S-2 | Requisition priority field has no effect on the queue | Halloran. |
| S-3 | No feedback after filing a field failure report | Halloran. |
| S-4 | Equipment catalog search needs category filters | Halloran. |
