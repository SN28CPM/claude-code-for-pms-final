"""Stress test: every fix, many random seeds, a realistic timeline, and what-ifs.

Timeline (12 weeks): weeks 1-4 on 4.1 rules, weeks 5-8 on 4.2 rules (the damage
happens, scores sink), weeks 9-12 on the fix. "Before" = weeks 2-4, "after" =
weeks 10-12. That's closer to reality than simulate.py, where the fix starts
from healthy scores.

Data is built in memory the same way generate.py builds it, with a different
seed each run and some knobs to turn. Nothing on disk is overwritten except
out/stress_test.md. Run: python3 stress_test.py  (takes a minute or two)
"""

import math
import os
import random
import statistics
from datetime import datetime, timedelta
from types import SimpleNamespace

import generate
import simulate
import simulate_keep60 as k
from simulate import V41, V42

WEEKS = 12
FIX_WEEK = 9
BEFORE, AFTER = (2, 3, 4), (10, 11, 12)
SEEDS = range(1, 21)

FIXES = {
    "4.2 left as is": dict(rules=V42),
    "Back to 90s": dict(rules={**V42, "timeout": 90}),
    "Back to 90s + fresh start": dict(rules={**V42, "timeout": 90}, reset=True),
    "60s, late answers free": dict(rules={**V42, "late_not_penalized": True}),
    "60s, late answers free + fresh start": dict(rules={**V42, "late_not_penalized": True}, reset=True),
    "Proposal, no fresh start": dict(rules=k.SCENARIOS["e4-stays-open-late-no-costs"]),
    "Proposal + fresh start": dict(rules=k.SCENARIOS["e4-stays-open-late-no-costs"], reset=True),
    "Proposal + fresh start + ease-back": dict(
        rules={**k.SCENARIOS["e4-stays-open-late-no-costs"], "decay": 0.10}, reset=True),
    "First draft (late no free) + fresh start": dict(rules=k.SCENARIOS["e2-ping-stays-open"], reset=True),
}


def build(seed, slow_mean=70, no_answer=0.03, available=0.75, extra=()):
    """Same recipe as generate.py, in memory. extra adds (name, cohort, area, yes, mean, spread)."""
    rng = random.Random(seed)
    speeds = {**generate.ANSWER_SPEED, "slow": (slow_mean, 10)}
    people = [(n, c, a, y, *speeds[c]) for n, c, a, y in generate.RESPONDERS] + list(extra)
    responders = {}
    for name, cohort, area, yes, mean, spread in people:
        r = rng.uniform(0, 8) if area == "central" else rng.uniform(14, 19)
        a = rng.uniform(0, 2 * math.pi)
        responders[name] = SimpleNamespace(
            name=name, cohort=cohort, area=area, yes=yes, mean=mean, spread=spread,
            x=generate.CITY / 2 + r * math.cos(a), y=generate.CITY / 2 + r * math.sin(a),
            capabilities=rng.sample(generate.TAGS, 4))
    callouts, responses, n = [], {}, 0
    for day in range(WEEKS * 7):
        for t in sorted(rng.uniform(0, 86400) for _ in range(generate.CALLOUTS_PER_DAY)):
            n += 1
            x, y = rng.uniform(0, generate.CITY), rng.uniform(0, generate.CITY)
            callouts.append(SimpleNamespace(
                number=n, at=generate.START + timedelta(days=day, seconds=t), region="test-city",
                location=n, required_capabilities=[rng.choice(generate.TAGS)]))
            for r in responders.values():
                avail = rng.random() < available
                secs = None if rng.random() < no_answer else round(min(180, max(5, rng.gauss(r.mean, r.spread))))
                responses[(n, r.name)] = dict(available=avail, travel=round(math.dist((r.x, r.y), (x, y)) + 3, 1),
                                              seconds=secs, would_take=rng.random() < r.yes)
    return responders, callouts, responses


def run_fix(fix, data):
    responders, callouts, responses = data
    plan = lambda w: V41 if w < 5 else (V42 if w < FIX_WEEK else fix["rules"])
    pings = k.run_plan(plan, responders, callouts, responses,
                       reset_week=FIX_WEEK if fix.get("reset") else None)
    b = simulate.metrics(pings, responders, BEFORE)
    a = simulate.metrics(pings, responders, AFTER)
    sel = [p for p in pings if p["week"] in AFTER]
    a["pings_per_callout"] = len(sel) / len({p["callout_number"] for p in sel})
    a["busiest"] = max(a["per_week"].values())
    return b, a


def checks(b, a, v42_outer, watch=("TEST-12",)):
    willing = [r for r in b["per_week"] if r not in watch and b["per_week"][r] >= 3]
    worst = min(a["per_week"][r] / max(b["per_week"][r], 0.1) for r in willing)
    return dict(
        AC1=a["cohort"]["slow"] >= 0.8 * b["cohort"]["slow"],
        AC2=worst >= 0.5,
        AC3=a["acceptance"] >= b["acceptance"] - 0.02,
        AC4=a["unfilled"] <= b["unfilled"] + 0.01,
        AC5=a["outer_share"] >= v42_outer - 0.005,
        AC6=all(a["per_week"][w] <= 2 for w in watch),
    )


def sweep(fixes, seeds, **knobs):
    rows = {name: [] for name in fixes}
    for seed in seeds:
        data = build(seed, **knobs)
        res = {name: run_fix(FIXES[name], data) for name in fixes}
        v42_outer = run_fix(FIXES["4.2 left as is"], data)[1]["outer_share"]
        watch = tuple(n for n, r in data[0].items() if r.cohort in ("disengaged", "late-decliner"))
        for name, (b, a) in res.items():
            rows[name].append((b, a, checks(b, a, v42_outer, watch)))
    return rows


