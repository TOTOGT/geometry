#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp138-verify.py -- companion to book6/wp138-the-hive-on-earth.html. Written 2026-10-26. Run BEFORE trusting the page's numbers.
RECOMPUTED here: family and school sizing from the 2024 DoD family counts (assumes ~1.3 M active duty, NOT confirmed in the source);
Newark land and household arithmetic; four-county shares; regular-polygon wall length per unit area.
QUOTED, NOT CHECKED: 15,000-25,000 troops (secondary report of a speech); Census figures (fetched 2026-10-26); the memo itself (not read).
NOT A SOURCE FOR: where the Pentagon will build, what it will accept, or any county's housing, school or flood capacity."""
import math, re, sys
from pathlib import Path
fails=[]
def check(ok,msg):
    print('    %s  %s'%('PASS' if ok else 'FAIL',msg))
    if not ok: fails.append(msg)
def head(n,t): print('\n'+'='*70+'\n  [%s]  %s\n'%(n,t)+'='*70)
PAGE=Path(__file__).resolve().parent/'wp138-the-hive-on-earth.html'
html=PAGE.read_text(encoding='utf-8') if PAGE.exists() else ''

head(1,'sizing from the 2024 DoD active-duty family profile')
FAM,SPOUSE,KIDS=1495107,621400,869007
AD=1.3e6   # assumption
ratio=FAM/AD; kratio=KIDS/AD
print('    family members per member = %.4f ; children per member = %.4f (AD assumed 1.3 M)'%(ratio,kratio))
rows={}
for t in (15000,25000):
    fam=t*ratio; res=t+fam; kids=t*kratio
    rows[t]=(fam,res,kids,kids*.411,kids*(.325+.226))
    print('    %d troops: family %d, residents %d, children %d, ages 0-5 %d, ages 6-18 %d, schools@650 %.1f'%(t,fam,res,kids,kids*.411,kids*.551,kids*.551/650))
check(round(rows[15000][1],-2)==32300 and round(rows[25000][1],-2)==53800,'residents about 32,000 to 54,000')
check(abs(.411+.325+.226-.962)<1e-9,'the three age shares in the source sum to 96.2 percent (the rest is 19+ or unreported)')

head(2,'Newark')
NEW_POP,DENS,HH,ACRES=323808,12903.8,2.62,65
for res in (rows[15000][1],rows[25000][1]):
    print('    %d residents: %.2f sq mi at Newark density, %d households, +%.1f%% of 323,808, half to counties -> %.0f units/acre on %d acres'%(res,res/DENS,res/HH,100*res/NEW_POP,res/HH/2/ACRES,ACRES))
check(abs(rows[15000][1]/DENS-2.50)<0.01 and abs(rows[25000][1]/DENS-4.17)<0.01,'2.5 to 4.2 sq mi')
check(round(rows[15000][1]/HH/2/ACRES)==95 and round(rows[25000][1]/HH/2/ACRES)==158,'about 95 to 158 units per acre')

head(3,'four counties')
POP={'Bergen':955743,'Essex':863728,'Hudson':724858,'Passaic':524118}
tot=sum(POP.values()); print('    total %d'%tot)
for x in (100000,rows[15000][1],rows[25000][1]): print('    %d is %.2f%% of the four counties'%(x,100*x/tot))
check(tot==3068447,'four-county 2020 total 3,068,447 (Bergen and Hudson from citypopulation.de, Essex and Passaic from QuickFacts: mixed sources)')
check(abs(100000/tot*100-3.26)<0.01,'100,000 is about 3.3 percent')
print('    even split of military residents: %d to %d per county'%(rows[15000][1]/4,rows[25000][1]/4))

head(4,'regular polygon wall length per unit area (perimeter / sqrt(area))')
hexa=2*math.sqrt(2*math.sqrt(3)); sq=4.0; tri=3*math.sqrt(4/math.sqrt(3))
print('    hexagon %.3f  square %.3f  triangle %.3f'%(hexa,sq,tri))
check(abs(hexa-3.722)<0.001 and abs(tri-4.559)<0.001,'3.722 / 4.000 / 4.559')

head(5,'page labels and exclusions')
low=re.sub(r'<[^>]+>',' ',html).lower()
for lab in ['concept, not a nomination','memo was not read','schematic, not a map','not peer-reviewed','assumes about 1.3 million','not checked']:
    check(lab in low,'label present: '+lab)
check(not re.search(r'>\s*90\s*%\s*crew dose|lonsdaleite',low),'cut lunar claims (>90% crew dose, lonsdaleite) not reintroduced')
check('wp136-living-in-a-moon-habitat.html' in html and 'Orthogenesis/Architecture/hex-habitat.html' in html and (Path(__file__).resolve().parent.parent/'Orthogenesis/Architecture/hex-habitat.html').exists(),'links to WP136 and to Hex Habitat Mars (file exists)')
check(not any(b in html for b in ('fetch(','localStorage','XMLHttpRequest')),'no network or storage calls')
print('\n[HONESTY] Arithmetic and labels only. It does not show where the base would go, that any county has capacity, or that the competition would accept this.')
print('\nALL PASS' if not fails else '\nFAILED: %d'%len(fails)); sys.exit(1 if fails else 0)
