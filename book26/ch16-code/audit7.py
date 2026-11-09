# Denominator audit for every rate displayed in the status table, cohorts through Sep 2025, <=30.
import io,contextlib
src=open('audit3.py').read().split("print('\\nNotPosted minus Posted")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
T=C.defaultdict(lambda:[0,0,0])
for r in X:
    if ym(r)>(2025,9):continue
    s=status(r);k=s
    if s in('NotPosted','Posted'):k=s+(' exact$1' if cash(r)=='exact $1' else(' >$1' if cash(r)=='>$1' else ' other'))
    a=out(r,30);T[k][0]+=1
    if a is None:T[k][1]+=1
    else:T[k][2]+=a
for k,t in sorted(T.items()):
    n=t[0]-t[1];print(f'{k:24s} eligible {t[0]} unknown {t[1]} denominator {n} early pleas {t[2]} rate {100*t[2]/n:.1f}%')
