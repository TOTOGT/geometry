#!/usr/bin/env python3
"""Verify Book XXVII (UoPeople MSIT study book), draft 2026-11-12.

Run from anywhere:  python3 b27-verify.py
Checks structure, links, that each chapter's unit headings match the official unit
lists read from the UoPeople course pages on 2026-11-12, that the computed worked
examples (chapters 1-3: critical path, PERT, earned value, risk; chapters 4-12: SQL, scheduling, paging, Dijkstra, regression and more) are recomputed here and match the
pages, and that the honesty markers are present. It does NOT check that the
theory statements are correct; that is a reading task, not a script task.
"""
import os, re, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b27_calc as C
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS  " if ok else "FAIL  ") + name + ("" if ok else "  " + detail))
    if not ok:
        fails += 1
def read(n):
    with open(os.path.join(HERE, n), encoding="utf-8") as f:
        return f.read()

FILES = {
    "index.html": None,
    "b27-ch01-organizational-theory-and-behavior.html": [
        "Introduction to Organizational Theory and Behavior",
        "Organizational Concepts and Theories",
        "Employee Motivation and Rewards",
        "Attitudes, Perceptions, and Behaviors",
        "Organizational Communication",
        "Collaborative Dynamics: Groups and Teams",
        "Leadership, Power, and Conflict",
        "Organizational Culture and Change"],
    "b27-ch02-business-law-ethics-csr.html": [
        "Introduction to Ethics in Business", "Ethics in Accounting",
        "Ethics and Environmental Concerns", "Ethics in Finance", "Ethics in the Law",
        "Ethics in Marketing", "Ethics in Management", "Ethics in Corporate Planning"],
    "b27-ch03-managing-projects-programs.html": [
        "Introduction to Project Management", "Initiation Phase",
        "Project Planning, Part 1", "Project Planning, Part 2", "Project Planning, Part 3",
        "Project Execution", "Control", "Closing and Project Success Factors"],
    "b27-ch04-databases.html": ["Database Systems Fundamentals", "Entity-Relationship Modelling", "Relational Data Modelling", "Structured Query Language", "Database Administration", "Transaction Management", "Database Security, Backup and Recovery", "Emerging Database Technologies"],
    "b27-ch05-operating-systems.html": ["Introduction to Operating Systems", "Understanding System Structures", "Fundamental Principles of Operating Systems", "Device Interaction and Management", "Resource Allocation Strategies", "Operating System Services", "Enhancing System Efficiency", "Modern Computing Environments"],
    "b27-ch06-algorithms.html": ["The Role of Algorithms in Computing", "Growth of Functions and Asymptotic Analysis of Algorithms", "Divide and Conquer", "Analysis of Sorting Algorithms", "Data Structures and Algorithms", "Hash Tables and their Applications", "Graphs and Algorithms", "String Matching Algorithms"],
    "b27-ch07-programming-languages.html": ["Programming Language Introduction", "Building the Programming Foundation", "Functions", "Variable, Objects, and Mutation", "Memory, Errors, and Design", "Control Structures and Type Systems", "Evaluation and Lazy Evaluation", "Preparation for the Final Project"],
    "b27-ch08-machine-learning.html": ["Introduction to Machine Learning", "Linear Regression", "Supervised Learning", "Unsupervised Learning", "Artificial Neural Networks", "Ensemble Learning", "Overview of Deep Learning and Gen AI", "Responsible and Explainable AI"],
    "b27-ch09-software-engineering.html": ["Introduction to Software Engineering Concepts", "Software Design and Architecture", "Emerging Industry Trends in Software Engineering", "Advanced Problem-Solving in Software Engineering", "Role-Specific Skills in Software Engineering", "Team Collaboration and Agile Practices", "Real-World Applications and Problem Solving", "Evaluating the Business Impact of Software Solutions"],
    "b27-ch10-hci.html": ["Introduction to HCI", "User Interface Design", "Smart Interfaces", "Virtual Worlds", "Brain Interfaces", "Input/Output", "Digital Assistants", "The Internet of Things (IoT)"],
    "b27-ch11-cybersecurity.html": ["Introduction to Cyber Security", "Ethical Hacking & Cyber Security methodologies", "Cyber Security Methodologies and setting up Lab for Cyber Security", "Website Pentesting & Security", "Mobile Pentesting & Wireless Security", "Dark web and Deep Web", "Cyber Forensics", "Bug Bounty Platforms & Reporting"],
    "b27-ch12-capstone.html": ["Project Proposal: Part 1", "Project Proposal: Part 2", "Project Implementation Plan: Part 1", "Project Implementation Plan: Part 2", "Project Implementation Plan: Part 3", "Project Implementation Plan: Part 4", "Final Project Due", "Capstone Report Submission"],
    "b27-ch00-math-for-msit.html": ["Logic and Proof", "Sets, Relations and Functions", "Counting and Combinatorics", "Probability and Bayes' Rule", "Sequences, Sums and Recurrences", "Graphs and Trees", "Linear Algebra", "Calculus for Learning"],
    "b27-ch00b-cryptography-math.html": ["Modular Arithmetic", "Primes, GCD and Euclid's Algorithm", "Fermat's and Euler's Theorems", "Fast Exponentiation", "Symmetric Ciphers and Why Keys Matter", "The Public-Key Idea and Diffie-Hellman", "RSA", "Hashes, Signatures and Limits"],
}

