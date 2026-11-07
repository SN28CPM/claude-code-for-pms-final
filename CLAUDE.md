# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Answer only the question the student asks, from the sources they
  name. Don't investigate beyond it or offer a theory about what
  Release 4.2 changed unless they ask for one.
- Read and write only within this directory.
  Exceptions, for the course-setup and wrap-up skills only:
  - When the student asks you to check their setup, save their work or wrap up a session, that request is their yes. You may run the GitHub command-line program installed at ~/.ccpm/gh for those checks and saves, and look in that folder to find it.
  - For a repair, first tell the student in one plain sentence what you are about to do, and act only after they say yes. Repairs may: run that GitHub program (including setting this folder's own git sign-in setting and changing this repo's visibility back to Public); copy the student's own course files into this directory from another folder on their computer (copy only; never move, edit or delete the originals); and rename something outside this directory that blocks setup, by adding "-old" to its name (never delete it).
  Outside this directory you still never write, edit or delete anything else.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

I'm the new PM for **Rook Dispatch**, replacing Priya Raghunathan (left 21 Aug 2026,
no overlap). Sources: Rook wiki (About Rook, Glossary, Team directory, Releases,
Q3 roadmap, Product briefs) and `00-rook/company/notes/handoff-from-priya.docx`.

### The company
- Rook Industries sells coordination and provisioning software to independent
  masked responders and the handlers and quartermasters who support them. Rook
  doesn't employ responders. Publicly it presents as a logistics/workforce vendor.
- 241 staff, mostly remote (HQ Site Aleph; Berlin, Singapore, Cornwall). Revenue is
  per active responder. Monthly release train, 4.x numbering.
- **Confidentiality (contractual):** cover identities are never stored. Never design
  for, or try to work out, a responder's legal identity. Read Security Policy 4.1
  before touching responder records.

### Products
| Product | What it does | Users |
| --- | --- | --- |
| Rook Dispatch (mine, the flagship) | Availability, proximity, who gets pinged for a callout, and whether they take it | Handlers (desktop console); responders (phone) |
| Rook Supply | Requisitions, maintenance, field failure reports | Handlers, quartermasters |

Dispatch writes the Responder Availability Record. Supply reads it for maintenance scheduling.

### Vocabulary (Rook-specific meanings)
- **Callout**: a request for a responder to attend an incident (the unit of work).
  **Ping**: one callout offered to one responder's phone.
- Ping outcomes: **taken**, **turned down**, or **missed** (the ping wait ran out).
  Turned down and missed are recorded separately, but both move the ping to the next responder.
- **Ping wait**: how long a ping stays live. It's global and set per release (90s → 60s in 4.2).
- **Acceptance rate**: share of pings taken. This is the headline metric.
  **Time-to-accept**: the median number of seconds from sending a ping to it being taken.
- **Coverage gap**: no available responder had the required tags. Nobody *could* go,
  which is not the same as low acceptance.
- **Routing priority**: the score that ranks responders. Inputs are proximity (a travel-time
  estimate), availability, capability match and recent acceptance history. Turning a ping
  down or missing it lowers your future rank.
- **Capability tags**: flight, structural-entry, hazmat-tolerant, cold-weather, aquatic,
  crowd-management, de-escalation.
- **Handler**: looks after one or a few responders, and is usually the person using the product.
  **Quartermaster**: owns gear stock and approves requisitions (a Supply user).
  **Mutual aid**: responders covering each other's areas. It isn't supported yet and is
  on the Q4 exploration list.

### People (Dispatch team, as of 2 Sep 2026)
Wiki comments sign with roles. Here's who each role is:
| Role in comments | Person | Location | Notes |
| --- | --- | --- | --- |
| Engineering manager | Marcus Oyelaran | Site Aleph | Runs Dispatch eng. Priya says he's direct; ask him first |
| Staff engineer | Wen Li | Berlin | Built the code that decides who gets pinged. No written spec exists. Was away 14–24 Aug |
| Product designer | Sofia Marino | Site Aleph | Console + phone app; ran the September interviews |
| Support lead | Nadia Hoffmann | Berlin | Tickets; hears handler pain first. Priya suggests a standing 15 min |
| Director of Product | Helen Achebe | Site Aleph | My director; owns roadmap and commitments |
| Data analyst | Ravi Menon | Singapore | Owns the weekly acceptance-rate numbers. He isn't in the 4.2 thread |

