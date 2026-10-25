#!/usr/bin/env python3
"""ch3-circadian audit (stdlib). Exit 0 = pass."""
import math,re,sys
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
# autonomous system x' = f(x): period S. rescale rates by c: y(t)=x(c t) has period S/c
S=24.2
for c in (0.5,2,3):
    # y(t)=sin(2*pi*c*t/S) has period S/c
    ok=all(abs(math.sin(2*math.pi*c*(t+S/c)/S)-math.sin(2*math.pi*c*t/S))<1e-9 for t in (0,1.3,7.7))
    ck(f'uniform x{c} rescaling: period {S}->{S/c:.2f}',ok)
ck('doubling all rates halves period',abs(S/2-12.1)<1e-12)
# Reeb field of c*alpha is R/c in Darboux alpha=dz+q dp: alpha(R)=1 -> (c alpha)(R/c)=1
c=3.0; ck('Reeb of c*alpha is R/c (c*alpha)(R/c)=1',abs(c*1.0*(1/c)-1)<1e-12)
# Exercise 3.3: z(t) = -(w t/2 + sin(2 w t)/4); drop per lap = pi
w=2*math.pi/S; z=lambda t:-(w*t/2+math.sin(2*w*t)/4)
ck('Legendrian z drops by pi per lap',abs((z(0)-z(S))-math.pi)<1e-9)
# Legendrian: dz + q dp = 0 along q=cos wt,p=sin wt: z' = -q p' = -w cos^2
dz=lambda t:(z(t+1e-6)-z(t-1e-6))/2e-6
ck('z\' = -q p\'',all(abs(dz(t)+math.cos(w*t)*w*math.cos(w*t))<1e-5 for t in (0,3,9)))
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',open('ch3-circadian.html',encoding='utf-8').read()))
for g in ['Withdrawn as stated (audit 2026-10-25','Former prediction — withdrawn','Corrected, testable form','Show that symmetric rescaling changes T by the factor 1/λ','the model\'s assumption, not a derived fact']:
    ck('present: '+g,g in t)
ck('absent: while symmetric rescaling does not','while symmetric rescaling does not' not in t)
sys.exit(1 if bad else 0)