# ---- files, self-containment, links
for fn in FILES:
    check(f"{fn} exists", os.path.exists(os.path.join(HERE, fn)))
pages = {fn: read(fn) for fn in FILES if os.path.exists(os.path.join(HERE, fn))}
for fn, h in pages.items():
    check(f"{fn} has no external resources",
          not re.search(r'(src|href)="https?://', h) and "<script" not in h and "@import" not in h)
    check(f"{fn} has a title and a viewport", "<title>" in h and "viewport" in h)
    check(f"{fn} has no placeholder text", not re.search(r"lorem ipsum|TODO|FIXME", h, re.I))
    for href in re.findall(r'href="([^"#]+)"', h):
        if href.startswith(("http", "mailto")):
            continue
        if href.startswith("../") and not os.path.isdir(os.path.join(HERE, "..", "book24")):
            print(f"SKIP  {fn} link {href} (sibling book folder not present here; run from inside the geometry repo)")
            continue
        ok = os.path.exists(os.path.normpath(os.path.join(HERE, href)))
        check(f"{fn} link {href} resolves", ok)

# ---- unit headings match the official lists
def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s.replace("&middot;", "·").replace("&amp;", "&"))).strip()
for fn, units in FILES.items():
    if units is None or fn not in pages:
        continue
    heads = [clean(m) for m in re.findall(r"<h2>(.*?)</h2>", pages[fn])]
    found = [re.sub(r"^Unit \d+ · ", "", h) for h in heads if h.startswith("Unit ")]
    # chapter 3 titles for planning units carry a subtitle after a colon
    ok = len(found) == len(units) and all(f.startswith(u) for f, u in zip(found, units))
    check(f"{fn} unit headings match the official 8-unit list", ok, f"found {found}")
    check(f"{fn} has 8 self-check questions", pages[fn].count("<b>Self-check</b>") == 8)

# ---- computed worked examples
ACT = {"A": (3, []), "B": (2, ["A"]), "C": (4, ["A"]), "D": (3, ["B"]), "E": (2, ["C"]),
       "F": (4, ["D", "E"])}
es, ef = {}, {}
for a, (d, pre) in ACT.items():
    es[a] = max([ef[p] for p in pre], default=0); ef[a] = es[a] + d
T = max(ef.values()); lf, ls = {}, {}
for a in reversed(list(ACT)):
    succ = [b for b in ACT if a in ACT[b][1]]
    lf[a] = min([ls[b] for b in succ], default=T); ls[a] = lf[a] - ACT[a][0]
flt = {a: ls[a] - es[a] for a in ACT}
crit = [a for a in ACT if flt[a] == 0]
check("CPM: project duration is 13 days", T == 13)
check("CPM: critical path is A, C, E, F", crit == ["A", "C", "E", "F"])
check("CPM: float B = 1 and D = 1", flt["B"] == 1 and flt["D"] == 1)
ch3 = pages.get("b27-ch03-managing-projects-programs.html", "")
check("page states duration 13 and path A→C→E→F",
      "duration is 13 days" in ch3 and "A &rarr; C &rarr; E &rarr; F" in ch3)