### Releases
- **4.0** (7 Apr): new console navigation, responder profile redesign, routing override audit log.
- **4.1** (16 Jun): proximity now uses a travel-time estimate, bulk callout, push reliability.
- **4.2** (12 Aug): proximity weighted up relative to recent acceptance history; ping wait
  90 → 60s; console filters persist; three defect fixes. Release notes leave out deferred items.

### Where things stand on 4.2 (per the wiki thread and the handoff)
- Since 4.2, fewer pings are being taken, and callout tickets are running about 3x normal.
  Nadia's split is ~2/3 "phone never goes off" and ~1/3 "gone before I could answer".
  She attributes the second to the 60s ping wait. She can't explain the first.
  Volume was flat but still elevated on 26 Aug, and a handler emailed her directly.
- On 14 Aug, Marcus asked whether the routing change was *meant* to apply to responders who'd
  been turning jobs down. He said the config doesn't distinguish them. Wen was away. The thread
  shows no answer.
- Nadia asked for the acceptance trend. Marcus offered "rough", not the real weekly numbers.
- Priya's view: it's mostly August seasonality, so wait for September and don't revert 4.2,
  because the change was a three-quarter-old ask from wide-area responders. Marcus repeated
  "August dip" on 26 Aug.
- On 28 Aug, Marcus proposed regrouping on 4.2 once the new PM had had a week. Nadia has a
  ticket breakdown ready.

### Roadmap (Q3, last reviewed 30 Jun, every item owned by Priya, so ownership needs reassigning)
| Item | Target | Status |
| --- | --- | --- |
| Change to who gets pinged | 4.2 | Committed. Shipped |
| Ping timeout tuning | 4.2 | Committed. The 60s cut shipped; unclear if that's the whole item |
| Availability Confidence | 4.2 | Committed. **Not in 4.2 release notes** |
| Requisition approval chains (Supply) | 4.3 | Committed |
| Handler phone app | Q4 | Exploring |
| Shared cover between responders | Q4 | Exploring |
Committed items are "locked" and changes go through Product. Priya flagged that items squeezed
out of 4.2 still need a conversation with Helen about whether they remain Q3 commitments.

### Product briefs
- **Routing Override Audit Log** and **Bulk Callout** shipped (4.0, 4.1). Bulk Callout's
  brief wanted a time-to-full-coverage baseline first.
- **Handler Phone App** (8 Sep): notifications, status view and one-tap contact for handlers.
  Sofia is exploring it for Q4, unstaffed. It came from Aunt Dot's interview.
