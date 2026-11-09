# Primary contrast: bail >$1, charge x court x year x history x bail band, cohorts through Sep 2025. Denominators, bounds, transfers, frozen-weight resampling, earlier cohorts.
import io,contextlib
src=open('audit3.py').read().split("print('\\nNotPosted minus Posted")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
C3=lambda r:(g(r,'Top_Arraign_Article_Section'),g(r,'Court_Name'),ym(r)[0],hist(r),bin_(r))
def run(cut,label):
    A=[r for r in X if ym(r)<=cut and status(r) in('NotPosted','Posted') and cash(r)=='>$1']
    print('\n==',label,'eligible',C.Counter(status(r) for r in A))
    for s in('NotPosted','Posted'):
        R=[r for r in A if status(r)==s];un=sum(out(r,30) is None for r in R);K=[r for r in R if out(r,30) is not None];y=sum(out(r,30) for r in K);n=len(K)
        tr=sum(1 for r in K if 'GJ' in g(r,'Disposition_Type') and num(g(r,'Days_Arraign_to_Dispo')) is not None and num(g(r,'Days_Arraign_to_Dispo'))<=30)
        print(f' {s}: eligible {len(R)} unknown-timing {un} denominator {n} early pleas {y} rate {100*y/n:.1f}% bounds {100*y/(n+un):.1f}-{100*(y+un)/(n+un):.1f}% transfers<=30 {tr} ({100*tr/n:.1f}%)')
    cnt=C.defaultdict(lambda:[0,0])
    for r in A:
        if out(r,30) is not None:cnt[C3(r)][status(r)=='NotPosted']+=1
    F_=[r for r in A if out(r,30) is not None and cnt[C3(r)][0] and cnt[C3(r)][1]]
    for s in('NotPosted','Posted'):
        R=[r for r in F_ if status(r)==s];y=sum(out(r,30) for r in R);tr=sum(1 for r in R if 'GJ' in g(r,'Disposition_Type') and (num(g(r,'Days_Arraign_to_Dispo')) or 999)<=30);print(f' overlap {s}: n {len(R)} early pleas {y} ({100*y/len(R):.1f}%) transfers {tr} ({100*tr/len(R):.1f}%)')
    cells=C.defaultdict(lambda:{'N':[],'P':[]})
    for r in F_:cells[C3(r)]['N' if status(r)=='NotPosted' else 'P'].append((out(r,30),g(r,'arr_cycle_id')))
    W={k:len(v['P']) for k,v in cells.items()};T=sum(W.values())
    pt=sum(W[k]*(sum(y for y,_ in v['N'])/len(v['N'])-sum(y for y,_ in v['P'])/len(v['P'])) for k,v in cells.items())/T*100
    def draw(seed,reps):
        random.seed(seed);out_=[]
        rid=0;ids=[]
        for k,v in cells.items():
            for grp in('N','P'):
                for y,c in v[grp]:
                    if c in('','NULL'):rid+=1;c=('r',rid)
                    ids.append(c)
        uniq=list(set(ids))
        for _ in range(reps):
            w=dict((c,random.expovariate(1)) for c in uniq);i=0;tot=0
            for k,v in cells.items():
                a=b=c_=d=0
                for y,_x in v['N']:
                    e=w[ids[i]];i+=1;a+=e;b+=e*y
                for y,_x in v['P']:
                    e=w[ids[i]];i+=1;c_+=e;d+=e*y
                tot+=W[k]*(b/a-d/c_)
            out_.append(100*tot/T)
        out_.sort();return out_
    one=sum(1 for v in cells.values() if len(v['P'])==1)
    print(f' estimate {pt:.2f}; cells {len(cells)}; cells with one posted case {one}; posted weight frozen at observed counts')
    if label.startswith('primary'):
        for sd in(11,22):
            B=draw(sd,1000);print(f'  seed {sd}: 1000 draws, 2.5/97.5 pct {B[25]:.2f} {B[975]:.2f}; min {B[0]:.2f} max {B[-1]:.2f}')
run((2025,9),'primary through Sep 2025')
run((2025,6),'through Jun 2025')
run((2024,12),'through Dec 2024')
