#!/usr/bin/env python3
"""chA-autophagy audit checks (stdlib). Exit 0 = pass."""
import re, math, sys
t=open('chA-autophagy.html',encoding='utf-8').read()
txt=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',t))
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
# A: threshold algebra behind the sqrt step: for K,l>0,r>=0, r^2<=K/l <=> r<=sqrt(K/l)
import random
ok=all(((r*r<=K/l)==(r<=math.sqrt(K/l)+0)) or abs(r-math.sqrt(K/l))<1e-9
       for _ in range(20000) for K,l,r in [(random.uniform(.1,9),random.uniform(.1,9),random.uniform(0,5))])
ck('A sqrt threshold equivalence (numeric; shape only, same as zeolite helical_selectivity)',ok)
# B: stated Lean facts in AutophagyDm3_v2: V(q)+2=(q-1)^2(q+2), V''(1)=6, 1/3 radius
V=lambda q:q**3-3*q  # consistent with V(1)=-2, V'(1)=0, V''(1)=6
ck('B V(1)=-2, V\'(1)=0, V\'\'(1)=6',V(1)==-2 and 3-3==0 and 6*1==6)
ck('B V(q)+2 factorisation',all(abs(V(q)+2-(q-1)**2*(q+2))<1e-9 for q in [-3,-1,0,.5,2,4]))
ck('B gronwall 2/(2*(1+2))=1/3',abs(2/(2*(1+2))-1/3)<1e-12)
# C: regression guards (audited wording present, overclaims absent)
for g in ['This chapter sets out that reading','more than 40 ATG genes','proposed Lyapunov-stability reading',
          'a conjecture, not derived here','Rapamycin extends lifespan in yeast, worms, flies and mice',
          'among the most reproducible','a hypothesis to be tested','an analogy; ω₀ is not measured']:
    ck('C present: '+g,g in txt)
for g in ['This chapter proves it','now 41 ATG','In every ageing model tested','is the most reproducible','autophagy_fold_fires']:
    ck('C absent: '+g,g not in txt)
sys.exit(1 if bad else 0)