- **Requisition Approval Chains** (Supply): a second sign-off over $2,000, plus heavy scope
  creep (48h reroute, dashboard, handler tracking, replacing Halloran's spreadsheet). Phasing TBD.

### Priya's open asks for me
- Settle the deferred-4.2-items question with Helen.
- Write the missing description of how Dispatch decides who gets pinged.
- Ignore filter-persistence ticket noise.

Session notes (Module 1, 24 Oct 2026):
- Availability Confidence is the only 4.2 item clearly deferred. Ping timeout tuning looks
  shipped (the 60s cut). The wiki keeps no record of deferrals for 4.0 or 4.1.
- Helen's ask is in `05-super-speed/director-request.txt`: a one-pager plus a clickable
  prototype from the handler (Kip) and quiet-responder view before any code fix. It has no
  severity and no deadline.
- Nothing addressing the 4.2 problems is scheduled. 4.3 holds only Requisition approval chains (Supply).
- No routing weights are documented anywhere. The code is in `00-rook/code/dispatch-routing/`
  and hasn't been read yet.
- Draft requirements, with acceptance criteria, are in `dispatch-4.2-requirements.md`. All
  baselines are TBD until Ravi's numbers come in. The thresholds in it are placeholders.

Session notes (Module 2, 24 Oct 2026):
- Interviews (Sofia, 2–5 Sep) and the 147 tickets come from different people. Only #3043
  (Ambrose) overlaps. Interviews are loud on handler alerts, dark mode and text size. Tickets
  are loud on quiet responders (30, all open, about Farlight, The Undertow, Corporal
  Ashgrove and Halfmoon) and on pings gone before answering (15, all open, from 12 Aug).
- 64/147 tickets are closed, and none filed after 27 Aug. The table has no closed date,
  so time-to-resolve can't be measured.
- Code confirms a missed ping is penalized like a turned-down one (−0.12 vs +0.08 credit),
  with no easing back. Working theory: the 60s wait leads to more misses, a lower rank, and quiet responders.
- `00-rook/test-data/routing/` runs synthetic data through the real code. Only the 90s
  wait with the 4.2 weights passes every check. Answer speeds are assumed, so real
  seconds-to-answer data is needed (the pings table lacks it).
- Also drafted `dispatch-backlog.md`. Next: check the theory against the real `pings` table.

Session notes (Module 3, 31 Oct 2026):
- `pings` (1,696 rows, 29 Jun–6 Sep) confirms the theory. Acceptance was steady at ~77%, then
  64% after 12 Aug. Missed went 2% → 18% starting on 12 Aug itself, and turn-downs didn't rise.
  Callouts nobody took went 5.5% → 11%.
- Tickets agree with pings: "gone before answering" tickets start 12 Aug, and pings to quiet
  responders drop from 17 Aug, the same week the "quiet responder" tickets start.
- Real collapse is Farlight, The Undertow, Vesper and Meteor Mite (18–29% taken after 4.2,
  11–17 pings in ~4 weeks). There are no tickets about Vesper or Meteor Mite. Ashgrove and
  Halfmoon are ticketed but mid-table.
- No distance column exists, so I used callout area vs. responder home area as a stand-in.
  Outsiders now take 82–94% of callouts in Uptown, Harborside, Old Town and Eastgate (the
  home areas of the four collapsed responders). Before 4.2 they took 0%.
- The acceptance score never resets or decays (2019 TODO in `history.py`), and scores live in
  memory only. Open for Wen: are live scores persisted? Is answer time logged? Are real
  travel-time estimates stored?

Session notes (Module 4, 31 Oct 2026):
- Routing flow: free responders in region (`availability.py`) → score (`routing.py`) → rank → offer one at a
  time with 60s wait (`offer.py`) → yes +0.08 / no or miss −0.12 (`history.py`). Nobody is removed, only ordered.
  Callout creation, travel-time and push code are stubs and live elsewhere.
- Score = 0.60 × closeness (1 − min/45) + 0.25 × "said yes lately" + 0.15 × skills match. At score 0, max is 0.75.
  A floored responder must be under ~3 min away to outrank a healthy one 20 min away.
- Week-1 score hits after 4.2 predicted who went quiet (Undertow −0.72, Meteor Mite −0.56, Farlight −0.44).
  Vesper (−0.20) collapsed and Nightwell (−0.32) grew, likely from unknown starting scores.
- Marcus's 14 Aug question is half answered: the change applies to everyone, and the code can't tell a miss from a no.
  The people hurt were missers, not turn-downers. Whether it was intended is open for Wen/Helen.
- Three groups since 4.2: 4 dropped out (~12 → ~1/wk), 2 fading (Ashgrove, Halfmoon), 10 gaining (up to 21/wk, a
  burnout risk). Still diverging at 31 Aug, so not seasonal. No trend by incident type (all 20 rose).
- Recovery from 0 needs ~7 takes in a row (about 2 months at 1 ping/wk). Open: do restarts wipe scores, and do handler
  overrides (4.0 audit log) bypass or affect scoring? Ask Wen/Marcus.

Session notes (Module 5, 7 Nov 2026):
- `05-super-speed/brief.md` is the solution brief for Helen. It keeps the 60s ping wait: the ping stays open up to 3 min,
  a late take counts, "covered" is free, any no costs −0.12, and there's a one-time fresh start (all scores to 0.5).
  It also covers the responder and Kip views. Helen picks between this and going back to 90s plus a fresh start.
- Stress test (`00-rook/test-data/routing/stress_test.py`, 20 seeds, 4.1 → 4.2 → fix): no fix works without a fresh
  start (90s alone gives 2.2/wk). With a fresh start, the proposal gives 19.2/wk and 90s gives 15.6/wk. Both fill in
  ~50s. The proposal still works if answers take 100s+, where 90s collapses. That is the case for keeping 60s.
- Costs: acceptance per ping drops ~79% → 65% (needs a "covered" outcome from Ravi), and time-to-accept goes 29 → 42s,
  which breaks requirement B3 as written. The busiest responders aren't relieved. Ease-back was dropped (it lets
  disengaged responders creep back). Late-no loophole closed. `test_rules.py` has 12 rule checks.
