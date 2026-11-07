"""Turn the weekly numbers into a report: a dated Markdown file and latest.html.

Usage (from the course folder):
    python3 .claude/skills/weekly-trends/render.py <weekly.csv> [<run date YYYY-MM-DD>]

weekly.csv has one row per week, the columns returned by the skill's query:
week_start, pings, taken, turned_down, missed, callouts, unfilled,
quiet4_pings, tickets, gone_tickets, quiet_tickets
Empty cells mean "no data that week". Settings come from config.json next to
this file (release date, fix launch date, targets, where reports go).
"""

import csv
import json
import os
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def num(v):
    return None if v in (None, "", "null") else float(v)


def monday(d):
    return d - timedelta(days=d.weekday())


def load(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            row = {k: num(v) for k, v in r.items() if k != "week_start"}
            row["week"] = date.fromisoformat(r["week_start"][:10])
            p = row["pings"]
            row["taken_pct"] = row["taken"] / p * 100 if p else None
            row["missed_pct"] = row["missed"] / p * 100 if p else None
            row["unfilled_pct"] = row["unfilled"] / row["callouts"] * 100 if row.get("callouts") else None
            row["turned_pct"] = row["turned_down"] / p * 100 if p else None
            row["per_callout"] = p / row["callouts"] if p and row.get("callouts") else None
            row["callout_tickets"] = (row.get("gone_tickets") or 0) + (row.get("quiet_tickets") or 0)
            rows.append(row)
    return sorted(rows, key=lambda r: r["week"])


def period(week, cfg):
    rel = monday(date.fromisoformat(cfg["release_4_2"]))
    fix = cfg.get("fix_launch")
    if fix and week >= monday(date.fromisoformat(fix)):
        return "fix" if week > monday(date.fromisoformat(fix)) else "fix week"
    if week < rel:
        return "before 4.2"
    return "4.2 week" if week == rel else "after 4.2"


def avg(rows, key):
    vals = [r[key] for r in rows if r.get(key) is not None]
    return sum(vals) / len(vals) if vals else None


def fmt(v, unit="", digits=1):
    return "–" if v is None else f"{v:.{digits}f}{unit}"


def chart(rows, series, cfg, title, unit, ymax=None):
    """A small line chart as inline SVG. series: [(key, label, css class, dashed)]."""
    W, H, L, R, T, B = 640, 190, 40, 12, 24, 30
    weeks = [r["week"] for r in rows]
    vals = [r[k] for r in rows for k, *_ in series if r.get(k) is not None]
    top = ymax or (max(vals) * 1.15 if vals else 1) or 1
    x = lambda i: L + (W - L - R) * (i / max(len(weeks) - 1, 1))
    y = lambda v: T + (H - T - B) * (1 - v / top)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{title}"><title>{title}</title>']
    for g in range(5):
        gv = top * g / 4
        out.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(gv):.1f}" y2="{y(gv):.1f}"/>'
                   f'<text class="tick" x="{L - 6}" y="{y(gv) + 4:.1f}" text-anchor="end">{gv:.0f}{unit}</text>')
    for i, w in enumerate(weeks):
        if i % max(1, len(weeks) // 8) == 0 or i == len(weeks) - 1:
            out.append(f'<text class="tick" x="{x(i):.1f}" y="{H - 10}" text-anchor="middle">{w.day} {w.strftime("%b")}</text>')
    marks = [(cfg["release_4_2"], "4.2")] + ([(cfg["fix_launch"], "fix")] if cfg.get("fix_launch") else [])
    for d, label in marks:
        wk = monday(date.fromisoformat(d))
        if weeks and weeks[0] <= wk <= weeks[-1]:
            i = weeks.index(min(weeks, key=lambda w: abs((w - wk).days)))
            out.append(f'<line class="mark" x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{T - 6}" y2="{H - B}"/>'
                       f'<text class="tick" x="{x(i) + 4:.1f}" y="{T - 8}">{label}</text>')
    for key, label, cls, dashed in series:
        pts = [(x(i), y(r[key])) for i, r in enumerate(rows) if r.get(key) is not None]
        if pts:
            d = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
            dash = ' stroke-dasharray="6 4"' if dashed else ""
            out.append(f'<polyline class="line {cls}" points="{d}"{dash}/>')
            out += [f'<circle class="dot {cls}" cx="{px:.1f}" cy="{py:.1f}" r="3"/>' for px, py in pts]
    out.append("</svg>")
    legend = "".join(f'<span><i class="sw {cls}{" dash" if dashed else ""}"></i>{label}</span>' for _, label, cls, dashed in series)
    return f'<figure><figcaption>{title}</figcaption><div class="legend">{legend}</div>{"".join(out)}</figure>'


def main():
    cfg = json.load(open(os.path.join(HERE, "config.json")))
    rows = load(sys.argv[1])
    run = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()
    for r in rows:
        r["period"] = period(r["week"], cfg)
    data = [r for r in rows if r.get("pings") is not None]
    last_data = data[-1]["week"] if data else None
    t = cfg["targets"]
    n_quiet = len(cfg["quiet_responders"])

    groups = ["before 4.2", "after 4.2"] + (["fix"] if cfg.get("fix_launch") else [])
    summary = {g: [r for r in data if r["period"] == g] for g in groups}
    tk = {g: [r for r in rows if r["period"] == g] for g in groups}
    latest = data[-1] if data else {}

    def status(ok):
        return "on target" if ok else "off target"

    checks = [
        ("Missed pings", f"≤ {t['missed_pct_max']:.0f}%", latest.get("missed_pct"), "%",
         latest.get("missed_pct") is not None and latest["missed_pct"] <= t["missed_pct_max"]),
        (f"Pings to the {n_quiet} quiet responders", f"≥ {t['quiet_pings_each_min'] * n_quiet} a week ({t['quiet_pings_each_min']} each)",
         latest.get("quiet4_pings"), "", (latest.get("quiet4_pings") or 0) >= t["quiet_pings_each_min"] * n_quiet),
        ("Callouts nobody took", f"≤ {t['unfilled_pct_max']:.0f}%", latest.get("unfilled_pct"), "%",
         latest.get("unfilled_pct") is not None and latest["unfilled_pct"] <= t["unfilled_pct_max"]),
        ("New quiet-responder tickets", f"{t['quiet_tickets_max']}", latest.get("quiet_tickets"), "",
         (latest.get("quiet_tickets") or 0) <= t["quiet_tickets_max"]),
    ]

    fix_line = (f"Fix launched {cfg['fix_launch']}." if cfg.get("fix_launch")
                else "The fix hasn't launched yet. Set `fix_launch` in `.claude/skills/weekly-trends/config.json` on launch day to start the \"after the fix\" column.")
    stale = ""
    if last_data and (date.fromisoformat(run) - last_data).days > 14:
        stale = (f"**No new ping data since the week of {last_data.day} {last_data.strftime('%b %Y')}.** "
                 "The numbers below haven't moved; check with Ravi that the pings table is still being filled.")

    md = [f"# Weekly trends: {run}", "", f"Release 4.2 shipped {cfg['release_4_2']}. {fix_line}", ""]
    if stale:
        md += [stale, ""]
    md += ["## Averages per week, by period", "",
           "| Measure | " + " | ".join(groups) + " |", "|" + " --- |" * (len(groups) + 1)]
    for label, key, unit in [("Pings", "pings", ""), ("Taken", "taken_pct", "%"), ("Missed", "missed_pct", "%"),
                             ("Callouts nobody took", "unfilled_pct", "%"), (f"Pings to the {n_quiet} quiet responders", "quiet4_pings", "")]:
        md.append(f"| {label} | " + " | ".join(fmt(avg(summary[g], key), unit, 1 if unit else 0) for g in groups) + " |")
    for label, key in [("Tickets", "tickets"), ("Gone-before-answering tickets", "gone_tickets"), ("Quiet-responder tickets", "quiet_tickets")]:
        md.append(f"| {label} | " + " | ".join(fmt(avg(tk[g], key)) for g in groups) + " |")
    md += ["", "The release week itself (and the fix's launch week) is left out of these averages.",
           "", f"## Latest week with ping data ({latest.get('week', '–')}) against the brief's targets", "",
           "| Measure | Target | Latest | Status |", "| --- | --- | --- | --- |"]
    for label, target, v, unit, ok in checks:
        md.append(f"| {label} | {target} | {fmt(v, unit)} | {status(ok)} |")
    ac = cfg.get("acceptance_criteria", {})
    ac_defs = [
        ("AC1 Taken", "taken_pct", "%", ">=", ac.get("AC1_taken_pct_min")),
        ("AC2 Missed", "missed_pct", "%", "<=", ac.get("AC2_missed_pct_max")),
        ("AC3 Turned down", "turned_pct", "%", "<=", ac.get("AC3_turned_down_pct_max")),
        ("AC4 Nobody took it", "unfilled_pct", "%", "<=", ac.get("AC4_unfilled_pct_max")),
        ("AC5 Pings per callout", "per_callout", "", "<=", ac.get("AC5_pings_per_callout_max")),
        ("AC6 Secs to reach taker", "secs_to_taker", "s", "<=", ac.get("AC6_secs_to_taker_max")),
        ("AC7 Responders below half", "below_half", "", "<=", ac.get("AC7_below_half_max")),
        ("AC8 Responders above 1.5×", "above_150", "", "<=", ac.get("AC8_above_150_max")),
        ("AC9 Callout tickets", "callout_tickets", "", "<=", ac.get("AC9_callout_tickets_max")),
    ]
    ac_defs = [d for d in ac_defs if d[4] is not None]

    def ac_cell(r, key, unit, op, lim):
        v = r.get(key)
        if v is None:
            return "–", None
        ok = v >= lim if op == ">=" else v <= lim
        digits = 2 if key == "per_callout" else (1 if unit == "%" else 0)
        return f"{fmt(v, unit, digits)} {'✓' if ok else '✗'}", ok

    ac_rows = [r for r in data if r["period"] != "before 4.2"][-8:]
    ac_summary = []
    if ac_defs and ac_rows:
        md += ["", f"## Acceptance criteria, week by week (limits from {ac.get('source', 'config')})", "",
               "| Criterion | Limit | " + " | ".join(str(r["week"]) for r in ac_rows) + " |",
               "|" + " --- |" * (len(ac_rows) + 2)]
        for label, key, unit, op, lim in ac_defs:
            cells = [ac_cell(r, key, unit, op, lim) for r in ac_rows]
            md.append(f"| {label} | {'≥' if op == '>=' else '≤'} {lim:g}{unit} | " + " | ".join(c for c, _ in cells) + " |")
            ac_summary.append((label, cells[-1][1]))
        passed = sum(1 for _, ok in ac_summary if ok)
        md += ["", f"Latest week: **{passed} of {len(ac_summary)} criteria pass.**"]

    md += ["", "Time-to-accept (guardrail ≤ 43s) can't be shown yet: the pings table doesn't record answer times.", "",
           "## Week by week", "",
           "| Week of | Period | Pings | Taken | Missed | Unfilled | Quiet 4 pings | Tickets (gone / quiet) |",
           "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        md.append(f"| {r['week']} | {r['period']} | {fmt(r.get('pings'), '', 0)} | {fmt(r.get('taken_pct'), '%')} | "
                  f"{fmt(r.get('missed_pct'), '%')} | {fmt(r.get('unfilled_pct'), '%')} | {fmt(r.get('quiet4_pings'), '', 0)} | "
                  f"{fmt(r.get('tickets'), '', 0)} ({fmt(r.get('gone_tickets'), '', 0)} / {fmt(r.get('quiet_tickets'), '', 0)}) |")

    charts = "".join([
        chart(data, [("taken_pct", "Taken", "c1", False), ("missed_pct", "Missed", "c2", True)], cfg, "Share of pings taken and missed", "%", 100),
        chart(data, [("quiet4_pings", f"Pings to the {n_quiet} quiet responders", "c3", False)], cfg, f"Pings to {', '.join(cfg['quiet_responders'])}", ""),
        chart(data, [("unfilled_pct", "Callouts nobody took", "c2", False)], cfg, "Callouts nobody took", "%"),
        chart(rows, [("gone_tickets", "Gone before answering", "c2", True), ("quiet_tickets", "Quiet responder", "c4", False)], cfg, "Support tickets by type", ""),
    ])
    cards = "".join(f'<div class="card"><div class="lbl">{label}</div><div class="val">{fmt(v, unit)}</div>'
                    f'<div class="st {"ok" if ok else "bad"}">{status(ok)} · target {target}</div></div>'
                    for label, target, v, unit, ok in checks)
    ac_html = ""
    if ac_summary:
        head = "".join(f"<th>{r['week'].day} {r['week'].strftime('%b')}</th>" for r in ac_rows)
        body = ""
        for label, key, unit, op, lim in ac_defs:
            tds = ""
            for r in ac_rows:
                text, ok = ac_cell(r, key, unit, op, lim)
                tds += f'<td class="{"" if ok is None else ("ok" if ok else "bad")}">{text}</td>'
            body += f"<tr><th>{label} <span class='lim'>{'≥' if op == '>=' else '≤'} {lim:g}{unit}</span></th>{tds}</tr>"
        passed = sum(1 for _, ok in ac_summary if ok)
        ac_html = (f'<figure><figcaption>Acceptance criteria: {passed} of {len(ac_summary)} pass in the latest week</figcaption>'
                   f'<div class="tbl"><table><tr><th></th>{head}</tr>{body}</table></div></figure>')
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weekly Trends</title><style>
:root{{--bg:#f7f6f2;--card:#fff;--ink:#1b1b19;--ink2:#55544f;--muted:#8a8982;--line:#e1e0d9;--c1:#2a78d6;--c2:#e34948;--c3:#1baf7a;--c4:#eda100;--ok:#1d7a4f;--bad:#b4322f}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#141413;--card:#1e1e1c;--ink:#efeee9;--ink2:#c3c2b7;--line:#2c2c2a;--c1:#3987e5;--c2:#e66767;--c3:#199e70;--c4:#c98500;--ok:#7fd3a6;--bad:#f08b88}}}}
:root[data-theme="dark"]{{--bg:#141413;--card:#1e1e1c;--ink:#efeee9;--ink2:#c3c2b7;--line:#2c2c2a;--c1:#3987e5;--c2:#e66767;--c3:#199e70;--c4:#c98500;--ok:#7fd3a6;--bad:#f08b88}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
.wrap{{max-width:900px;margin:0 auto;padding:20px 16px 40px}}h1{{font-size:22px;margin:0 0 4px}}.sub{{color:var(--ink2);margin:0 0 14px}}
.warn{{background:var(--card);border-left:4px solid var(--c4);padding:10px 12px;margin:0 0 14px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:18px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}}.lbl{{font-size:13px;color:var(--ink2)}}.val{{font-size:24px;font-weight:600}}
.st{{font-size:12px}}.ok{{color:var(--ok)}}.bad{{color:var(--bad)}}
figure{{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 12px;padding:12px}}figcaption{{font-weight:600;margin-bottom:4px}}
svg{{width:100%;height:auto}}.grid{{stroke:var(--line)}}.tick{{fill:var(--muted);font-size:11px}}.mark{{stroke:var(--muted);stroke-dasharray:4 4}}
.line{{fill:none;stroke-width:2}}.dot{{stroke:var(--card);stroke-width:1.5}}
.c1{{stroke:var(--c1)}}.dot.c1{{fill:var(--c1)}}.c2{{stroke:var(--c2)}}.dot.c2{{fill:var(--c2)}}.c3{{stroke:var(--c3)}}.dot.c3{{fill:var(--c3)}}.c4{{stroke:var(--c4)}}.dot.c4{{fill:var(--c4)}}
.legend{{display:flex;gap:14px;font-size:12px;color:var(--ink2);margin-bottom:4px}}.legend span{{display:flex;align-items:center;gap:5px}}
.sw{{width:16px;border-top:2px solid}}.sw.dash{{border-top-style:dashed}}.sw.c1{{border-color:var(--c1)}}.sw.c2{{border-color:var(--c2)}}.sw.c3{{border-color:var(--c3)}}.sw.c4{{border-color:var(--c4)}}
.foot{{color:var(--muted);font-size:12px}}
.tbl{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}}
th,td{{padding:6px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}}th:first-child{{text-align:left}}
tr th{{font-weight:500;color:var(--ink2)}}.lim{{color:var(--muted);font-size:12px}}
</style></head><body><div class="wrap">
<h1>Weekly trends</h1><p class="sub">Run {run} · Release 4.2 shipped {cfg['release_4_2']} · {fix_line.replace('`', '')}</p>
{f'<div class="warn">{stale.replace("**", "")}</div>' if stale else ''}
<div class="cards">{cards}</div>{ac_html}{charts}
<p class="foot">Source: rook.pings and rook.support_tickets. Dashed lines mark the 4.2 release and the fix launch. Full tables: {run}.md in this folder.</p>
</div></body></html>"""

    out_dir = os.path.join(ROOT, cfg["report_dir"])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, f"{run}.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    with open(os.path.join(out_dir, "latest.html"), "w") as f:
        f.write(html)
    print(f"Wrote {cfg['report_dir']}/{run}.md and {cfg['report_dir']}/latest.html")
    if stale:
        print("STALE:", stale)


if __name__ == "__main__":
    main()
