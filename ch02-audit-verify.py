#!/usr/bin/env python3
"""ch02-biological audit (stdlib). Exit 0 = pass."""
import math,re,sys
bad=0
def ck(n,c):
    global bad; print(('PASS ' if c else 'FAIL ')+n); bad+=(not c)
raw=open('ch02-biological.html',encoding='utf-8').read()
t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',raw))
ck('HPA omega .21 -> period ~30 s',abs(2*math.pi/0.21-29.9)<0.2)
ck('theta 7 Hz -> 44 rad/s; .45 rad/s -> .072 Hz',abs(2*math.pi*7-43.98)<0.01 and abs(0.45/(2*math.pi)-0.0716)<1e-3)
ck('circadian omega 2pi/86400',abs(2*math.pi/86400-7.27e-5)<1e-7)
ck('immune omega .18 -> ~35 s',abs(2*math.pi/0.18-34.9)<0.2)
for m,v in [('HPA',.38),('neural',.55),('circadian',.29),('immune',.44)]:
    ck(f'relaxation time {m} = {1/v:.1f} s (seconds, not hours)',1/v<4)
r=lambda c,h:(round(c-h,2),round(c+h,2))
ck('kappa: HPA prediction 0.14-0.22 is wider than table 0.15-0.22',r(.18,.04)==(0.14,0.22) and r(.18,.04)!=(0.15,0.22))
ck('kappa: neural and immune match table',r(.30,.05)==(.25,.35) and r(.15,.04)==(.11,.19))
for g in ['Status: stated, unsourced','withdrawn until one is shown','Audit note (2026-10-25)','not a theta rhythm','shared functional form, not a demonstrated shared invariant','conditional proposals','wider than the tabulated HPA range']:
    ck('present: '+g,g in t)
for g in ['computed from first principles; none are fitted','derived from the geometry of each system, not from fitting','is the theta frequency (~7 Hz)']:
    ck('absent: '+g,g not in t)
sys.exit(1 if bad else 0)
