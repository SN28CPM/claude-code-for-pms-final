---
name: fix-brief
description: Fixes a product brief so it passes the review checklist. It names an owner, gives measurable success targets, keeps the same scope throughout, and puts the problem before the fix. It can also set up a new brief that way from the start. Use it when the student says "fix the brief", "fix my brief", "make this brief pass the checklist", "clean up the brief", "start a new brief" or "draft a brief", or asks to apply the review-checklist fixes. It runs the review-checklist skill first and proposes each change. It edits the brief only after the student approves, then re-checks.
---

# Fix a brief

The student is a PM, not an engineer. They want the brief fixed, not lectured about.
This skill does the fixing for the four checks defined in
`.claude/skills/review-checklist/SKILL.md`. Read that file first. Its Pass / Partly /
Fail rules are the standard here.

**The student approves every change before it's made.** Asking for a fix is not
approval of the specific edits. Propose first (section 3), and edit only what they
approve (section 4). Nothing is written to the brief, or to a new file, before then.

## 1. Find the brief and review it

- Use the file the student named. If they didn't name one, use the brief this
  session was working on. If they want a new brief, go to section 5.
- Run the review-checklist checks on it, silently. You need the list of gaps; the
  student doesn't need the full review again unless they ask.

## 2. Collect the facts you can't make up

Some fixes need facts only the student or the sources have. **Never invent a name,
date, number or data source.**
- **Owner:** a person's name. If it's on the page, in the course's CLAUDE.md, or the
  student said it in this session, use it. Otherwise put `[PM name]` in place and
  ask for the name in your closing message. Don't guess a name from an email
  address or a username.
- **Targets and baselines:** take the numbers from the brief itself, its
  appendices, or sources the student named (for example the `pings` table or test
  results in the course folder). If a target is a judgment call, propose one from
  the evidence and label it as proposed.
- Ask at most one short question, and only if you can't proceed without the
  answer. Otherwise fix everything else and leave clearly marked placeholders.

## 3. Propose the changes and get approval

Work out each fix using the table in section 4. Don't edit anything yet. Show the
student a numbered list of proposed changes, one per fix:

- **What and where:** the check it fixes, and the section or line it touches.
- **Before → after:** the current text (quoted, or "nothing here yet" for a new
  section), then the exact new text. Show a new section or table in full.
- **Why:** one short reason, tied to the checklist.
- Mark any placeholder you'd insert, such as `[PM name]`.

Then ask one question: which changes to make. Offer **all of them**, **some of them**
(by number), or **none**. Use the question tool if it's available, with "Approve all"
first.

- Make only the changes the student approved, with the text they saw. If they reword
  one, use their wording.
- If they want a change done differently, revise it and show it again before editing.
- If they approve none, stop and leave the brief as it was.
- If an edit you're making turns out to need anything beyond what was approved (for
  example a line elsewhere that must change too), stop and ask about that piece first.

## 4. Apply the approved fixes

Edit the brief in place. Keep the author's voice and structure, and change only what
the student approved.

| Gap | Fix |
| --- | --- |
| **No named owner** | Put an "Owner: [name], accountable for this brief and its delivery" line in the header. Add the owner as the first row of any who-does-what table, with what they own: the decisions, tracking the measures, and when they report back. |
| **Success measures vague, missing or buried** | Add a "How we'll know it worked" section on page one, after the fix and before the asks. Make it a table: Measure · Target · By (a date, or time after launch) · Source (the data and who reports it). Give the baseline next to each target. Add at least one guardrail: a number that must not get worse. Remove placeholder success lists from the appendices and point to the new section. |
| **A measure the fix itself breaks** | Say so next to the measure, and turn it into a guardrail with a realistic level. Point to the cost that explains it. Ask the decision-maker to accept the change. |
| **Scope drift** | Keep one "Not in this brief (follow-ups)" list near the success section. Move anything out of scope there: deferred items, other teams' work, nice-to-haves. Take out-of-scope items out of the success measures. Introduce every item before it's referred to later. Make the recommendation read the same everywhere (title, body and asks). Update stale lines, such as a prototype "coming next" that now exists. |
| **Fix appears before the problem** | Title the brief after the problem, not the solution. Open with what's wrong, who it hurts, and the evidence, with a one-line *Sources:* note naming where the numbers come from. The first mention of the solution comes after that. |

Don't add new claims while fixing. If a fix needs a number you don't have, use a
placeholder and list it.

## 5. Starting a new brief

When the student asks to draft or start a brief, first show them the outline:
the section headings below, with one line on what goes in each, plus the file
name. Write the file only once they approve. Then show the full draft and ask
before saving any further changes to it. Use this order so it passes from the start:

1. **Title:** the problem, in plain words.
2. **Header:** For · Owner (named, accountable) · Date · Status.
3. **The problem:** what's wrong, who it hurts, and the evidence, with a *Sources:* line.
4. **What we'd build:** the fix, from the point of view of the people it affects.
5. **Why this option:** the alternatives considered, and why this one.
6. **How we'll know it worked:** a Measure / Target / By / Source table, plus a guardrail.
7. **Not in this brief (follow-ups).**
8. **What we need:** the owner first, then each decision or piece of work with a named person.
9. **Appendices:** evidence, costs and limits.

Write it in `<module folder>/brief.md` unless the student names another file.

## 6. Re-check and report

- Run the review-checklist checks again on the edited brief.
- Report in plain language:
  - one line with the result before and after (for example "Before: 0 of 4 pass.
    After: 4 of 4 pass, once the owner's name is filled in.");
  - a short list of what changed, by section, and any proposed changes the student
    turned down (and which check still falls short because of that);
  - any placeholders left for the student to fill, and the one question if there is one.
- Don't save to GitHub unless the student asks. Don't save anything to memory or
  outside the course folder.
