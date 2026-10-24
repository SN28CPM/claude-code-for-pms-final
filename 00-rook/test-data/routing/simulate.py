"""Run the test data through the real routing code under each scenario.

Uses routing.py and history.py from 00-rook/code/dispatch-routing as-is
(only the tuning values are swapped per scenario). The phone side is
replaced by responses.csv: a responder answers if their answer time is
inside the offer window.

Every scenario runs weeks 1-4 on the 4.1 rules (the baseline), then
switches to the scenario's rules for weeks 5-8, the way 4.2 landed
mid-stream on 12 August.

Writes out/pings_<scenario>.csv (same columns as the rook.pings table)
and out/summary.md with the acceptance-criteria results.
"""

import csv
import os
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..", "..", "code", "dispatch-routing")
sys.path.insert(0, CODE)

import availability  # noqa: E402
import history  # noqa: E402
import routing  # noqa: E402

V41 = dict(timeout=90, w_prox=0.45, w_acc=0.40, missed_counts=True, decay=0.0)
V42 = dict(timeout=60, w_prox=0.60, w_acc=0.25, missed_counts=True, decay=0.0)
SCENARIOS = {
    "v4.1": V41,
    "v4.2-current": V42,
    "fix-a-timeout-90": {**V42, "timeout": 90},
    "fix-b-missed-not-penalized": {**V42, "missed_counts": False},
    "fix-c-score-eases-back": {**V42, "decay": 0.10},
    "fix-d-b-plus-c": {**V42, "missed_counts": False, "decay": 0.10},
}
SWITCH_WEEK = 5  # weeks 1-4 run on 4.1
BASELINE_WEEKS = (2, 3, 4)
AFTER_WEEKS = (6, 7, 8)


def load():
    def rows(name):
        with open(os.path.join(HERE, name)) as f:
            return list(csv.DictReader(f))
    responders = {r["name"]: SimpleNamespace(
        name=r["name"], cohort=r["cohort"], area=r["area"],
        capabilities=r["capabilities"].split(";")) for r in rows("responders.csv")}
    callouts = [SimpleNamespace(
        number=int(c["callout_number"]), at=datetime.fromisoformat(c["at"]),
        region="test-city", location=int(c["callout_number"]),
        required_capabilities=[c["required_capability"]]) for c in rows("callouts.csv")]
    responses = {}
    for r in rows("responses.csv"):
        responses[(int(r["callout_number"]), r["responder"])] = dict(
            available=r["available"] == "1", travel=float(r["travel_minutes"]),
            seconds=int(r["answer_seconds"]) if r["answer_seconds"] else None,
            would_take=r["would_take"] == "1")
    return responders, callouts, responses


def apply_rules(rules):
    routing.WEIGHT_PROXIMITY = rules["w_prox"]
    routing.WEIGHT_RECENT_ACCEPTANCE = rules["w_acc"]


def run(name, rules, responders, callouts, responses):
    history._scores.clear()
    start = callouts[0].at
    pings, last_day = [], None
    for c in callouts:
        week = (c.at - start).days // 7 + 1
        active = rules if week >= SWITCH_WEEK else V41
        apply_rules(active)
        day = (c.at - start).days
        if last_day is not None and day != last_day and active["decay"]:
            for n in list(history._scores):
                s = history._scores[n]
                history._scores[n] = s + active["decay"] * (history.NEUTRAL_SCORE - s)
        last_day = day

        free = [r for r in responders.values() if responses[(c.number, r.name)]["available"]]
        availability.available_for = lambda region, at, free=free: free
        availability.travel_time_minutes = (
            lambda r, loc: responses[(loc, r.name)]["travel"])

        sent = c.at
        for r in routing.rank_for_callout(c):
            resp = responses[(c.number, r.name)]
            answered = resp["seconds"] is not None and resp["seconds"] <= active["timeout"]
            if answered and resp["would_take"]:
                outcome = "taken"
            elif answered:
                outcome = "turned down"
            else:
                outcome = "missed"
            pings.append(dict(callout_number=c.number, responder=r.name,
                              sent_at=sent.isoformat(timespec="seconds"), outcome=outcome,
                              week=week, seconds=resp["seconds"],
                              to_fill=(sent - c.at).total_seconds() + (resp["seconds"] or 0)))
            if outcome == "taken":
                history.record_accepted(r)
                break
            if outcome == "turned down" or active["missed_counts"]:
                history.record_declined(r)
            sent += timedelta(seconds=resp["seconds"] if answered else active["timeout"])
    return pings


