---
name: weekly-trends
description: Builds the weekly trends report for Rook Dispatch. It compares before 4.2, after 4.2 and after the fix, week by week, from the rook-database pings and support_tickets tables, and checks the brief's targets. Use it when the student says "weekly trends", "run the weekly report", "show this week's trends" or "how are the numbers this week", and when the weekly scheduled task runs. It writes reports/weekly-trends/<date>.md and latest.html.
---

# Weekly trends

Shows how Dispatch is doing each week: before Release 4.2, after 4.2, and after the
fix in `05-super-speed/brief.md`, measured against that brief's "How we'll know it
worked" targets. The reader is a PM, so keep the summary plain.

Settings live in `config.json` next to this file:
- `release_4_2`: the release date.
- `fix_launch`: the fix's launch date, or `null` until it ships. When the student
  says the fix has launched, set it, with their OK.
- `quiet_responders`, `targets` and `report_dir`.

## Steps

1. **Read `config.json`.**
2. **Get the numbers.** Use the rook-database connector's `run_query` with exactly
   this query. If `quiet_responders` in the config has changed, replace the four names in the
   `IN (...)` list. If `release_4_2` has changed, replace the date in `base`:

   ```sql
   WITH p AS (SELECT date_trunc('week', sent_at)::date AS wk, count(*) AS pings,
       count(*) FILTER (WHERE outcome='taken') AS taken,
       count(*) FILTER (WHERE outcome='turned down') AS turned_down,
       count(*) FILTER (WHERE outcome='missed') AS missed,
       count(*) FILTER (WHERE responder IN ('Farlight','The Undertow','Vesper','Meteor Mite')) AS quiet4_pings
     FROM rook.pings GROUP BY 1),
   co AS (SELECT callout_number, min(sent_at) AS first_ping,
       min(sent_at) FILTER (WHERE outcome='taken') AS taker_pinged,
       count(*) AS n, bool_or(outcome='taken') AS filled
     FROM rook.pings GROUP BY 1),
   c AS (SELECT date_trunc('week', first_ping)::date AS wk, count(*) AS callouts,
       count(*) FILTER (WHERE NOT filled) AS unfilled,
       round(percentile_cont(0.5) WITHIN GROUP (ORDER BY extract(epoch FROM taker_pinged - first_ping))
         FILTER (WHERE n >= 2 AND filled)::numeric, 0) AS secs_to_taker
     FROM co GROUP BY 1),
   weeks AS (SELECT DISTINCT wk FROM p),
   rw AS (SELECT r.name, w.wk, count(x.*) AS n FROM rook.responders r CROSS JOIN weeks w
     LEFT JOIN rook.pings x ON x.responder = r.name AND date_trunc('week', x.sent_at)::date = w.wk
     GROUP BY 1,2),
   base AS (SELECT name, avg(n) AS usual FROM rw
     WHERE wk < date_trunc('week', DATE '2026-08-12')::date GROUP BY 1),
   load AS (SELECT rw.wk, count(*) FILTER (WHERE rw.n < 0.5 * b.usual) AS below_half,
       count(*) FILTER (WHERE rw.n > 1.5 * b.usual) AS above_150
     FROM rw JOIN base b USING (name) GROUP BY 1),
   t AS (SELECT date_trunc('week', filed_at)::date AS wk, count(*) AS tickets,
       count(*) FILTER (WHERE subject ~* '(vanished before|moved on|gone before|lost one|first one in|out of signal)') AS gone_tickets,
       count(*) FILTER (WHERE subject ~* '(hardly anything|nothing coming through|not gone off|quieter than usual|still very quiet|still on the list|pass this on)') AS quiet_tickets
     FROM rook.support_tickets GROUP BY 1)
   SELECT coalesce(p.wk, t.wk) AS week_start, p.pings, p.taken, p.turned_down, p.missed,
     c.callouts, c.unfilled, p.quiet4_pings, coalesce(t.tickets,0) AS tickets,
     coalesce(t.gone_tickets,0) AS gone_tickets, coalesce(t.quiet_tickets,0) AS quiet_tickets,
     c.secs_to_taker, l.below_half, l.above_150
   FROM p FULL JOIN t ON t.wk = p.wk LEFT JOIN c ON c.wk = coalesce(p.wk, t.wk)
     LEFT JOIN load l ON l.wk = coalesce(p.wk, t.wk) ORDER BY 1
   ```

   If the connector isn't available, say so and stop. Never make up numbers.
3. **Save the rows as CSV** in the session's scratchpad folder (or a temporary
   folder if there's no scratchpad), with the header
   `week_start,pings,taken,turned_down,missed,callouts,unfilled,quiet4_pings,tickets,gone_tickets,quiet_tickets,secs_to_taker,below_half,above_150`.
   Use `YYYY-MM-DD` dates, and leave empty cells for nulls. Copy the values exactly.
4. **Render the report:**
   `python3 .claude/skills/weekly-trends/render.py <that csv> <today as YYYY-MM-DD>`.
   This writes `reports/weekly-trends/<date>.md` (the tables) and
   `reports/weekly-trends/latest.html` (the charts).
5. **Summarize** in five lines or fewer:
   - which targets are on or off target this week, and how many acceptance criteria
     (AC1–AC9, from `dispatch-4.2-acceptance-test.md`) pass;
   - what moved since last week's report (read the previous dated `.md` in the
     folder, if there is one);
   - whether the fix has launched;
   - a warning if the script printed `STALE`, meaning there's been no new ping data
     for over two weeks.

## Rules

- Read and write only inside the course folder (plus the scratchpad). The
  connector is read-only.
- Don't change `config.json` without the student's OK. That includes the fix
  launch date and the targets.
- The targets come from the brief. If the brief's targets change, update
  `config.json` to match, after asking.
- Time-to-accept can't be reported until the pings table records answer times.
  Say so; don't estimate it.
- Don't save to GitHub unless asked. Don't save anything to memory.
