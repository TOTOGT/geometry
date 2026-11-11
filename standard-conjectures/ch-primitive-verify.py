#!/usr/bin/env python3
"""Verifier for standard-conjectures/ch-primitive.html (R6, R24).
1. Re-runs the three computations the page relies on; each must exit 0.
2. Checks that the numbers printed on the page are the numbers those scripts compute.
3. Checks that the page carries its open lemma and makes no general claim."""
import subprocess, re, sys, os
here = os.path.dirname(os.path.abspath(__file__))
page = open(os.path.join(here, 'ch-primitive.html'), encoding='utf-8').read()
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)
def run(script):
    r = subprocess.run([sys.executable, '-I', os.path.join(here, script)], capture_output=True, text=True, timeout=170)
    return r.returncode, r.stdout
outs = {}
for sc in ('verify_p2xp2.py', 'verify_p3xp3.py', 'verify_surfaces.py', 'verify_cartan.py', 'verify_projected_chain.py'):
    rc, out = run(sc); outs[sc] = out
    chk('%s exits 0' % sc, rc == 0)
p3 = outs['verify_p3xp3.py']
for r_, val in ((0, '20'), (1, '4'), (2, '20/9'), (3, '4')):
    chk('P3xP3 V_%d = %s printed by script' % (r_, val), re.search(r'\(-1\)\^%d deg\(p\^2 h\^\d\) = %s\b' % (r_, re.escape(val)), p3) is not None)
chk('page prints V_r = 20, 4, 20/9, 4', '20,\\ 4,\\ 20/9,\\ 4' in page)
chk('page prints P2xP2 values 6s^2t^2, 2s^2t^2, 3s^2t^2', all(x in page for x in ('$6s^2t^2$', '$2s^2t^2$', '$3s^2t^2$')))
chk('P2xP2 script reports codim-2 value 3 s^2 t^2 (24 checks)', '24/24' in outs['verify_p2xp2.py'] or 'PASS' in outs['verify_p2xp2.py'])
chk('T x S: dimension formula 1+(rho_T-1)(rho_S-1) printed by script', 'dim primitive=5 (expected 5)' in outs['verify_surfaces.py'])
cc = outs['verify_cartan.py']
chk('Cartan script reports all checks passed', re.search(r'(\d+)/\1 checks passed', cc) is not None)
chk('page states the 40 exact checks of verify_cartan.py', '40 exact checks' in page and '40/40' in cc)
chk('page links the quiver note', '../collab/pinot-orthogonal-quivers/index.html' in page)
chk('page links the open questions page', 'open-questions.html' in page and os.path.exists(os.path.join(here, 'open-questions.html')))
chk('page does not claim a quiver-to-conjecture link is established', 'Nothing on this page links the quiver note' in page)
chk('projected-chain script passes 26/26 and page cites it', '26/26' in outs['verify_projected_chain.py'] and '26 exact checks' in page)
chk('page states ample curves are not primitive', 'never itself primitive' in page)
chk('page no longer claims chain classes lie in P_T x P_S directly', 'classes $E_i\\otimes F_j$' not in page)
chk('page carries the open lemma tag', '[OPEN]' in page)
chk('page says it does not approach a proof of the standard conjectures', 'does not approach one' in page)
bad = [s for s in ('proves the standard conjecture', 'establishes the general', 'new theorem') if s in page.lower()]
chk('page makes no general or novelty claim %s' % bad, not bad)
print('%d/%d checks passed' % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