def metrics(pings, responders, weeks):
    sel = [p for p in pings if p["week"] in weeks]
    n_weeks = len(weeks)
    per = defaultdict(int)
    for p in sel:
        per[p["responder"]] += 1
    per_week = {r: per[r] / n_weeks for r in responders}
    taken = [p for p in sel if p["outcome"] == "taken"]
    callouts = {p["callout_number"] for p in sel}
    filled = {p["callout_number"] for p in taken}
    cohort = defaultdict(list)
    for r in responders.values():
        cohort[r.cohort].append(per_week[r.name])
    outer_taken = sum(1 for p in taken if responders[p["responder"]].area == "outer")
    willing = [v for r, v in per_week.items() if responders[r].cohort != "disengaged"]
    return dict(
        per_week=per_week,
        cohort={k: statistics.mean(v) for k, v in cohort.items()},
        acceptance=len(taken) / len(sel),
        missed_share=sum(p["outcome"] == "missed" for p in sel) / len(sel),
        median_tta=statistics.median(p["seconds"] for p in taken),
        unfilled=1 - len(filled) / len(callouts),
        outer_share=outer_taken / len(taken),
        spread=max(willing) / max(min(willing), 1),
        median_fill=statistics.median(p["to_fill"] for p in taken),
    )


def main():
    responders, callouts, responses = load()
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    results = {}
    for name, rules in SCENARIOS.items():
        pings = run(name, rules, responders, callouts, responses)
        with open(os.path.join(HERE, "out", f"pings_{name}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["callout_number", "responder", "sent_at", "outcome"])
            w.writeheader()
            w.writerows({k: p[k] for k in w.fieldnames} for p in pings)
        results[name] = (metrics(pings, responders, BASELINE_WEEKS),
                         metrics(pings, responders, AFTER_WEEKS),
                         dict(history._scores))

    v42_outer = results["v4.2-current"][1]["outer_share"]
    lines = ["# Routing scenarios: results", "",
             f"Baseline = weeks {BASELINE_WEEKS} on 4.1 rules. After = weeks {AFTER_WEEKS} "
             "on the scenario's rules.", "",
             "| Scenario | Acceptance | Missed share | Median secs to accept | Median secs to fill callout | Unfilled | "
             "Slow cohort pings/wk | Quick cohort pings/wk | Busiest / quietest | Outer-area share |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    base = results["v4.1"][0]
    lines.append(f"| baseline (4.1, wks 2-4) | {base['acceptance']:.0%} | {base['missed_share']:.0%} | "
                 f"{base['median_tta']:.0f} | {base['median_fill']:.0f} | {base['unfilled']:.1%} | {base['cohort']['slow']:.1f} | "
                 f"{base['cohort']['quick']:.1f} | {base['spread']:.1f}x | {base['outer_share']:.0%} |")
    for name, (b, a, _) in results.items():
        lines.append(f"| {name} | {a['acceptance']:.0%} | {a['missed_share']:.0%} | "
                     f"{a['median_tta']:.0f} | {a['median_fill']:.0f} | {a['unfilled']:.1%} | {a['cohort']['slow']:.1f} | "
                     f"{a['cohort']['quick']:.1f} | {a['spread']:.1f}x | {a['outer_share']:.0%} |")

    lines += ["", "## Acceptance criteria", "",
              "| Scenario | AC1 slow cohort >= 80% of baseline | AC2 nobody willing (>= 3/wk at baseline) < 50% of own baseline | "
              "AC3 acceptance >= baseline - 2 pts | AC4 unfilled <= baseline + 1 pt | "
              "AC5 outer share >= 4.2's | AC6 disengaged gets <= 2 pings/wk |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for name, (b, a, scores) in results.items():
        willing = [r for r in responders if responders[r].cohort != "disengaged"
                   and b["per_week"][r] >= 3]
        worst = min(willing, key=lambda r: a["per_week"][r] / max(b["per_week"][r], 0.1))
        worst_ratio = a["per_week"][worst] / max(b["per_week"][worst], 0.1)
        checks = [
            (a["cohort"]["slow"] >= 0.8 * b["cohort"]["slow"],
             f"{a['cohort']['slow'] / b['cohort']['slow']:.0%}"),
            (worst_ratio >= 0.5, f"{worst} at {worst_ratio:.0%}"),
            (a["acceptance"] >= b["acceptance"] - 0.02, f"{a['acceptance']:.0%} vs {b['acceptance']:.0%}"),
            (a["unfilled"] <= b["unfilled"] + 0.01, f"{a['unfilled']:.1%} vs {b['unfilled']:.1%}"),
            (a["outer_share"] >= v42_outer - 0.005, f"{a['outer_share']:.0%}"),
            (a["per_week"]["TEST-12"] <= 2, f"{a['per_week']['TEST-12']:.1f}"),
        ]
        lines.append(f"| {name} | " + " | ".join(
            f"{'PASS' if ok else 'FAIL'} ({detail})" for ok, detail in checks) + " |")

    lines += ["", "## Pings per week by responder (baseline -> after)", "",
              "| Responder | Cohort | Area | " + " | ".join(SCENARIOS) + " |",
              "| --- | --- | --- | " + " | ".join("---" for _ in SCENARIOS) + " |"]
    for r in responders.values():
        cells = [f"{results[s][0]['per_week'][r.name]:.0f} -> {results[s][1]['per_week'][r.name]:.0f}"
                 for s in SCENARIOS]
        lines.append(f"| {r.name} | {r.cohort} | {r.area} | " + " | ".join(cells) + " |")

    out = os.path.join(HERE, "out", "summary.md")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