- Kip handles Meteor Mite (quiet) and The Gale (13 → 21/wk). The Undertow is Desmond Okafor's, Vesper is Aunt Dot's,
  Farlight is Linda Pruitt's.
- Prototypes: `prototype.html` (console + phone) and `prototype-mobile.html` (tabs), each with a 4.2-today toggle and an
  "All responders" travel-time view (made-up minutes). Open: may a handler see other handlers' responders? Travel time
  only, no locations.
- Later in Module 5: the dispatcher views got a pings chart (real taken/turned down/missed counts per responder since
  4.2) and a combined distance + pings view. It shows Meteor Mite is nearest (9 min) but missed 8 of 14. There's
  also a two-window version: `dispatcher.html` (runs the clock and rules) and `responder.html` (Mite's phone), synced
  across windows. It was tested through a local server, not by double-clicking the files. `.claude/launch.json` starts it.

Session notes (Module 6, 7 Nov 2026). The post-4.2 recovery project is named **Jedi Order** (PM: Yoda):
- Project skills in `.claude/skills/`: `review-checklist` (checks a brief for owner, success measures, scope, and
  problem before fix), `fix-brief` (proposes fixes and edits only after I approve; also a new-brief template), and
  `weekly-trends` (queries pings and tickets, writes `reports/weekly-trends/<date>.md` + `latest.html`).
- `weekly-trends` is scheduled every Monday ~9:11 (task `rook-weekly-trends`, Auto mode, stored in
  ~/.claude/scheduled-tasks, outside the folder, with my OK). On fix launch day, set `fix_launch` in its config.json.
  The data ends 6 Sep, so reports show STALE until the tables get new rows.
- `brief.md` was fixed per the checklist: problem-led title, sources line, a "How we'll know it worked" table with
  targets, dates and sources, and follow-ups split out. Owner: Yoda, Rook Dispatch PM.
- `dispatch-4.2-acceptance-test.md`: AC1–AC9, with limits set by the worst pre-4.2 week (29 Jun – 9 Aug). 4.2 fails
  8 of 9 (only turn-downs recover). Its own goal failed: reaching the taker went from ~26s to 61s. AC1–AC9 are now
  in `dispatch-4.2-requirements.md` §8 and the weekly report. Callouts/week fell ~140 → ~120 after 4.2 (unexplained;
  ask Ravi/Nadia).
- Later in Module 6: `final-report.html` is a 12-slide presentation with one finding and my exact prompt per
  module, real-data charts, an in-slide prototype demo, and the skills slide. The project is **Jedi Order**, owner
  **Yoda** (in the brief, requirements, acceptance test, report and weekly report). `final-report-storybook.html`
  retells it for a 3-year-old (read-aloud + tap-in-time game). `final-report-storybook.pdf` is built from page
  screenshots, because headless Chrome's print fails on the emoji (render with `?shot#N`).
