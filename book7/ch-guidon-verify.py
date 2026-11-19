#!/usr/bin/env python3
"""ch-guidon-verify.py -- Book 7, Niède Guidon: the arithmetic and the graph behind the chapter.

What this checks.  Every number below is copied from a source named in the chapter; the script tests that the
arithmetic done ON those numbers on the page is right.  It does not test the archaeology, the dating methods or any
claim about who was first anywhere.  Standard library only.

  1  life dates: born 1933-03-12, died 2025-06-04, age 92 on the day she died; park 1979 < FUMDHAM 1986 < UNESCO 1991
  2  White Sands (New Mexico) age intervals, in thousands of years, read as plain intervals:
       seeds 2021: 21-23; pollen 2023: 23.4 +/- 2.5 and 22.6 +/- 2.3; OSL 2023: a MINIMUM of 21.5 +/- 1.9 (lower end
       only); lake mud 2025: 20.7-22.4.  Their common overlap is [21.0, 22.4].  This is interval overlap, not a
       statistical combination.
  3  Toca da Tira Peia (not Pedra Furada): layers from about 4 to 22 thousand years; 113 artifacts, 15 reported
       human-altered in the bottom two layers
  4  scale: 22 thousand years against the 1.8 million years of the Dmanisi remains, and against 2.12 million (Shangchen)
  5  where the sources disagree with each other, as numbers: orangutan split 19.3-15.7 Ma vs about 12 Ma;
       Sumatra/Bornean split 4.9-2.9 Ma vs about 0.4 Ma vs 3.4 Ma
  6  the connection graph: only edges the sources state; components with and without the dispute edges
  controls (the test must be able to fail):
  7  a corrupted birth year breaks check 1; adding the critics' 15-17 thousand-year interval empties check 2's overlap;
       removing the mentor edges changes check 6
  9  Norse contact (Wikipedia, L'Anse aux Meadows): 1021 lies inside the earlier radiocarbon range 990-1050 and is 28
       years after the 993 spike; 1492 is 471 years later; 1100 is outside the range (control)
  8  after contact (Columbian exchange page, Wikipedia): the declines it states, as percentages, sit inside the 80-95%
       it gives; a 50% decline would not (control)

Not checked: dating methods; whether the Pedra Furada stones are tools; whether the Germany molar belongs to the
orangutan lineage (the sources do not place it there); anything about the sources' accuracy.
Run:  python3 ch-guidon-verify.py
"""
from datetime import date
import sys

fails = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("  -- " + detail) if detail else ""))
    if not ok:
        fails.append(name)


def age_on(born, day):
    return day.year - born.year - ((day.month, day.day) < (born.month, born.day))


# 1  life dates (Pesquisa FAPESP obituary; Wikipedia agrees on both dates)
born, died = date(1933, 3, 12), date(2025, 6, 4)
check("1a age on 4 June 2025 is 92", age_on(born, died) == 92, f"{age_on(born, died)}")
check("1b park 1979 < FUMDHAM 1986 < UNESCO listing 1991", 1979 < 1986 < 1991)
check("1c first Piauí mission 1973 precedes her doctorate (1975, FAPESP) and the park (1979)", 1973 < 1975 < 1979)
check("1d control: a corrupted birth year (1934) breaks 1a", age_on(date(1934, 3, 12), died) != 92)

# 2  White Sands intervals (thousand years); None = unbounded above
seeds = (21.0, 23.0)
pollen1 = (23.4 - 2.5, 23.4 + 2.5)
pollen2 = (22.6 - 2.3, 22.6 + 2.3)
osl_min = (21.5 - 1.9, None)
mud = (20.7, 22.4)


def overlap(ivs):
    lo = max(i[0] for i in ivs)
    his = [i[1] for i in ivs if i[1] is not None]
    hi = min(his)
    return (lo, hi) if lo <= hi else None


ov = overlap([seeds, pollen1, pollen2, osl_min, mud])
check("2a the five reported intervals share a common overlap", ov is not None)
check("2b that overlap is [21.0, 22.4] thousand years", ov is not None and abs(ov[0] - 21.0) < 1e-9 and abs(ov[1] - 22.4) < 1e-9, str(ov))
check("2c pollen intervals as computed: [20.9, 25.9] and [20.3, 24.9]; OSL lower end 19.6",
      abs(pollen1[0] - 20.9) < 1e-9 and abs(pollen1[1] - 25.9) < 1e-9 and abs(pollen2[0] - 20.3) < 1e-9
      and abs(pollen2[1] - 24.9) < 1e-9 and abs(osl_min[0] - 19.6) < 1e-9)
check("2d control: adding the critics' 15-17 interval empties the overlap", overlap([seeds, pollen1, pollen2, osl_min, mud, (15.0, 17.0)]) is None)

# 3  Toca da Tira Peia (Lahaye et al. 2013, via Science News)
check("3a 15 human-altered stones are fewer than the 113 artifacts, and 15/113 is about 13%", 15 < 113 and round(15 / 113 * 100) == 13, f"{15 / 113 * 100:.1f}%")
check("3b the layer span is 22 - 4 = 18 thousand years", 22 - 4 == 18)

