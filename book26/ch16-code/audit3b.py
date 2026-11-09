# Fixed-population robustness: all three specifications on the cases retained by the strictest one.
import io,contextlib
src=open('audit3.py').read().split("print('\\nNotPosted minus Posted")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
cnt=C.defaultdict(lambda:[0,0])
for r in A:
    if out(r,30) is None: continue
    cnt[C3(r)][status(r)=='NotPosted']+=1
fixed=[r for r in A if out(r,30) is not None and cnt[C3(r)][0] and cnt[C3(r)][1]]
print('fixed population: NotPosted',sum(status(r)=='NotPosted' for r in fixed),'Posted',sum(status(r)=='Posted' for r in fixed))
for nm,cf in (('charge+county+year+history',C1),('+bail bin',C2),('charge+court+year+history+bail bin',C3)):
    e=est(fixed,cf,30,'NotPosted','Posted');print(f'  {nm:38s} <=30: {e[0]:5.1f} [{e[1]:5.1f},{e[2]:5.1f}] cells {e[3]}')
print('raw on fixed population: %.1f'%(100*(sum(out(r,30) for r in fixed if status(r)=="NotPosted")/sum(status(r)=="NotPosted" for r in fixed)-sum(out(r,30) for r in fixed if status(r)=="Posted")/sum(status(r)=="Posted" for r in fixed))))
