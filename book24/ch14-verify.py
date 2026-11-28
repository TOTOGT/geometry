#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch14-verify.py -- the elementary checks behind book24/ch14-tensor-spectrum-matmul.html.   python3 book24/ch14-verify.py
Standard library only. This checks arithmetic and one planar identity. It does not check any theorem of the OpenAI preprints.

  [1] exact: 6/3 = 2 and 6/(8/3) = 9/4 (the two ratios quoted in section 4); 3 * (3/4) = 9/4 (e = 3t with t <= 3/4)
  [2] exact: (1 + 1/(3m))^3 >= 1 + 1/m for m = 1..2000 (the step in Lemma 5.1 of the October paper), as Fractions
  [3] planar mean width: W(S) = sqrt(2 pi) E max <g,s>  equals half the perimeter of conv(S). E max <g,s> = E|g| * mean over
      directions of the support function; E|g| = sqrt(pi/2). The direction average is a deterministic midpoint rule (200000 points).
      Cases: segment of length 2; equilateral triangle side 2 (expect 3); 3-4-5 triangle (expect 6); collinear 0,1,2 (expect 2);
      the obtuse triangle (0,0),(4,0),(1,0.5) (expect half its perimeter, 4.0797, not the Monte Carlo 4.0744)
  [4] the page links to the preprints at their original source and says the Lean status is unverified
"""
import math, sys, re
from fractions import Fraction as Fr
from pathlib import Path
HERE=Path(__file__).resolve().parent
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*70+'\n  [%s]  %s\n'%(n,t)+'='*70)

head(1,'exact ratios')
check(Fr(6,3)==2,'6/3 = 2')
check(Fr(6)/Fr(8,3)==Fr(9,4),'6/(8/3) = 9/4')
check(3*Fr(3,4)==Fr(9,4),'3 * 3/4 = 9/4')

head(2,'(1+1/(3m))^3 >= 1+1/m')
ok=all((1+Fr(1,3*m))**3>=1+Fr(1,m) for m in range(1,2001))
check(ok,'holds for m = 1..2000 (exact); expansion 1+1/m+1/(3m^2)+1/(27m^3) shows it for all m')

head(3,'planar mean width = half perimeter of the convex hull')
def hull(pts):
    pts=sorted(set(pts))
    if len(pts)<=2: return pts
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def perim(pts):
    h=hull(pts)
    if len(h)==2: return 2*math.dist(h[0],h[1])
    return sum(math.dist(h[i],h[(i+1)%len(h)]) for i in range(len(h)))
def W(pts,N=200000):
    s=0.0
    for i in range(N):
        th=2*math.pi*(i+0.5)/N; c,sn=math.cos(th),math.sin(th)
        s+=max(p[0]*c+p[1]*sn for p in pts)
    return math.sqrt(2*math.pi)*math.sqrt(math.pi/2)*(s/N)
cases={'segment length 2':[(0,0),(2,0)],
 'equilateral side 2':[(0,0),(2,0),(1,math.sqrt(3))],
 '3-4-5':[(0,0),(4,0),(0,3)],
 'collinear 0,1,2':[(0,0),(1,0),(2,0)],
 'obtuse (0,0),(4,0),(1,0.5)':[(0,0),(4,0),(1,0.5)]}
for name,pts in cases.items():
    w=W(pts); h=perim(pts)/2
    print('      %-30s W=%.5f  half-perimeter=%.5f'%(name,w,h))
    check(abs(w-h)<1e-4,name)
check(abs(perim(cases['obtuse (0,0),(4,0),(1,0.5)'])/2-4.0797)<1e-3,'obtuse triangle exact value 4.0797 (the audit Monte Carlo gave 4.0744, within sampling error)')

head(4,'page claims')
t=(HERE/'ch14-tensor-spectrum-matmul.html').read_text()
check('github.com/openai/math/blob/' in t,'links to the preprints at their original repository')
check('unverified' in t,'says the Lean status is unverified')
check('92b516ef8e2abf66c3db7aa31438d3010bc7956f' in t,'pins the commit')
print('\n'+('ALL PASS' if not fails else 'FAILURES: %d'%len(fails)))
sys.exit(1 if fails else 0)
