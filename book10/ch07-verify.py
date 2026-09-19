#!/usr/bin/env python3
"""Recompute every number Book X chapter 7 prints, from the series beside it.

Usage:  python3 book10/ch07-verify.py

Chapter 7 makes one claim about the Gapminder misconception study and one about
South Korea. Neither is quoted from a secondary source: the Korean figures are
computed here from `book10/ch07-korea-worldbank.tsv`, which is the World Bank
series as retrieved on 2026-09-19 with the indicator codes and the API path in
its header, so a reader can pull it again and diff.

The ordering claim is the chapter's contribution and it is stated precisely:
for each of four series, the year at which half the 1960-2020 change had
happened. The order those four years come in is the whole argument, and it is
recomputed every time this script runs.

The script also reads the page and fails if it has stopped printing what the
arithmetic says. A chapter that has drifted from its own numbers is the failure
this corpus keeps finding; a script that reads the page is the only guard that
does not depend on anyone remembering.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TSV = ROOT / "book10" / "ch07-korea-worldbank.tsv"
PAGE = ROOT / "book10" / "ch07-up-before-right.html"

SERIES = [("under5_mortality_per_1000", "under-5 mortality", True),
          ("total_fertility_rate",      "births per woman",  True),
          ("life_expectancy",           "life expectancy",   False),
          ("gdp_pc_const2015usd",       "GDP per capita",    False)]


def load():
    lines = [l for l in TSV.read_text(encoding="utf-8").split("\n")
             if l and not l.startswith("#")]
    head = lines[0].split("\t")
    data = {h: {} for h in head[1:]}
    for l in lines[1:]:
        c = l.split("\t")
        y = int(c[0])
        for i, h in enumerate(head[1:], start=1):
            if i < len(c) and c[i]:
                data[h][y] = float(c[i])
    return data


def halfway(s, falling, y0=1960, y1=2020):
    """Year, by linear interpolation, at which half the y0-to-y1 change was in."""
    target = s[y0] + (s[y1] - s[y0]) / 2
    ys = sorted(y for y in s if y0 <= y <= y1)
    for i in range(1, len(ys)):
        p, c = ys[i - 1], ys[i]
        hit = (s[p] > target >= s[c]) if falling else (s[p] < target <= s[c])
        if hit:
            return p + (target - s[p]) / (s[c] - s[p]), target
    raise SystemExit("::error::no crossing in %s -- the series changed shape" % s)


def main():
    if not TSV.exists():
        print("::error::%s is missing" % TSV.relative_to(ROOT))
        return 1
    d = load()
    fail = []

    print("  South Korea -- the year half the 1960-2020 change had happened")
    years = {}
    for key, label, falling in SERIES:
        s = d[key]
        yr, tgt = halfway(s, falling)
        years[key] = yr
        print("    %-18s %9.2f -> %9.2f   half %9.2f   reached %.1f"
              % (label, s[1960], s[2020], tgt, yr))

    order = [k for k, _, _ in SERIES]
    got = sorted(order, key=lambda k: years[k])
    span = years[order[-1]] - years[order[0]]
    print("    order: %s" % " -> ".join(
        dict((k, l) for k, l, _ in SERIES)[k] for k in got))
    print("    span : %.1f years" % span)
    if got != order:
        fail.append("the four series no longer fall in the order the chapter argues: %s" % got)

    # Ha-Joon Chang, F&D, September 2026: life expectancy was 53 when he was
    # born in 1963. The series puts 53.8 at 1960 and 55.0 at 1963.
    le = d["life_expectancy"]
    print("  Chang's '53' against the series: 1960 %.2f, 1963 %.2f" % (le[1960], le[1963]))
    if not 53.0 <= le[1960] < 54.0:
        fail.append("the 1960 value no longer rounds to the 53 the chapter discusses")
    if le[1963] < 54.5:
        fail.append("1963 no longer differs from 53 as the chapter says")

    # Gapminder Misconception Study 2017: twelve three-option questions.
    p = (2 / 3) ** 12
    print("  (2/3)^12 = %.6f  -> all twelve wrong by chance = %.2f%%" % (p, p * 100))
    print("  the observed 15%% is %.1f times that rate" % (0.15 / p))
    print("  mean score 2.2/12 = %.1f%%, against a random 33.3%%" % (2.2 / 12 * 100))

    if not PAGE.exists():
        fail.append("%s is missing" % PAGE.relative_to(ROOT))
    else:
        flat = " ".join(re.sub(r"<[^>]+>", " ",
                 re.sub(r"<script.*?</script>|<style.*?</style>", " ",
                        PAGE.read_text(encoding="utf-8"), flags=re.S)).split())
        must = ["1970.8", "1975.0", "1984.7", "1999.5", "28.7",
                "19.5", "18.3", "33.3", "53.8", "55.0"]
        missing = [m for m in must if m not in flat]
        if missing:
            fail.append("the page no longer prints: %s" % missing)
        print("  page checked for %d printed figures; missing %d" % (len(must), len(missing)))

    for f in fail:
        print("::error::" + f)
    if fail:
        return 1
    print("every figure in chapter 7 recomputed from the series, and the page prints them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