# 4  scale
dmanisi, shangchen, ka = 1_800_000, 2_120_000, 22_000
check("4a 22 thousand years is 1.2% of the 1.8 million years since Dmanisi", abs(ka / dmanisi * 100 - 1.22) < 0.01, f"{ka / dmanisi * 100:.2f}%")
check("4b it is 1.0% of the 2.12 million years at Shangchen (hedged by its source)", abs(ka / shangchen * 100 - 1.04) < 0.01, f"{ka / shangchen * 100:.2f}%")

# 5  source disagreements, as numbers (million years)
split_a, split_b = (15.7, 19.3), 12.0
check("5a the two orangutan-split figures do not overlap: 12 lies 3.7 below 15.7", not (split_a[0] <= split_b <= split_a[1]) and abs((split_a[0] - split_b) - 3.7) < 1e-9)
sb = [(2.9, 4.9), (0.4, 0.4), (3.4, 3.4)]
check("5b the three Sumatra/Bornean split estimates have no common value", overlap(sb) is None)
check("5c Europe's apes: 16 to 7 million years is a span of 9 million years", 16 - 7 == 9)

# 6  the connection graph: nodes are people the sources name; edges only where a source states them
collab_groups = {
    "Toca 2013 authors (Wikipedia reference list)": ["Guidon", "Lahaye", "Hernandez", "Boeda", "Felice", "Hoeltz", "Lourdeau", "Pagli", "Rasse", "Viana"],
    "1994 Antiquity paper": ["Meltzer", "Adovasio", "Dillehay"],
}
pairs = [("Guidon", "Delibrias"), ("Leroi-Gourhan", "Guidon"), ("Laming-Emperaire", "Guidon")]
pairs += [("Guidon", x) for x in ("Pessis", "Parenti", "Guerin", "Peyre", "dos Santos")]  # 2002 interview
dispute = [("Dillehay", "Guidon"), ("Adovasio", "Guidon"), ("Meltzer", "Guidon"), ("Fiedel", "Guidon"), ("Haynes", "Guidon"), ("Waters", "Guidon")]
loners = ["Pelegrin"]  # said to find a natural origin 'very unlikely'; no collaboration edge stated


def components(nodes, edges):
    parent = {n: n for n in nodes}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in edges:
        parent[find(a)] = find(b)
    return len({find(n) for n in nodes})


def build(with_mentors=True, with_dispute=False):
    edges = []
    for g in collab_groups.values():
        edges += [(a, b) for i, a in enumerate(g) for b in g[i + 1:]]
    ps = pairs if with_mentors else [p for p in pairs if p[0] not in ("Leroi-Gourhan", "Laming-Emperaire")]
    edges += ps
    if with_dispute:
        edges += dispute
    nodes = set(loners) | {n for e in edges for n in e} | {x for g in collab_groups.values() for x in g}
    nodes |= {"Fiedel", "Haynes", "Waters"}
    if not with_mentors:
        nodes |= {"Leroi-Gourhan", "Laming-Emperaire"}
    return nodes, edges


n0, e0 = build()
n1, e1 = build(with_dispute=True)
c0, c1 = components(n0, e0), components(n1, e1)
check("6a collaboration edges only: 6 components (Guidon's cluster, the 1994 trio, Fiedel, Haynes, Waters, Pelegrin)", c0 == 6, f"{len(n0)} people, {c0} components")
check("6b adding the six dispute edges joins all but Pelegrin: 2 components", c1 == 2, f"{c1} components")
n2, e2 = build(with_mentors=False)
check("7  control: dropping the two mentor edges changes the count (they are doing work)", components(n2, e2) != c0, f"{components(n2, e2)} vs {c0}")

# 8  declines stated on the Columbian exchange page (Wikipedia), recomputed from its own numbers
mexico = (1 - 1.0 / 20.0) * 100          # 'about 20 million' to 'barely more than a million'
peru = (1 - 0.6 / 9.0) * 100             # 'about 9 million' to 600,000 by 1620
check("8a Mexico: 20 million to about 1 million is about 95%; Peru: 9 million to 0.6 million is about 93%",
      abs(mexico - 95.0) < 0.5 and abs(peru - 93.3) < 0.1, f"{mexico:.1f}% and {peru:.1f}%")
check("8b both lie inside the 80-95% range the page gives", 80 <= peru <= 95 and 80 <= mexico <= 95)
check("8c control: a 50% decline is outside that range", not (80 <= 50 <= 95))

# 9  Norse contact at L'Anse aux Meadows, figures as Wikipedia states them
lo, hi, mean, tree = 990, 1050, 1014, 1021
check("9a 1021 and the older mean 1014 both lie inside the earlier radiocarbon range 990-1050", lo <= tree <= hi and lo <= mean <= hi)
check("9b 1021 is 28 years after the 993 carbon-14 spike and 471 years before 1492", tree - 993 == 28 and 1492 - tree == 471)
check("9c control: a date of 1100 falls outside that range", not (lo <= 1100 <= hi))

print()
print("Edges are only those the chapter's sources state; a missing edge means 'not stated here', not 'none exists'.")
if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("All checks passed. They test the arithmetic on the sources' numbers; they do not test the archaeology.")
