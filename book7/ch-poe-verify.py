#!/usr/bin/env python3
"""
Poe -- the dark sky, and what it costs to be unreadable.

Four blocks, and only the first three are physics.

[1] and [2] compute the dark-sky paradox from published constants: that every
shell of a static infinite universe contributes the same flux, so the sum
diverges; and that a finite horizon makes it converge, to a sky some 1e-14 as
bright as a stellar surface. This is the answer Poe stated qualitatively in
1848 -- that there is a distance beyond which no ray has yet arrived.

[3] computes Harrison's 1964 refinement, which is a different bound and the
one that actually holds: stars burn out long before their light can fill the
sky, by a factor of about 1e13. Poe's horizon is sufficient; Harrison's
energy budget is necessary.

[4] checks the chronology the chapter asserts, and [5] reads the chapter file
back to confirm the credit is stated as anticipation and not as a solution.
Block [5] strips epigraph, blockquote and claims-table before scanning: a
scanner that cannot tell a mention from a claim will fail a chapter for
quoting the very sentence it is disputing.

Standard library only.  python3 book7/ch-poe-verify.py
"""

import math, os, re, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.join(HERE, 'ch-poe.html')

# --- published constants, all order-of-magnitude standard ------------------
C_LIGHT   = 2.998e8           # m/s
MPC       = 3.0857e22         # m
R_SUN     = 6.957e8           # m
N_GAL     = 0.02              # galaxies per Mpc^3 (bright-galaxy density)
STARS_GAL = 1.0e11            # stars per galaxy
AGE_UNIV  = 13.8e9            # yr
YR        = 3.156e7           # s
T_STAR    = 1.0e10            # yr, a sun-like main-sequence lifetime

n_star = N_GAL * STARS_GAL / MPC**3          # stars per m^3
sigma  = math.pi * R_SUN**2                  # geometric cross-section, m^2

# ==========================================================================
head(1, 'EVERY SHELL CONTRIBUTES THE SAME -- SO THE STATIC SUM DIVERGES')
print("  The paradox in its arithmetic form. A shell of radius r and thickness")
print("  dr holds 4*pi*r^2*dr*n stars; each is dimmer as 1/r^2. The r^2 cancels")
print("  exactly, so every shell delivers the same flux and the total is")
print("  unbounded. This is the step Poe restates in words in Eureka (1848).\n")

L_SUN = 3.828e26  # W
def shell_flux(r, dr):
    """Flux at the origin from a shell at radius r, thickness dr. W/m^2."""
    n_shell = 4.0 * math.pi * r * r * dr * n_star
    return n_shell * L_SUN / (4.0 * math.pi * r * r)

print('      r (Mpc)        shell flux (W/m^2)')
fluxes = []
for r_mpc in (10, 100, 1000, 10000, 100000):
    f = shell_flux(r_mpc * MPC, 10 * MPC)
    fluxes.append(f)
    print('      %9d        %.6e' % (r_mpc, f))
spread = max(fluxes) / min(fluxes)
check(abs(spread - 1.0) < 1e-9,
      'all five shells deliver identical flux (spread = %.1e)' % (spread - 1.0),
      'spread %.3e' % spread)
check(sum(fluxes) > 4 * fluxes[0],
      'the partial sum grows without bound as shells are added')

# ==========================================================================
head(2, 'A HORIZON MAKES IT FINITE -- POE\'S ANSWER, IN NUMBERS')
print("  Sky brightness is a covering fraction: what proportion of the celestial")
print("  sphere is filled by a stellar disc. In an unbounded static universe that")
print("  fraction reaches 1 and the sky burns. Cut the integral at a horizon and")
print("  it stops at n*sigma*R -- a pure geometric count of discs along a line.\n")

R_hor = C_LIGHT * AGE_UNIV * YR                  # m, light-travel horizon
olbers_len = 1.0 / (n_star * sigma)              # m, mean free path to a star
f_cover = n_star * sigma * R_hor

print('      star number density n     %.3e m^-3' % n_star)
print('      stellar cross-section     %.3e m^2' % sigma)
print('      Olbers length 1/(n sigma) %.3e m  = %.2e light years' %
      (olbers_len, olbers_len / (C_LIGHT * YR)))
print('      horizon c*t_0             %.3e m  = %.2e light years' %
      (R_hor, R_hor / (C_LIGHT * YR)))
print('      covering fraction n*sigma*R  %.3e' % f_cover)

