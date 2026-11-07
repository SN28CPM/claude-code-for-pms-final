"""Rule checks for the keep-60s proposal: one callout at a time, scripted answers.

Each case says who answers, after how many seconds, and yes or no, then checks
who got the job and what happened to everyone's score. Run: python3 test_rules.py
"""

from datetime import datetime
from types import SimpleNamespace

import simulate_keep60 as k
from simulate import V42, history

E4 = k.SCENARIOS["e4-stays-open-late-no-costs"]
E2 = k.SCENARIOS["e2-ping-stays-open"]
FIX_A = k.SCENARIOS["fix-a-timeout-90 (reference)"]


def one_callout(rules, answers):
    """answers: list of (seconds or None, yes) in ranked order (first = closest)."""
    names = [f"R{i}" for i in range(len(answers))]
    responders = {n: SimpleNamespace(name=n, cohort="test", area="central", capabilities=["flight"])
                  for n in names}
    callout = SimpleNamespace(number=1, at=datetime(2026, 9, 1, 12, 0), region="r", location=1,
                              required_capabilities=["flight"])
    responses = {(1, n): dict(available=True, travel=1 + 5 * i, seconds=s, would_take=yes)
                 for i, (n, (s, yes)) in enumerate(zip(names, answers))}
    pings = k.run_plan(lambda week: rules, responders, [callout], responses)
    scores = {n: round(history.recent_acceptance(responders[n]), 2) for n in names}
    outcomes = {p["responder"]: p["outcome"] for p in pings}
    sent = {p["responder"]: p["sent_at"][-5:] for p in pings}
    return outcomes, scores, sent


CASES = [
    # name, rules, answers, expected outcomes, expected scores
    ("Late yes still wins if it beats the next person",
     E4, [(70, True), (30, True)], {"R0": "taken", "R1": "missed"}, {"R0": 0.58, "R1": 0.5}),
    ("Covered by someone faster: no cost to the late responder",
     E4, [(70, True), (5, True)], {"R0": "missed", "R1": "taken"}, {"R0": 0.5, "R1": 0.58}),
    ("A late no still costs (loophole closed)",
     E4, [(70, False), (30, True)], {"R0": "turned down", "R1": "taken"}, {"R0": 0.38, "R1": 0.58}),
    ("A late no was free under the first draft (the loophole)",
     E2, [(70, False), (30, True)], {"R0": "turned down", "R1": "taken"}, {"R0": 0.5, "R1": 0.58}),
    ("Never answering still costs",
     E4, [(None, True), (20, True)], {"R0": "missed", "R1": "taken"}, {"R0": 0.38, "R1": 0.58}),
    ("Answering after the 3-minute cap counts as no answer",
     E4, [(181, True), (20, True)], {"R0": "missed", "R1": "taken"}, {"R0": 0.38, "R1": 0.58}),
    ("A quick no costs and moves on straight away",
     E4, [(10, False), (20, True)], {"R0": "turned down", "R1": "taken"}, {"R0": 0.38, "R1": 0.58}),
    ("Nobody says yes: callout unfilled, everyone charged as today",
     E4, [(None, True), (15, False)], {"R0": "missed", "R1": "turned down"}, {"R0": 0.38, "R1": 0.38}),
    ("4.2 today: a 70s yes is a miss and costs",
     V42, [(70, True), (20, True)], {"R0": "missed", "R1": "taken"}, {"R0": 0.38, "R1": 0.58}),
    ("90s reference: a 70s yes is a take",
     FIX_A, [(70, True), (20, True)], {"R0": "taken"}, {"R0": 0.58, "R1": 0.5}),
]


def main():
    failed = 0
    for name, rules, answers, want_out, want_scores in CASES:
        outcomes, scores, sent = one_callout(rules, answers)
        ok = outcomes == want_out and scores == want_scores
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"      outcomes {outcomes} (wanted {want_out})")
            print(f"      scores   {scores} (wanted {want_scores})")
    # Timing: after a quick no, the next ping goes out at the moment of the no.
    _, _, sent = one_callout(E4, [(10, False), (20, True)])
    ok = sent == {"R0": "00:00", "R1": "00:10"}
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  Next ping goes out right after a quick no ({sent})")
    # Timing: with no answer, the next ping goes out at 60s, not later.
    _, _, sent = one_callout(E4, [(70, True), (30, True)])
    ok = sent == {"R0": "00:00", "R1": "01:00"}
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  Next ping still goes out at 60s ({sent})")
    print(f"\n{len(CASES) + 2 - failed} passed, {failed} failed")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
