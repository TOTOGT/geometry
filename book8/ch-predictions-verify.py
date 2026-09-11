#!/usr/bin/env python3
"""
Book 8 -- the falsifiable-prediction register, verified against the chapters.

WHY THIS EXISTS. On 11 September 2026 the register was audited by hand and was
wrong in four places at once: Chapter 1's figure title advertised F1-F6 over a
dashboard holding five cards; Chapter 1's meta description said six; Chapter 2
declared its three predictions as H1-H3 while the index counted them as F6-F8;
and Chapter 4 declared three predictions as F1-F3, which are Chapter 1's numbers
and different predictions. The headline number 26 was nevertheless correct --
which is the point. A count can be right while the thing it counts is
inconsistent, and nothing in the repository could tell the difference.

WHAT IT CHECKS. The index fixes the register: each chapter carries a declared
range, and the ranges must tile F1..F26 exactly once. Every number in a range
must then be declared in that chapter and nowhere else. Chapter-local namespaces
(Chapter 4's V-series) must not intrude on it. The headline numbers in the index,
Chapter 10 and Chapter 13 must agree with the register they describe.

Standard library only. Run from anywhere:  python3 book8/ch-predictions-verify.py
"""

import os, re, sys

HERE  = os.path.dirname(os.path.abspath(__file__))
rd    = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

# --------------------------------------------------------------------------
head(1, 'THE INDEX FIXES THE REGISTER')
print('  Each chapter card in index.html carries a declared range Fa-Fb.')
print('  The ranges must tile F1..F26, each number claimed exactly once.\n')

idx  = rd('index.html')
HREF = re.compile(r'href="(ch[^"]+\.html)"')
RNG  = re.compile(r'\bF(\d{1,2})(?:&ndash;|-|–)F(\d{1,2})\b')

owner, spans = {}, []
for m in RNG.finditer(idx):
    a, b = int(m.group(1)), int(m.group(2))
    if (a, b) == (1, 26):                 # the arc-level headline, not a chapter range
        continue
    before = [h for h in HREF.finditer(idx[:m.start()])]
    if not before:
        continue
    chap = before[-1].group(1)            # the card the range sits inside
    if (a, b, chap) in spans:             # the index prints some cards twice
        continue
    spans.append((a, b, chap))
    for n in range(a, b + 1):
        owner.setdefault(n, []).append((chap, a, b))

for a, b, chap in sorted(spans):
    print('    F%-2d-F%-3d  %s' % (a, b, chap))

dupes   = {n: v for n, v in owner.items() if len(v) > 1}
missing = [n for n in range(1, 27) if n not in owner]
strays  = [n for n in owner if not 1 <= n <= 26]
check(not dupes,   'no number is claimed by two chapters', str(dupes))
check(not missing, 'F1..F26 are all claimed',              str(missing))
check(not strays,  'no claimed number falls outside F1..F26', str(strays))
check(sum(b - a + 1 for a, b, _ in spans) == 26,
      'the ranges sum to exactly 26', str(sum(b - a + 1 for a, b, _ in spans)))

# --------------------------------------------------------------------------
head(2, 'EVERY REGISTERED PREDICTION IS DECLARED, ONCE, IN ITS OWN CHAPTER')
print('  Declaration form, house style:  <div class="box-label">Prediction &middot; Fn: ...')
print('  Chapter 1 is the exception: its five are cards in a dashboard array.\n')

DECL = re.compile(r'Prediction\s*(?:&middot;|·)\s*F(\d{1,2})\s*:')
CARD = re.compile(r"id:\s*'F(\d{1,2})'")

chapters = sorted({c for _, _, c in spans})
declared = {}
for chap in chapters:
    s = rd(chap)
    got = sorted({int(x) for x in DECL.findall(s)} | {int(x) for x in CARD.findall(s)})
    declared[chap] = got
    print('    %-26s declares %s' % (chap, ', '.join('F%d' % n for n in got) or '(none)'))

print()
for chap in chapters:
    want = sorted(n for n in owner if owner[n][0][0] == chap)
    check(declared[chap] == want, '%s declares exactly its own range' % chap,
          'declares %s, index says %s' % (declared[chap], want))

seen = {}
for chap, got in declared.items():
    for n in got: seen.setdefault(n, []).append(chap)