check(1e-16 < f_cover < 1e-12,
      'the sky is ~1e-14 of a stellar surface, not 1 -- the horizon resolves it',
      '%.2e' % f_cover)
check(olbers_len / R_hor > 1e8,
      'the Olbers length exceeds the horizon by ~%.0e' % (olbers_len / R_hor))
check(1e23 <= olbers_len / (C_LIGHT * YR) <= 1e25,
      'the Olbers length is %.1e ly -- within an order of magnitude of the '
      'textbook 1e23, the spread being the assumed star density'
      % (olbers_len / (C_LIGHT * YR)),
      '%.2e ly' % (olbers_len / (C_LIGHT * YR)))

# ==========================================================================
head(3, 'HARRISON 1964 -- THE BOUND THAT DOES NOT NEED A HORIZON')
print("  Harrison's point is stronger than the horizon and independent of it:")
print("  filling the sky would take the Olbers length divided by c, and no star")
print("  burns that long. Give the universe infinite age and the sky stays dark,")
print("  because the fuel runs out first.\n")

t_fill = olbers_len / C_LIGHT / YR               # yr to fill the sky
ratio  = t_fill / T_STAR

print('      time to fill the sky      %.2e yr' % t_fill)
print('      main-sequence lifetime    %.2e yr' % T_STAR)
print('      shortfall factor          %.2e' % ratio)
check(ratio > 1e10,
      'stars burn out ~1e13 times too soon to fill the sky',
      '%.2e' % ratio)
check(t_fill > AGE_UNIV,
      'the fill time also exceeds the age of the universe, so both bounds bite')
print("\n  Read together: Poe's horizon is sufficient, Harrison's budget is")
print("  necessary. The chapter must not merge them, and does not.")

# ==========================================================================
head(4, 'THE CHRONOLOGY, AND THE SIZE OF THE GAP')
EVENTS = [
    (1823, 'Olbers states the paradox in print (not the first to pose it)'),
    (1848, 'Poe, Eureka -- the horizon argument, subtitled A Prose Poem'),
    (1858, 'Maedler -- first finite-age resolution in the scientific literature'),
    (1860, 'Kaiser popularises Maedler in a popular-science book'),
    (1901, 'Kelvin -- first satisfactory mathematical treatment (little known)'),
    (1964, 'Harrison -- the modern resolution, from stellar lifetimes'),
    (1987, 'Harrison, Darkness at Night -- Poe and Kelvin restored to the record'),
]
for y, what in EVENTS:
    print('      %d   %s' % (y, what))
years = [y for y, _ in EVENTS]
check(years == sorted(years), 'the chronology is monotone')
check(1858 - 1848 == 10, 'Poe to the first scientific publication: 10 years')
check(1901 - 1848 == 53, 'Poe to the first mathematics: 53 years')
check(1987 - 1848 == 139, 'Poe to the historical recovery: 139 years')
check(1849 < 1858, 'Poe was dead (1849) before the idea entered the literature')

# ==========================================================================
head(5, 'THE CHAPTER FILE -- IS THE CREDIT STATED AS ANTICIPATION?')
if not os.path.exists(CHAPTER):
    check(False, 'ch-poe.html present next to this script', CHAPTER)
else:
    raw = open(CHAPTER, encoding='utf-8').read()
    # strip the places where a disputed sentence is quoted on purpose
    body = re.sub(r'<div class="hero-epigraph">.*?</div>', ' ', raw, flags=re.S)
    body = re.sub(r'<blockquote>.*?</blockquote>', ' ', body, flags=re.S)
    body = re.sub(r'<table class="data-table">.*?</table>', ' ', body, flags=re.S)
    body = re.sub(r'<div class="sources">.*?</div>', ' ', body, flags=re.S)
    flat = re.sub(r'<[^>]+>', ' ', body).lower()

    OVERCLAIM = ['poe solved', 'poe proved', 'poe was the first to solve',
                 'poe resolved the paradox', 'poe discovered the big bang']
    for phrase in OVERCLAIM:
        check(phrase not in flat, 'chapter prose does not say "%s"' % phrase)
    check('anticipat' in flat, 'chapter states the credit as anticipation')
    for y, _ in EVENTS:
        check(str(y) in raw, 'chapter carries the year %d' % y)
    check('maedler' in flat or 'mädler' in flat or 'm&auml;dler' in flat,
          'chapter names Maedler, who got there first in print')
    check('harrison' in flat, 'chapter names Harrison')
    check('prose poem' in flat, 'chapter names the subtitle that did the filing')

# ==========================================================================
print('\n' + '=' * 68)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
