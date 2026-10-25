#!/usr/bin/env python3
"""Body-vs-note consistency guards for ch4-neural, ch5-immune, ch2-allostatic, chLambda-polylaminin (stdlib)."""
import re,sys,math
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
T=lambda f:re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',open(f,encoding='utf-8').read()))
# arithmetic behind the notes
ck('40 Hz for 45 min = 108000 cycles; one cycle 25 ms',40*45*60==108000 and abs(1/40-0.025)<1e-12)
ck('Hopf r-dot = lam r - r^3: cycle r=sqrt(lam), derivative -2lam',all(abs((l-3*(math.sqrt(l))**2)+2*l)<1e-12 for l in (0.1,1,4)))
ck('48 h / (6..12 h) doublings -> 2^4..2^8 = 16..256',(2**(48//12),2**(48//6))==(16,256))
ck('V=(r-1)^2: r=3/2 outside radius 1/3? |r-1|=.5>1/3 yet V=.25<1/3, and V>1/9',abs(.5)>1/3 and (.5**2)<1/3 and (.5**2)>1/9)
t=T('ch4-neural.html')
for g in ['phase-locked (coherent','Proposition 4.1 (conjectural)','does not establish the bound','not on frequency','On one proposed picture']: ck('ch4 present: '+g,g in t)
ck('ch4 absent: suddenly fire in phase.','suddenly fire in phase.' not in t)
t=T('ch5-immune.html')
for g in ['16–256 cells','that is withdrawn','spleen and lymphoid tissue','Proposition 5.1 (model)','an assumption of the bistable model','a gradient with a high barrier']: ck('ch5 present: '+g,g in t)
for g in ['one cell becomes thousands in 48 hours','It is called fever','confirming that K is a genuine threshold']: ck('ch5 absent: '+g,g not in t)
t=T('ch2-allostatic.html')
for g in ['not of r itself','V &gt; 1/9','K operator is read as firing']: ck('ch2a present: '+g,g in t)
ck('ch2a absent: λ is the radial coordinate r','λ is the radial coordinate r' not in t)
t=T('chLambda-polylaminin.html')
for g in ['ILLUSTRATIVE MOCK-UP — not a real run','is read here as following C','It did not produce the clinical results']: ck('chL present: '+g,g in t)
for g in ['follows C → K → F → U exactly','strongest empirical anchor yet']: ck('chL absent: '+g,g not in t)
sys.exit(1 if bad else 0)
