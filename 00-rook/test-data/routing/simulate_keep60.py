"""Fixes that keep the 60-second ping wait, run through the same test data.

Same harness as simulate.py (same callouts, same people answering the same
way, weeks 1-4 on 4.1 rules), but with two new rule options:

- late: the ping stays on the phone after 60s. We still move on to the next
  person at 60s, but whoever says yes first gets the callout. A late yes counts
  as a take.
- late_not_penalized: an answer that arrives after 60s (or after someone else
  took the callout) costs nothing. Only a real no, or no answer at all, costs.

Writes out/summary_keep60.md. Does not touch simulate.py's outputs.
"""

import os
from datetime import timedelta

import simulate
from simulate import V41, V42, history, routing, availability

LATE_CAP = 180  # the ping comes off the phone after this many seconds, filled or not

SCENARIOS = {
    "v4.1": V41,
    "v4.2-current": V42,
    "fix-a-timeout-90 (reference)": {**V42, "timeout": 90},
    "e1-late-answers-free": {**V42, "late_not_penalized": True},
    "e2-ping-stays-open": {**V42, "late": True, "late_not_penalized": True},
    "e3-stays-open-plus-ease-back": {**V42, "late": True, "late_not_penalized": True, "decay": 0.10},
    "e4-stays-open-late-no-costs": {**V42, "late": True, "late_not_penalized": True, "late_no_costs": True},
    "e4-from-floored-no-reset": {**V42, "late": True, "late_not_penalized": True, "late_no_costs": True,
                                 "slow_start_score": 0.0},
    "e4-from-floored-with-reset": {**V42, "late": True, "late_not_penalized": True, "late_no_costs": True,
                                   "slow_start_score": 0.5},
}


def run(rules, responders, callouts, responses):
    return run_plan(lambda week: rules if week >= simulate.SWITCH_WEEK else V41,
                    responders, callouts, responses)


def run_plan(plan, responders, callouts, responses, reset_week=None):
    """plan(week) gives the rules for that week. If reset_week is set, every
    score goes back to neutral at the start of that week (the one-time fresh start).
    """
    history._scores.clear()
    start = callouts[0].at
    pings, last_day, switched, was_reset = [], None, False, False
    for c in callouts:
        week = (c.at - start).days // 7 + 1
        active = plan(week)
        rules = active
        if reset_week is not None and week >= reset_week and not was_reset:
            history._scores.clear()
            was_reset = True
        if active is not V41 and rules.get("slow_start_score") is not None and not switched:
            # Stand-in for the real situation: slow responders already floored
            # by weeks of 4.2 rules (0.0), or given a fresh start (0.5).
            for r in responders.values():
                if r.cohort == "slow":
                    history._scores[r.name] = rules["slow_start_score"]
            switched = True
        simulate.apply_rules(active)
        day = (c.at - start).days
        if last_day is not None and day != last_day and active.get("decay"):
            for n in list(history._scores):
                s = history._scores[n]
                history._scores[n] = s + active["decay"] * (history.NEUTRAL_SCORE - s)
        last_day = day

        free = [r for r in responders.values() if responses[(c.number, r.name)]["available"]]
        availability.available_for = lambda region, at, free=free: free
        availability.travel_time_minutes = lambda r, loc: responses[(loc, r.name)]["travel"]

        window = LATE_CAP if active.get("late") else active["timeout"]
        sent_at, t, filled_at, sent = [], 0.0, None, []
        for r in routing.rank_for_callout(c):
            if filled_at is not None and t >= filled_at:
                break
            resp = responses[(c.number, r.name)]
            secs = resp["seconds"]
            answer_at = t + secs if secs is not None and secs <= window else None
            sent.append((r, t, resp, answer_at))
            if answer_at is not None and resp["would_take"]:
                filled_at = answer_at if filled_at is None else min(filled_at, answer_at)
            # Move on early only on a quick no; otherwise after the 60s wait.
            if answer_at is not None and not resp["would_take"] and secs <= active["timeout"]:
                t = answer_at
            else:
                t += active["timeout"]

        winner = None
        if filled_at is not None:
            winner = min((s for s in sent if s[3] is not None and s[2]["would_take"]),
                         key=lambda s: s[3])[0]
        for r, at, resp, answer_at in sent:
            on_time = answer_at is not None and resp["seconds"] <= active["timeout"]
            before_fill = answer_at is not None and (filled_at is None or answer_at <= filled_at)
            if r is winner:
                outcome = "taken"
            elif answer_at is not None and before_fill and not resp["would_take"]:
                outcome = "turned down"
            else:
                outcome = "missed"
            pings.append(dict(callout_number=c.number, responder=r.name,
                              sent_at=(c.at + timedelta(seconds=at)).isoformat(timespec="seconds"),
                              outcome=outcome, week=week, seconds=resp["seconds"],
                              to_fill=(filled_at if r is winner else 0)))
            if outcome == "taken":
                history.record_accepted(r)
            elif outcome == "turned down":
                if on_time or not active.get("late_not_penalized") or active.get("late_no_costs"):
                    history.record_declined(r)
            else:
                no_answer_at_all = resp["seconds"] is None or resp["seconds"] > LATE_CAP
                if not active.get("late_not_penalized") or no_answer_at_all:
                    history.record_declined(r)
    return pings


