# Corrected descriptive audit after review. Local-court misdemeanors, 2023-2025. Associations only.
import pickle,collections as C,math,random,statistics as St
F,X,flow=pickle.load(open('extract.pkl','rb'));ix={k:i for i,k in enumerate(F)}
g=lambda r,k:r[ix[k]]
def num(s):
    if s in('','NULL'):return None
    try:v=float(s)
    except:return 'bad'
    return v if math.isfinite(v) else 'bad'
print('FLOW',flow['all rows'],'all ->',flow[('court','Local')],'local ->',len(X),'local misdemeanor')
print('release decision',C.Counter(g(r,'Release Decision at Arraign') for r in X).most_common())
print('docket status',C.Counter(g(r,'Docket_Status') for r in X).most_common())
print('disp type',C.Counter(g(r,'Disposition_Type') for r in X).most_common())
bs=[r for r in X if g(r,'Release Decision at Arraign')=='Bail-set']
print('bail-set flags (posted,notposted)',C.Counter((g(r,'Bail_Set_and_Posted_at_Arraign'),g(r,'Bail_Set_and_Not_Posted_at_Arraign')) for r in bs).most_common())
def cash(r):
    v=num(g(r,'First_Bail_Set_Cash'))
    if v is None:return 'missing'
    if v=='bad':return 'bad'
    return 'zero' if v==0 else('negative' if v<0 else('exact $1' if v==1 else('(0,1)' if v<1 else '>$1')))
print('cash categories, bail-set',C.Counter(cash(r) for r in bs).most_common())
dur=[num(g(r,'Days_Arraign_to_Dispo')) for r in X]
print('duration: missing',sum(d is None for d in dur),'bad',sum(d=='bad' for d in dur),'negative',sum(isinstance(d,float) and d<0 for d in dur),'zero',sum(d==0 for d in dur),'one',sum(d==1 for d in dur))
print('plea with missing duration',sum(1 for r,d in zip(X,dur) if g(r,'Disposition_Type')=='Plea' and d is None))
def hist(r):
    v=[num(g(r,k)) for k in('prior_vfo_cnt','prior_nonvfo_cnt','prior_misd_cnt')]
    if any(isinstance(a,float) and a>0 for a in v):return 'positive'
    if all(isinstance(a,float) and a==0 for a in v):return 'zero'
    return 'unknown'
def status(r):
    rel=g(r,'Release Decision at Arraign');p=g(r,'Bail_Set_and_Posted_at_Arraign')=='Y';n=g(r,'Bail_Set_and_Not_Posted_at_Arraign')=='Y'
    if rel=='Bail-set':return 'NotPosted' if n and not p else('Posted' if p and not n else 'BailFlagsUnclear')
    return {'ROR':'ROR','Nonmonetary release':'NMR','Remanded':'Remanded','Disposed at arraign':'DisposedAtArraign','Unknown':'UnknownDecision'}.get(rel,'Other')
def ym(r):
    m,_,y=g(r,'First_Arraign_Date').split('/');return int(y),int(m)
def out(r,lim):
    d=num(g(r,'Days_Arraign_to_Dispo'));t=g(r,'Disposition_Type')
    if t=='Plea' and d is None:return None
    if d=='bad' or (isinstance(d,float) and d<0):return None
    return int(t=='Plea' and d is not None and d<=lim)
print('\nsample flow by status',C.Counter(status(r) for r in X).most_common())
print('history by status')
H=C.defaultdict(C.Counter)
for r in X:H[status(r)][hist(r)]+=1
for s,c in H.items():
    n=sum(c.values());print(' ',s,n,{k:round(v/n,3) for k,v in c.items()})
print('not-disposed share by arraign month, late 2025',[(m,round(sum(1 for r in X if ym(r)==(2025,m) and g(r,'Docket_Status')!='Disposed')/max(1,sum(1 for r in X if ym(r)==(2025,m))),3)) for m in range(7,13)])
print('last disposition months',sorted(C.Counter((g(r,'Disposition_Date').split('/')[-1],g(r,'Disposition_Date').split('/')[0]) for r in X if g(r,'Disposition_Date') not in('','NULL')).items())[-5:])
for label,keep in (('all cohorts',lambda r:True),('cohorts through Sep 2025',lambda r:ym(r)<=(2025,9))):
  print('\n==',label)
  T=C.defaultdict(lambda:[0,0,0,0])
  for r in X:
    if not keep(r):continue
    s=status(r);k=s
    if s in('NotPosted','Posted'):k=s+(' exact$1' if cash(r)=='exact $1' else(' >$1' if cash(r)=='>$1' else ' other'))
    a=out(r,30);b=out(r,31);T[k][0]+=1;T[k][1]+=a or 0;T[k][2]+=b or 0;T[k][3]+=(a is None)
  for k,t in sorted(T.items()):print(f'  {k:24s} n={t[0]:7d} <=30 {100*t[1]/t[0]:5.1f}%  <=31 {100*t[2]/t[0]:5.1f}%  unknown-timing {t[3]}')