def mid(vals):
    vals = sorted(vals)
    return f"{statistics.median(vals):.1f} ({vals[len(vals) // 10]:.1f}–{vals[-1 - len(vals) // 10]:.1f})"


def table(rows, cols):
    head = "| Fix | " + " | ".join(c for c, _ in cols) + " |"
    lines = [head, "|" + " --- |" * (len(cols) + 1)]
    for name, rs in rows.items():
        lines.append(f"| {name} | " + " | ".join(f(rs) for _, f in cols) + " |")
    return lines


def pct(key):
    return lambda rs: f"{statistics.median(a[key] for _, a, _ in rs):.0%}"


def main():
    out = ["# Stress test results", "",
           f"Timeline: weeks 1-4 on 4.1, weeks 5-8 on 4.2, fix from week {FIX_WEEK}. Before = weeks 2-4, "
           f"after = weeks 10-12. Numbers are medians over {len(SEEDS)} random seeds, with the "
           "10th–90th percentile range in brackets. Synthetic responders only.", ""]

    # 1. Every fix, 20 seeds, default assumptions.
    rows = sweep(list(FIXES), SEEDS)
    base = [b for b, _, _ in rows["4.2 left as is"]]
    out += ["## 1. Every fix, default assumptions (slow responders answer in about 70s)", "",
            f"Before (4.1): slow responders {mid([b['cohort']['slow'] for b in base])} pings/wk, "
            f"acceptance {statistics.median(b['acceptance'] for b in base):.0%}, "
            f"median fill {statistics.median(b['median_fill'] for b in base):.0f}s.", ""]
    out += table(rows, [
        ("Slow pings/wk", lambda rs: mid([a["cohort"]["slow"] for _, a, _ in rs])),
        ("Quick pings/wk", lambda rs: mid([a["cohort"]["quick"] for _, a, _ in rs])),
        ("Busiest responder/wk", lambda rs: mid([a["busiest"] for _, a, _ in rs])),
        ("Acceptance per ping", pct("acceptance")),
        ("Unfilled", lambda rs: f"{statistics.median(a['unfilled'] for _, a, _ in rs):.1%}"),
        ("Median secs to fill", lambda rs: f"{statistics.median(a['median_fill'] for _, a, _ in rs):.0f}"),
        ("Pings per callout", lambda rs: f"{statistics.median(a['pings_per_callout'] for _, a, _ in rs):.2f}"),
        ("Disengaged/wk", lambda rs: mid([a["per_week"]["TEST-12"] for _, a, _ in rs])),
    ])
    out += ["", "### How often each acceptance check passes (out of 20 seeds)", ""]
    out += table(rows, [(ac, (lambda ac: lambda rs: str(sum(c[ac] for _, _, c in rs)))(ac))
                        for ac in ("AC1", "AC2", "AC3", "AC4", "AC5", "AC6")])
    out += ["", "AC1 slow cohort ≥ 80% of before · AC2 no willing responder below half their own before · "
            "AC3 acceptance per ping within 2 pts · AC4 unfilled within 1 pt · AC5 wide-area share ≥ 4.2's · "
            "AC6 disengaged ≤ 2 pings/wk"]

    # 2. What if slow responders are faster or slower than we assumed?
    key = ["4.2 left as is", "Back to 90s + fresh start", "Proposal + fresh start"]
    out += ["", "## 2. What if our guess about answer speed is wrong? (slow pings/wk after, 10 seeds)", "",
            "| Slow responders answer in about… | " + " | ".join(key) + " | Proposal: median secs to fill |",
            "|" + " --- |" * (len(key) + 2)]
    for mean in (62, 70, 80, 100, 130):
        r = sweep(key, range(1, 11), slow_mean=mean)
        out.append(f"| {mean}s | " + " | ".join(mid([a["cohort"]["slow"] for _, a, _ in r[n]]) for n in key)
                   + f" | {statistics.median(a['median_fill'] for _, a, _ in r['Proposal + fresh start']):.0f} |")

    # 3. Patchy signal and thin availability.
    out += ["", "## 3. Patchy signal and fewer people free (10 seeds)", "",
            "| Condition | Fix | Slow pings/wk | Unfilled | Median secs to fill |", "| --- | --- | --- | --- | --- |"]
    for label, knobs in [("No answer 10% of the time", dict(no_answer=0.10)),
                         ("Only 50% of people free", dict(available=0.50)),
                         ("Only 30% of people free", dict(available=0.30))]:
        r = sweep(key, range(1, 11), **knobs)
        for n in key:
            out.append(f"| {label} | {n} | {mid([a['cohort']['slow'] for _, a, _ in r[n]])} | "
                       f"{statistics.median(a['unfilled'] for _, a, _ in r[n]):.1%} | "
                       f"{statistics.median(a['median_fill'] for _, a, _ in r[n]):.0f} |")

    # 4. Gaming: someone who waits past 60s and then says no.
    extra = [("TEST-13", "late-decliner", "central", 0.25, 75, 8)]
    gk = ["4.2 left as is", "First draft (late no free) + fresh start", "Proposal + fresh start"]
    r = sweep(gk, range(1, 11), extra=extra)
    out += ["", "## 4. Gaming check: a responder who waits past 60s, then mostly says no (10 seeds)", "",
            "| Fix | Late-decliner pings/wk | Disengaged (quick no) pings/wk |", "| --- | --- | --- |"]
    for n in gk:
        out.append(f"| {n} | {mid([a['per_week']['TEST-13'] for _, a, _ in r[n]])} | "
                   f"{mid([a['per_week']['TEST-12'] for _, a, _ in r[n]])} |")

    path = os.path.join(simulate.HERE, "out", "stress_test.md")
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