def main():
    responders, callouts, responses = simulate.load()
    results = {}
    for name, rules in SCENARIOS.items():
        pings = run(rules, responders, callouts, responses)
        results[name] = (simulate.metrics(pings, responders, simulate.BASELINE_WEEKS),
                         simulate.metrics(pings, responders, simulate.AFTER_WEEKS))

    v42_outer = results["v4.2-current"][1]["outer_share"]
    base = results["v4.1"][0]
    lines = ["# Keeping the 60-second ping wait: results", "",
             "Same test data and baseline as summary.md. Ping wait is 60s in every scenario "
             "except the 4.1 baseline and the fix-a reference.", "",
             "| Scenario | Acceptance | Missed share | Median secs to fill callout | Unfilled | "
             "Slow cohort pings/wk | Quick cohort pings/wk | Outer-area share | Disengaged pings/wk |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
             f"| baseline (4.1, wks 2-4) | {base['acceptance']:.0%} | {base['missed_share']:.0%} | "
             f"{base['median_fill']:.0f} | {base['unfilled']:.1%} | {base['cohort']['slow']:.1f} | "
             f"{base['cohort']['quick']:.1f} | {base['outer_share']:.0%} | {base['per_week']['TEST-12']:.1f} |"]
    for name, (b, a) in results.items():
        lines.append(f"| {name} | {a['acceptance']:.0%} | {a['missed_share']:.0%} | {a['median_fill']:.0f} | "
                     f"{a['unfilled']:.1%} | {a['cohort']['slow']:.1f} | {a['cohort']['quick']:.1f} | "
                     f"{a['outer_share']:.0%} | {a['per_week']['TEST-12']:.1f} |")

    lines += ["", "## Acceptance criteria (same as summary.md)", "",
              "| Scenario | AC1 slow cohort | AC2 nobody willing < 50% | AC3 acceptance | AC4 unfilled | "
              "AC5 outer share | AC6 disengaged |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for name, (b, a) in results.items():
        willing = [r for r in responders if responders[r].cohort != "disengaged" and b["per_week"][r] >= 3]
        worst = min(willing, key=lambda r: a["per_week"][r] / max(b["per_week"][r], 0.1))
        ratio = a["per_week"][worst] / max(b["per_week"][worst], 0.1)
        checks = [
            (a["cohort"]["slow"] >= 0.8 * b["cohort"]["slow"], f"{a['cohort']['slow'] / b['cohort']['slow']:.0%}"),
            (ratio >= 0.5, f"{worst} at {ratio:.0%}"),
            (a["acceptance"] >= b["acceptance"] - 0.02, f"{a['acceptance']:.0%} vs {b['acceptance']:.0%}"),
            (a["unfilled"] <= b["unfilled"] + 0.01, f"{a['unfilled']:.1%}"),
            (a["outer_share"] >= v42_outer - 0.005, f"{a['outer_share']:.0%}"),
            (a["per_week"]["TEST-12"] <= 2, f"{a['per_week']['TEST-12']:.1f}"),
        ]
        lines.append(f"| {name} | " + " | ".join(
            f"{'PASS' if ok else 'FAIL'} ({d})" for ok, d in checks) + " |")

    lines += ["", "## Pings per week by responder (baseline -> after)", "",
              "| Responder | Cohort | " + " | ".join(SCENARIOS) + " |",
              "| --- | --- | " + " | ".join("---" for _ in SCENARIOS) + " |"]
    for r in responders.values():
        lines.append(f"| {r.name} | {r.cohort} | " + " | ".join(
            f"{results[s][0]['per_week'][r.name]:.0f} -> {results[s][1]['per_week'][r.name]:.0f}"
            for s in SCENARIOS) + " |")

    out = os.path.join(simulate.HERE, "out", "summary_keep60.md")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