twice = {n: v for n, v in seen.items() if len(v) > 1}
check(not twice, 'no F-number is declared in two chapters', str(twice))
check(sorted(seen) == list(range(1, 27)), 'the declarations tile F1..F26',
      str(sorted(seen)))

# --------------------------------------------------------------------------
head(3, 'CHAPTER-LOCAL NAMESPACES DO NOT INTRUDE ON THE REGISTER')
print('  Chapter 4 states three further predictions. They are additional to the')
print('  register and carry a V prefix so that they cannot collide with it.\n')

ch4  = rd('ch4-field.html')
vloc = sorted({int(x) for x in re.findall(r'Prediction\s*(?:&middot;|·)\s*V(\d{1,2})\s*:', ch4)})
print('    ch4-field.html declares %s' % ', '.join('V%d' % n for n in vloc))
check(vloc == [1, 2, 3], 'ch4 declares V1, V2, V3', str(vloc))
check(not DECL.search(ch4), 'ch4 declares no F-number of its own',
      str(DECL.findall(ch4)))
check('ch4-field.html' not in chapters, 'ch4 is not assigned a register range by the index')

# Chapter 3 states none of its own; it points at Chapter 1's F3 and F4.
ch3 = rd('ch3-singularity.html')
check(not DECL.search(ch3), 'ch3 declares no prediction of its own',
      str(DECL.findall(ch3)))
check('Chapter 1' in ch3 and re.search(r'F3\s*/\s*F4', ch3) is not None,
      'ch3 names Chapter 1 when it cites F3 / F4')

# --------------------------------------------------------------------------
head(4, 'THE HEADLINE NUMBERS AGREE WITH THE REGISTER THEY DESCRIBE')
N = len(seen)
ch10, ch13 = rd('ch10-thermodynamics.html'), rd('ch13-holology.html')
check('Twenty-six falsifiable predictions (F1&ndash;F26)' in idx
      or 'Twenty-six falsifiable predictions (F1–F26)' in idx,
      'index says twenty-six, and names the range')
check('twenty-six falsifiable predictions' in ch10, 'ch10 says twenty-six')
check(len(re.findall(r'\b26 (?:registered )?predictions', ch13)) >= 1,
      'ch13 counts 26 predictions')
check(ch13.count('F1&ndash;F26') >= 2 or ch13.count('F1–F26') >= 2,
      'ch13 names the register rather than a bare count')
check(N == 26, 'the register actually holds 26', str(N))

# A count that is right about the wrong thing: the book states more falsifiable
# predictions than the register holds, and that difference should be stated.
total = N + len(vloc)
check('twenty-nine falsifiable predictions' in ch4,
      'ch4 records the true book-wide total (%d) beside the register (%d)' % (total, N))

# --------------------------------------------------------------------------
head(5, 'CONTROL: THIS SCRIPT TESTED SOMETHING')
check(len(spans) >= 8,  'at least 8 chapter ranges were read from the index', str(len(spans)))
check(N >= 26,          'at least 26 declarations were found in the chapters', str(N))
check(len(chapters) >= 8, 'at least 8 chapters were opened', str(len(chapters)))
print('    A vacuous pass is a pass. Block [5] exists so that blocks [1] and [2]')
print('    cannot report success by having quietly parsed nothing.')

# --------------------------------------------------------------------------
head('HONESTY', 'What this script establishes, and what it does not.')
print("""
  ESTABLISHED. That Book 8's falsifiable-prediction register is internally
  consistent: the index's chapter ranges tile F1..F26 without gap or overlap,
  every number in a range is declared in that chapter and in no other, the two
  chapter-local namespaces (Chapter 2's former H-series, now folded in; Chapter
  4's V-series, kept out) do not collide with it, and the headline counts in the
  index, Chapter 10 and Chapter 13 describe the register that actually exists.

  NOT ESTABLISHED. Anything whatsoever about whether a prediction is true, well
  posed, testable with the instrument named, or derived correctly from the
  framework. This script reads labels. F19's bound on the tensor-to-scalar ratio
  and F25's 9.7% shift in Hawking temperature are physics, and physics is settled
  by observation and not by a consistency check on a numbering scheme. The
  register being tidy is a precondition for those claims being checkable by
  someone else; it is not evidence for any of them.
""")

print('=' * 68)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 68); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
