"""Generate the synthetic test data for routing scenarios.

Seeded, so running it again gives the same files. Every responder is
made up (TEST-xx). Nothing here comes from real responder records.

Writes:
  responders.csv  who exists, where they sit, how fast they answer
  callouts.csv    8 weeks of callouts: when, where, what tag they need
  responses.csv   for every callout x responder: are they available,
                  how many seconds they'd take to answer, would they say yes

responses.csv is fixed in advance so every scenario faces exactly the
same callouts and the same people answering the same way. Only the
routing rules change between scenarios.
"""

import csv
import math
import os
import random
from datetime import datetime, timedelta

SEED = 4242
DAYS = 56
CALLOUTS_PER_DAY = 20
START = datetime(2026, 7, 13)
CITY = 40.0  # the city is a 40 x 40 grid, in travel minutes
TAGS = ["flight", "structural-entry", "hazmat-tolerant", "cold-weather",
        "aquatic", "crowd-management", "de-escalation"]

# name, answer-speed cohort, area, chance they'd say yes when they answer
RESPONDERS = [
    ("TEST-01", "quick", "central", 0.85),
    ("TEST-02", "quick", "central", 0.85),
    ("TEST-03", "quick", "outer", 0.85),
    ("TEST-04", "steady", "central", 0.85),
    ("TEST-05", "steady", "outer", 0.85),
    ("TEST-06", "steady", "outer", 0.85),
    ("TEST-07", "steady", "central", 0.85),
    ("TEST-08", "slow", "central", 0.85),
    ("TEST-09", "slow", "central", 0.85),
    ("TEST-10", "slow", "outer", 0.85),
    ("TEST-11", "slow", "outer", 0.85),
    ("TEST-12", "disengaged", "central", 0.25),
]

# seconds to answer: mean, spread. "slow" is the stairs / one-boot-on
# responder from the interviews: nearly always inside 90s, mostly past 60s.
ANSWER_SPEED = {
    "quick": (18, 6),
    "steady": (42, 10),
    "slow": (70, 10),
    "disengaged": (20, 6),
}
NO_ANSWER_CHANCE = 0.03  # out of signal, phone in another room
AVAILABLE_CHANCE = 0.75


def main():
    rng = random.Random(SEED)
    here = os.path.dirname(os.path.abspath(__file__))

    responders = []
    for name, cohort, area, yes in RESPONDERS:
        if area == "central":
            r, a = rng.uniform(0, 8), rng.uniform(0, 2 * math.pi)
        else:
            r, a = rng.uniform(14, 19), rng.uniform(0, 2 * math.pi)
        x, y = CITY / 2 + r * math.cos(a), CITY / 2 + r * math.sin(a)
        tags = sorted(rng.sample(TAGS, 4))
        responders.append(dict(name=name, cohort=cohort, area=area,
                               x=round(x, 1), y=round(y, 1),
                               capabilities=";".join(tags), yes_chance=yes))

    callouts = []
    n = 0
    for day in range(DAYS):
        times = sorted(rng.uniform(0, 86400) for _ in range(CALLOUTS_PER_DAY))
        for t in times:
            n += 1
            callouts.append(dict(
                callout_number=n,
                at=(START + timedelta(days=day, seconds=t)).isoformat(timespec="seconds"),
                x=round(rng.uniform(0, CITY), 1), y=round(rng.uniform(0, CITY), 1),
                required_capability=rng.choice(TAGS)))

    responses = []
    for c in callouts:
        for r in responders:
            available = rng.random() < AVAILABLE_CHANCE
            mean, spread = ANSWER_SPEED[r["cohort"]]
            if rng.random() < NO_ANSWER_CHANCE:
                seconds = ""
            else:
                seconds = round(min(180, max(5, rng.gauss(mean, spread))))
            would_take = rng.random() < r["yes_chance"]
            travel = round(math.dist((r["x"], r["y"]), (c["x"], c["y"])) + 3, 1)
            responses.append(dict(callout_number=c["callout_number"], responder=r["name"],
                                  available=int(available), travel_minutes=travel,
                                  answer_seconds=seconds, would_take=int(would_take)))

    for fname, rows in [("responders.csv", responders), ("callouts.csv", callouts),
                        ("responses.csv", responses)]:
        with open(os.path.join(here, fname), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"{fname}: {len(rows)} rows")


if __name__ == "__main__":
    main()
