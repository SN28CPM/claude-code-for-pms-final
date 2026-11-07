---
name: review-checklist
description: Reviews a product brief against a four-point checklist. Does it name who owns it, say how we'll know it worked, keep the same scope from start to finish, and explain the problem before the fix? Use it when the student says "review-checklist", "run the review checklist", "check this brief", "review my brief" or points it at a brief file (for example 05-super-speed/brief.md). It reports what passes and fails, with quotes from the brief. It doesn't change the brief unless asked.
---

# Review checklist

The student is a PM, not an engineer. They want a quick, honest verdict on a brief
they're about to send, in plain language. Don't use jargon.

## 1. Find the brief

- Use the file the student named. If they didn't name one, use the brief this
  session was working on. If there isn't one, look for `brief.md` files in the
  course folder. If there's more than one, ask one short question: "Which brief
  should I check?"
- Read the whole brief before judging it, including any appendices.
- Only read files inside the course folder.

## 2. Check the four points

Judge each point **Pass**, **Partly** or **Fail**. Back every verdict with a short
quote from the brief, and say where it is (the section heading, or the line number
if it's a file). If something is missing, say what you looked for and didn't find.

### 1. Names who owns it
- **Pass:** one named person is accountable for the brief as a whole. A role on its
  own ("the PM", "Product") doesn't count.
- **Partly:** the "From" line or a sign-off names someone, but nothing says they own
  delivery. Or the work is split between named people and nobody owns it overall.
  An owners table for tasks is useful, but it doesn't replace an overall owner.
- **Fail:** no named owner anywhere.

### 2. Says how we'll know it worked
- **Pass:** there are success measures that can be checked. Each one has a number,
  a time frame and a source of data. For example: "The four quiet responders are
  back above half their pre-4.2 volume within 4 weeks."
- **Partly:** measures exist but are vague ("improve engagement"), have no time
  frame, are all marked as placeholders, or don't say where the data comes from.
- **Fail:** nothing says what success looks like.
- Also flag any measure that the brief's own fix would break.

### 3. Keeps the same scope from start to finish
- List what the brief says it will do near the top: the problem it takes on, what
  it builds, and what it says is out of scope.
- Then check every later section against that list. Look for:
  - work that appears later but was never introduced (scope creep);
  - something promised early that drops out later (a silent cut);
  - something called out of scope that comes back in;
  - numbers or names that change between sections, such as a target, a date, who a
    responder belongs to, or which option is recommended.
- **Pass:** nothing drifts. **Partly:** small drift, or out-of-scope items are
  mentioned but clearly labelled as follow-ups. **Fail:** the brief ends up
  proposing something different from what it started with.

### 4. Explains the problem before the fix
- **Pass:** a reader understands what's wrong, who it hurts and how we know (with
  evidence) before the first mention of the solution.
- **Partly:** the problem comes first but has no evidence, or the fix is hinted at
  in the title or first lines before the problem is explained.
- **Fail:** the brief opens with the solution, or never says what problem it solves.
- Quote the first sentence that describes the fix, and say which section it's in.

## 3. Report back

Start with one line giving the overall verdict, for example: "3 of 4 pass. The gap
is ownership." Then this table:

| Check | Verdict | Evidence from the brief | What to fix |
| --- | --- | --- | --- |

Keep "What to fix" to one concrete sentence per row, such as the line to add or the
number to change. After the table, list any other drift you noticed under point 3
in up to five short bullets.

## Rules

- Don't edit the brief. If the student wants the fixes made, they'll ask. Then
  change only what the review flagged.
- Only judge what's on the page. Don't mark a point down for something the brief
  couldn't reasonably know.
- Quote; don't paraphrase the evidence. Keep each quote under about 20 words.
- Don't save anything to memory or outside the course folder.