for a in ACT:
    row = f"<tr><td>{a}</td><td>{ACT[a][0]}</td><td>{', '.join(ACT[a][1]) or '-'}</td><td>{es[a]}</td><td>{ef[a]}</td><td>{ls[a]}</td><td>{lf[a]}</td><td>{flt[a]}</td></tr>"
    check(f"page table row for activity {a} matches", row in ch3)

o, m_, p = 2, 5, 14
te = F(o + 4 * m_ + p, 6); sd = F(p - o, 6); var = sd ** 2
check("PERT: expected 6, sd 2, variance 4", (te, sd, var) == (6, 2, 4))
check("page states the PERT result", "expected duration is 6 days, the standard deviation 2 days and the variance 4 days squared" in ch3)

BAC, PV, EV, AC = 100000, 40000, 35000, 42000
CPI = F(EV, AC); SPI = F(EV, PV); EAC = F(BAC) / CPI
vals = dict(CV=EV - AC, SV=EV - PV, CPI=float(CPI), SPI=float(SPI), EAC=float(EAC),
            ETC=float(EAC - AC), VAC=float(BAC - EAC), TCPI=float(F(BAC - EV, BAC - AC)))
check("EVM: CV -7000, SV -5000", vals["CV"] == -7000 and vals["SV"] == -5000)
check("EVM: CPI 0.8333, SPI 0.875", abs(vals["CPI"] - 0.8333) < 1e-4 and vals["SPI"] == 0.875)
check("EVM: EAC 120000, ETC 78000, VAC -20000",
      round(vals["EAC"]) == 120000 and round(vals["ETC"]) == 78000 and round(vals["VAC"]) == -20000)
check("EVM: TCPI 1.1207", abs(vals["TCPI"] - 1.1207) < 1e-4)
check("page states the EVM results",
      "CV = -7,000" in ch3 and "SV = -5,000" in ch3 and "CPI = 0.8333" in ch3
      and "SPI = 0.875" in ch3 and "EAC = $120,000" in ch3 and "ETC = $78,000" in ch3
      and "VAC = -20,000" in ch3 and "1.1207" in ch3)
check("risk: 30% of $20,000 = $6,000", F(3, 10) * 20000 == 6000 and "expected value of $6,000" in ch3)

ch1 = pages.get("b27-ch01-organizational-theory-and-behavior.html", "")
check("expectancy example: 0.8 x 0.5 x 6 = 2.4", abs(0.8 * 0.5 * 6 - 2.4) < 1e-9 and "= 2.4" in ch1)

# ---- honesty markers
ch2 = pages.get("b27-ch02-business-law-ethics-csr.html", "")
idx = pages.get("index.html", "")
for name, h in (("ch1", ch1), ("ch2", ch2), ("ch3", ch3), ("index", idx)):
    check(f"{name} carries the reading-status statement (what it is not based on)", "not based on" in h)
check("ch1 flags the disagreement between two official pages", "two official pages disagree" in ch1 and 'class="tag">to confirm' in ch1)
check("ch2 says it is not legal advice", "not legal advice" in ch2)
check("ch2 says cases must be re-read in a primary source", "primary source" in ch2)
check("ch3 flags the guessed planning split as to confirm", "to confirm" in ch3 and "exact split" in ch3)
check("every chapter has the 'sourced' unit-list box", all('<span class="tag">sourced</span>' in h for h in (ch1, ch2, ch3)))
check("every chapter has the study-aid box with no-answers statement",
      all("does not contain answers to graded assignments" in h for h in (ch1, ch2, ch3)))
for code in ("5210", "5212", "5214", "5216", "5220", "5224", "5226", "5228", "5230", "5240", "5250", "5260", "5270", "5910", "5113", "5115", "5611"):
    check(f"index lists course {code}", code in idx)
check("index flags the capstone rule and the BUS 5611 prerequisite as to confirm", "B-" in idx and "prerequisite of BUS 5611" in idx and idx.count("to confirm") >= 2)