def bin_(r):
    v=num(g(r,'First_Bail_Set_Cash'));return 'a<=500' if v<=500 else('b<=1000' if v<=1000 else('c<=2500' if v<=2500 else('d<=5000' if v<=5000 else 'e>5000')))
random.seed(20261108)
def est(A,cellf,lim,G1,G0,reps=200):
    R=[(cellf(r),status(r),out(r,lim),g(r,'arr_cycle_id')) for r in A]
    R=[x for x in R if x[2] is not None]
    cl={}
    for i,x in enumerate(R):cl.setdefault(x[3] if x[3] not in('','NULL') else ('row',i),[]).append(i)
    def calc(w):
        c=C.defaultdict(lambda:[0.,0.,0.,0.])
        for x,wi in zip(R,w):
            t=c[x[0]]
            if x[1]==G1:t[0]+=wi;t[1]+=wi*x[2]
            else:t[2]+=wi;t[3]+=wi*x[2]
        W=D=0
        for t in c.values():
            if t[0]>0 and t[2]>0:W+=t[2];D+=t[2]*(t[1]/t[0]-t[3]/t[2])
        return 100*D/W
    pt=calc([1.]*len(R))
    bs=[]
    for _ in range(reps):
        w=[0.]*len(R)
        for ids in cl.values():
            e=random.expovariate(1)
            for i in ids:w[i]=e
        bs.append(calc(w))
    bs.sort()
    c=C.defaultdict(lambda:[0,0])
    for x in R:c[x[0]][x[1]==G1]+=1
    ov=[v for v in c.values() if v[0] and v[1]]
    return pt,bs[int(.025*reps)],bs[int(.975*reps)],len(ov),sum(v[1] for v in ov),sum(1 for x in R if x[1]==G1),sum(v[0] for v in ov),sum(1 for x in R if x[1]==G0),St.median(v[0] for v in ov)
keep=lambda r:ym(r)<=(2025,9)
A=[r for r in X if keep(r) and status(r) in('NotPosted','Posted') and cash(r)=='>$1']
C1=lambda r:(g(r,'Top_Arraign_Article_Section'),g(r,'County_Name'),ym(r)[0],hist(r))
C2=lambda r:C1(r)+(bin_(r),)
C3=lambda r:(g(r,'Top_Arraign_Article_Section'),g(r,'Court_Name'),ym(r)[0],hist(r),bin_(r))
print('\nNotPosted minus Posted, bail >$1, cohorts through Sep 2025, weighted to Posted overlap. Bootstrap percentile range resamples arrest cycles only.')
print('fields: est lo hi | cells | NotPosted used/all | Posted used/all | median posted per cell')
for nm,cf in (('charge+county+year+history',C1),('+bail bin',C2),('charge+court+year+history+bail bin',C3)):
  for lim in (30,31):
    e=est(A,cf,lim,'NotPosted','Posted');print(f'  {nm:38s} <= {lim}: {e[0]:5.1f} [{e[1]:5.1f},{e[2]:5.1f}] | {e[3]} | {e[4]}/{e[5]} | {e[6]}/{e[7]} | {e[8]}')
Y=[r for r in A if status(r)=='NotPosted']
q=C.Counter()
for r in Y:
    p=num(g(r,'Days_Arraign_Bail_Set_to_First_Posted'));d=num(g(r,'Days_Arraign_to_Dispo'))
    q['no posting observed' if p is None else('posting, no disposition' if d is None else('posted before dispo' if p<d else('posted same' if p==d else 'posted after dispo')))]+=1
print('\nposting vs disposition, NotPosted >$1',q.most_common())
print('arr_cycle repeated dockets among A',sum(1 for k,v in C.Counter(g(r,'arr_cycle_id') for r in A if g(r,'arr_cycle_id') not in('','NULL')).items() if v>1),'missing id',sum(1 for r in A if g(r,'arr_cycle_id') in('','NULL')))