# ---- chapters 4-12: computed examples, checked against hand-known values and the pages
P = {n: pages.get(n, "") for n in FILES}
c4, c5, c6, c7, c8, c9, c10, c11, c12 = [P[f] for f in list(FILES)[4:13]]
# ch4: textbook-style facts, derived independently of b27_calc where short
check("db: closure of A is ABC and of AD is ABCDE", C.fd_closure("A", C.FDS) == "ABC" and C.fd_closure("AD", C.FDS) == "ABCDE")
check("db: only candidate key is AD", C.candidate_keys() == ["AD"])
check("db page states closure and key", "ABC" in c4 and "ABCDE" in c4 and "<b>AD</b>" in c4 or ("candidate key is AD" in c4))
d = C.sql_demo()
check("sql: group-by rows Sales 2 55000, Engineering 2 85000, Legal 0 NULL",
      d["group"] == [("Sales", 2, 55000.0), ("Engineering", 2, 85000.0), ("Legal", 0, None)])
check("sql: inner join drops Ed (4 rows); having gives Engineering", len(d["inner"]) == 4 and d["having"] == [("Engineering",)])
check("sql: rollback restores row count 5 -> 6 -> 5", d["atomic"] == (5, 6, 5))
check("page states the SQL results", "Sales, 2, 55000" in c4 and "Engineering, 2, 85000" in c4 and "Legal, 0, NULL" in c4 and "returns 4 rows" in c4 or "returns " + "4 rows" in c4)
e1, a1 = C.conflict_serializable(C.S1); e2, a2 = C.conflict_serializable(C.S2)
check("serializability: S1 acyclic with edge T1->T2 only; S2 has a cycle", e1 == [(1, 2)] and a1 and e2 == [(1, 2), (2, 1)] and not a2)
# ch5: textbook values
check("os: FCFS avg wait 23/4, SJF 21/4, RR(4) 37/4", (C.fcfs()[0], C.sjf()[0], C.rr(4)[0]) == (C.F(23, 4), C.F(21, 4), C.F(37, 4)))
check("os: page-replacement 3 frames FIFO 15, LRU 12, OPT 9 (textbook values)", (C.fifo_faults(C.REFS, 3), C.lru_faults(C.REFS, 3), C.opt_faults(C.REFS, 3)) == (15, 12, 9))
check("os: Belady anomaly 9 faults with 3 frames, 10 with 4", (C.fifo_faults([1,2,3,4,1,2,5,1,2,3,4,5], 3), C.fifo_faults([1,2,3,4,1,2,5,1,2,3,4,5], 4)) == (9, 10))
need, order, safe = C.banker()
check("os: banker safe sequence P1,P3,P4,P0,P2 (textbook)", safe and order == ["P1", "P3", "P4", "P0", "P2"])
check("os: address 20000 -> page 4 offset 3616; frame 9 gives 40480", C.translate(20000) == (4, 3616) and 9 * 4096 + 3616 == 40480)
check("page states the OS numbers", "average waiting time 5.75" in c5 and "5.25" in c5 and "9.25" in c5 and "15 faults" in c5 and "12" in c5 and "40480" in c5 and "P1, P3, P4, P0, P2" in c5)
# ch6
ms, cmp_ = C.merge_sort_comparisons(C.MS_INPUT)
check("algo: merge sort result sorted, 17 comparisons (= n log n - n + 1 for n=8)", ms == sorted(C.MS_INPUT) and cmp_ == 17)
check("algo: binary search finds 43 at index 6 in 3 probes", C.binary_search_steps(sorted(C.MS_INPUT), 43) == (6, 3))
check("algo: hash chains slot 1 = [50,85,92], longest 3", C.hash_chains(C.HASH_KEYS, 7)[1] == [50, 85, 92] and max(map(len, C.hash_chains(C.HASH_KEYS, 7))) == 3)
dist, prev = C.dijkstra(C.GRAPH, "S")
check("algo: Dijkstra T=10 via S,B,A,C,T", dist["T"] == 10 and dist["A"] == 5 and C.path_to(prev, "T") == ["S", "B", "A", "C", "T"])
check("algo: KMP table ABABC = [0,0,1,2,0]; matches at 2 and 7", C.kmp_table("ABABC") == [0, 0, 1, 2, 0] and C.kmp_search("ABABABCABABC", "ABABC") == [2, 7])
check("page states algorithm results", "makes 17 comparisons" in c6 and "[0, 0, 1, 2, 0]" in c6 and "2 and 7" in c6 and "length 10" in c6 and "S &rarr; B &rarr; A &rarr; C &rarr; T" in c6)
# ch7
t = C.parse(C.tokenize(C.EXPR))
check("lang: parse tree (+ 2 (* 3 (- 4 1))) evaluates to 11", C.show(t) == "(+ 2 (* 3 (- 4 1)))" and C.ev(t) == 11)
check("lang: closure counter [1,2,1,3]; evaluations value 1, name 2, need 1", C.counter_closure() == [1, 2, 1, 3] and C.eval_strategies()[0] == {"v": 1, "n": 2, "need": 1})
check("page states language results", "(+ 2 (* 3 (- 4 1)))" in c7 and "1, 2, 1, 3" in c7 and "call by name 2" in c7)
# ch8: independent checks
w, b0, r2 = C.linreg(C.ML_X, C.ML_Y)
check("ml: regression w=3/5, b=11/5, R^2=3/5", (w, b0, r2) == (C.F(3, 5), C.F(11, 5), C.F(3, 5)))
check("ml: confusion matrix acc 0.7, prec 0.8, recall 2/3, F1 8/11", C.clf_metrics(**C.CONF) == dict(acc=C.F(7, 10), prec=C.F(4, 5), rec=C.F(2, 3), f1=C.F(8, 11)))
check("ml: one gradient step from 0,0 at lr 0.01 gives w=0.264, b=0.08 (hand: gradients -26.4 and -8)", [round(float(v), 6) for v in C.gd_step(0, 0, C.ML_X, C.ML_Y, 0.01)] == [0.264, 0.08])
check("ml: k-means ends at centres 1.5 and 13", C.kmeans_1d(C.KM_PTS, [1, 2])[0] == [1.5, 13.0])
check("page states ML results", "w = 3/5 = 0.6" in c8 and "2.2" in c8 and "0.6" in c8 and "0.7273" in c8 and "w = 0.264" in c8 and "b = 0.08" in c8 and "1.5 and 13" in c8)
# ch9
check("se: cyclomatic complexity of the CFG is 3 (E=9, N=8)", len(C.CFG_EDGES) == 9 and C.CFG_NODES == 8 and C.cyclomatic(9, 8) == 3 and len({n for e in C.CFG_EDGES for n in e}) == 8)
check("se: COCOMO organic 10 KLOC = 26.9 PM, 8.7 months", round(C.cocomo_organic(10)[0], 1) == 26.9 and round(C.cocomo_organic(10)[1], 1) == 8.7)
check("page states SE results", "V = 9 - 8 + 2 = 3" in c9 and "26.9 person-months" in c9 and "8.7 months" in c9)
# ch10
check("hci: Fitts 0.517 s (W=20), 0.400... for W=40; Hick 0.45 s", abs(C.fitts(0.2, 0.1, 160, 20) - 0.5170) < 1e-4 and abs(C.fitts(0.2, 0.1, 160, 40) - (0.2 + 0.1 * math.log2(5))) < 1e-12 and abs(C.hick(0.15, 7) - 0.45) < 1e-9)
check("page states HCI results", "0.517 s" in c10 and "0.432 s" in c10 and "0.45 s" in c10)
# ch11
check("sec: SHA-256('abc') equals the standard test vector", C.sha256_hex("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
check("sec: risk 4x5 = 20, 2x3 = 6", C.risk_score(4, 5) == 20 and C.risk_score(2, 3) == 6)
dd = C.bit_diff(C.sha256_hex("password1"), C.sha256_hex("password2"))
check("page states security results", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" in c11 and f"differ in {dd} of 256 bits" in c11 and "scoring 6" in c11)
# ch12
check("capstone: weights 15+34+6+20+25 = 100; per-assignment 1.875 and 5.67", sum(C.CAP_WEIGHTS.values()) == 100 and 15 / 8 == 1.875 and f"{34 / 6:.2f}" == "5.67")
check("page states capstone arithmetic", "sum to 100" in c12 and "1.875" in c12 and "5.67" in c12 and "45 of 100" in c12)

# ---- flags and reading-status statements for chapters 4-12
for i, h in zip(range(4, 13), (c4, c5, c6, c7, c8, c9, c10, c11, c12)):
    check(f"ch{i} states what it is not based on", "not based on" in h)
    check(f"ch{i} has the sourced box and the study-aid box", '<span class="tag">sourced</span>' in h and "does not contain answers to graded assignments" in h)
    check(f"ch{i} has an open box with to confirm", 'class="box open"' in h and 'class="tag">to confirm' in h)
    check(f"ch{i} has at least one computed tag", 'class="tag">computed' in h or i in (10, 11, 12) and 'class="tag">computed' in h)
check("ch6 flags page-vs-syllabus unit disagreement", "two official sources disagree" in c6)
check("ch8 flags page-vs-syllabus unit disagreement", "disagree completely" in c8 and "PAC" in c8)
check("ch10 flags the Unit 1 label conflict", "Learning Guide labels Unit 1" in c10)
check("ch11 states authorization requirement and gives no attack steps", "written authorization" in c11 and "no working attack steps" in c11)
check("ch11 does not tag 5270 as identity verification", "Identity Verification" not in c11)
check("ch12 flags BUS 5612 vs 5611, 'all eight' vs seven, and the unit-number conflict", "5612" in c12 and "5611" in c12 and "all eight" in c12 and "Unit 6" in c12)
check("ch3 links forward to ch4 and ch4..12 chain forward", "b27-ch04-databases.html" in ch3 and all(f in P[g] for g, f in zip(list(FILES)[4:12], list(FILES)[5:13])))
check("index links every chapter 1-12 and no longer says planned", all(f in idx for f in list(FILES)[1:13]) and "planned" not in idx)

# ---- chapters 0 and 0b: pre-MSIT math, independent checks
c0 = pages.get("b27-ch00-math-for-msit.html", ""); c0b = pages.get("b27-ch00b-cryptography-math.html", "")
check("math: p->q false only at (T,F)", [t[2] for t in C.implies_table()] == [True, False, True, True])
check("math: C(10,3)=120, 5!=120, C(52,5)=2,598,960", (math.comb(10, 3), math.factorial(5), math.comb(52, 5)) == (120, 120, 2598960))
check("math: Bayes posterior 0.009/(0.009+0.0495) = 0.1538", abs(0.009 / (0.009 + 0.0495) - 0.15384615) < 1e-6 and abs(C.bayes(0.01, 0.9, 0.05) - 0.15384615) < 1e-6)
check("math: sum 1..100 = 5050; matmul and det", sum(range(1, 101)) == 5050 == 100 * 101 // 2 and C.matmul([[1, 2], [3, 4]], [[0, 1], [1, 0]]) == [[2, 1], [4, 3]] and C.det2([[1, 2], [3, 4]]) == -2)
check("math: gradient formula -26.4 matches numerical slope", C.mse_grad_w(0, 0, C.ML_X, C.ML_Y) == -26.4 and abs(C.numeric_grad_w(0, 0, C.ML_X, C.ML_Y) + 26.4) < 1e-4)
check("page states chapter 0 results", "= 120" in c0 and "2,598,960" in c0 and "0.1538" in c0 and "5050" in c0 and "[[2, 1], [4, 3]]" in c0 and "-26.4" in c0 and "-2" in c0 and "5 edges" not in c0 and "handshake" in c0)
# crypto: independent of b27_calc where the identity is textbook
g_, x_, y_ = C.ext_gcd(240, 46)
check("crypto: gcd(240,46)=2 and 240x+46y=2", g_ == 2 and 240 * x_ + 46 * y_ == 2 and math.gcd(240, 46) == 2)
check("crypto: 17*2753 = 15*3120 + 1, so 2753 is the inverse of 17 mod 3120", 17 * 2753 == 15 * 3120 + 1 and C.mod_inv(17, 3120) == 2753 == pow(17, -1, 3120))
check("crypto: phi(12)=4, phi(3233)=3120=60*52", C.phi(12) == 4 and C.phi(3233) == 3120 == 60 * 52 and 61 * 53 == 3233)
check("crypto: Fermat 2^10 mod 11 = 1; 7^222 mod 11 = 5", pow(2, 10, 11) == 1 and pow(7, 222, 11) == 5)
check("crypto: 65^17 mod 3233 = 2790 in 6 multiplications; 17 = 10001b", C.modexp_steps(65, 17, 3233) == (2790, 6) == (pow(65, 17, 3233), 6) and bin(17) == "0b10001")
check("crypto: RSA toy n=3233, lambda=3120, d=2753, c=2790, back to 65", C.rsa_toy() == (3233, 3120, 2753, 2790, 65))
check("crypto: DH p=23 g=5 gives 8 and 19 and shared secret 2", C.dh_toy() == (8, 19, 2, 2) and pow(5, 6, 23) == 8 and pow(5, 15, 23) == 19)
check("crypto: XOR pad round trip", C.xor_demo()[0] == C.xor_demo()[3] and C.xor_demo()[0] ^ C.xor_demo()[1] == C.xor_demo()[2])
check("crypto: birthday 23 -> 0.5073, 57 -> 0.9901", round(C.birthday(23), 4) == 0.5073 and round(C.birthday(57), 4) == 0.9901)
dd0 = C.bit_diff(C.sha256_hex("password1"), C.sha256_hex("password2"))
check("page states cryptography-math results", all(t in c0b for t in ["= 2, with 240", "2753", "3233", "2790", "= 65", "6 modular multiplications", "10001", "publishes 8", "Bob publishes 19", "0.5073", "0.9901", f"differ in {dd0} of 256"]))
for nm, h in (("ch0", c0), ("ch0b", c0b)):
    check(f"{nm} says it is not from a UoPeople course", "not</b> drawn from a UoPeople course page" in h or "not</b> part of any UoPeople course" in h)
    check(f"{nm} has the study-aid box and a computed tag and an open box", "does not contain answers to graded assignments" in h and 'class="tag">computed' in h and 'class="box open"' in h)
check("ch0b says toy numbers are not secure and gives no attack procedure", "not secure" in c0b and "no attack procedures" in c0b)
check("ch11 points to chapter 0b and says the units contain no cryptography", "contain no cryptography" in c11 and "b27-ch00b" not in c11 and "chapter 0b" in c11)
check("index lists Part 0 with both chapters and says they sit before every path", "b27-ch00-math-for-msit.html" in idx and "b27-ch00b-cryptography-math.html" in idx and "before every path" in idx)

# ---- cross-check of the worked examples in Hoffstein, Pipher, Silverman (2008) that chapter 0b cites
check("book Ex 1.6: gcd(2024, 748) = 44 by Euclid's steps", C.ext_gcd(2024, 748)[0] == 44 and 2024 == 748 * 2 + 528 and 748 == 528 + 220 and 528 == 220 * 2 + 88 and 220 == 88 * 2 + 44 and 88 == 44 * 2)
check("book Ex 1.26: 2^(p-1) = 1 mod 15485863", pow(2, 15485862, 15485863) == 1)
check("book Ex 1.28: inverse of 7814 mod 17449 is 1284, with (u,v) = (1284,-575)", C.mod_inv(7814, 17449) == 1284 and 7814 * 1284 + 17449 * (-575) == 1 and pow(7814, 17447, 17449) == 1284)
check("book Ex 2.7: p=941, g=627, a=347, b=781 gives 390, 691 and shared 470", (pow(627, 347, 941), pow(627, 781, 941), pow(691, 347, 941), pow(390, 781, 941)) == (390, 691, 470, 470))
NN = 1223 * 1987
check("book Ex 3.8: RSA N=2430101, (p-1)(q-1)=2426892, d=1051235, c=1473513, m=1070777",
      NN == 2430101 and 1222 * 1986 == 2426892 and math.gcd(948047, 2426892) == 1 and C.mod_inv(948047, 2426892) == 1051235
      and pow(1070777, 948047, NN) == 1473513 and pow(1473513, 1051235, NN) == 1070777)
check("ch0b cites the book and its ISBN, and states what was and was not read",
      "Hoffstein" in c0b and "978-0-387-77993-5" in c0b and "Example 3.8" in c0b and "Example 2.7" in c0b and "I did <b>not</b> work from its proofs" in c0b)
check("ch0b reading map shows the recomputed book values", all(t in c0b for t in ["= 44", "= 1284", "shared secret 470", "d = 1051235", "1473513"]))
check("ch0b no longer uses lambda for (p-1)(q-1) (matches the book's notation)", "&lambda;" not in c0b and "(p-1)(q-1) = 3120" in c0b)

# ---- voice: first person, to a classmate; no notes addressed to the author or to a model
ALLP = {n: pages.get(n, "") for n in FILES}
BANNED = ["you pasted", "pasted", "your catalog", "your pasted", "this session", "you asked", "you supplied", "I have not read", "I have <b>not read", "not read</b>", "Claude"]
for nm, h in ALLP.items():
    bad = [b for b in BANNED if b in h]
    check(f"{nm} has no notes-to-the-author wording", not bad, str(bad))
check("study-aid box speaks in the first person to a classmate", all("I'm writing these chapters" in ALLP[f] for f in ALLP if f != "index.html"))
check("index preface speaks in the first person", "I'm starting the program now" in ALLP["index.html"] and "can work from the same page" in ALLP["index.html"])

# ---- cross-references to other books of the Opus
XREF = {"b27-ch00-math-for-msit.html": ["../book24/index.html", "../book24/ch01-vectors-span-independence.html", "../book24/ch05-linear-maps.html", "../book24/ch06-matrices-determinants.html", "../book18/ch02-the-rule-itself.html", "../book18/ch08-several-variables.html", "../book18/ch07-sequences-and-series.html", "../book20/ch03-what-to-expect.html", "../book20/ch04-back-toward-the-mean.html", "../book14/ch01-the-grammar-of-notation.html"],
        "b27-ch00b-cryptography-math.html": ["../book24/index.html", "../book24/ch01-vectors-span-independence.html", "../book24/ch06-matrices-determinants.html"],
        "b27-ch07-programming-languages.html": ["../book14/ch01-the-grammar-of-notation.html", "../book14/ch02-how-mathematical-prose-parses.html", "../book19/ch03-elaborator-macro-kernel.html"],
        "b27-ch08-machine-learning.html": ["../book17/index.html", "../book16/index.html", "../book18/ch02-the-rule-itself.html", "../book18/ch08-several-variables.html", "../book24/ch06-matrices-determinants.html", "../book24/ch08-inner-products.html", "../book24/ch09-numerical.html", "../book20/ch03-what-to-expect.html", "../book20/ch04-back-toward-the-mean.html"],
        "index.html": ["../book24/index.html", "../book18/index.html", "../book20/index.html", "../book17/index.html", "../book16/index.html", "../book14/index.html"]}
for fn, links in XREF.items():
    check(f"{fn} links to {len(links)} other books of the Opus", all(f'href="{l}"' in ALLP[fn] for l in links) and "See also in the Opus" in ALLP[fn] or (fn == "index.html" and all(f'href="{l}"' in ALLP[fn] for l in links)))
check("ch0b links the linear-algebra prerequisite to Book XXIV right where the preface is mentioned", "first course in linear algebra" in ALLP["b27-ch00b-cryptography-math.html"] and "Book XXIV, Linear Algebra for Graduate Study" in ALLP["b27-ch00b-cryptography-math.html"])
check("ch0 unit 7 points to Book XXIV", "Book XXIV, Linear Algebra for Graduate Study" in ALLP["b27-ch00-math-for-msit.html"])
check("cross-reference boxes say the match was chosen by title and description", all("by chapter title and description" in ALLP[f] for f in XREF if f != "index.html") and "by title and description" in ALLP["index.html"])

# ---- paths through the book
paths = {m.group(1): [int(x) for x in re.findall(r"<li>(\d+)</li>", m.group(2))]
         for m in re.finditer(r'<ol class="path" data-path="(\w)">(.*?)</ol>', idx, re.S)}
check("index has paths A, B, C and D", sorted(paths) == ["A", "B", "C", "D"], str(sorted(paths)))
for k, p in sorted(paths.items()):
    check(f"path {k} lists chapters 1-12 exactly once", sorted(p) == list(range(1, 13)), str(p))
    check(f"path {k} ends with the Capstone (12)", p and p[-1] == 12)
    check(f"path {k} puts BUS 5113 (1) before BUS 5611 (3)", p and p.index(1) < p.index(3))
if "A" in paths:
    # catalog sample: BUS5113, 5210, 5212, 5214, 5216, BUS5115, 5226, 5250, BUS5611, 5260, 5270, 5910
    check("path A matches the catalog sample sequence", paths["A"] == [1, 4, 5, 6, 7, 2, 8, 9, 3, 10, 11, 12])
check("index says B, C, D are suggestions and A is the catalog's", "B, C and D are my suggestions" in idx)

print()
print("ALL PASS" if fails == 0 else f"{fails} FAILED")
sys.exit(1 if fails else 0)
