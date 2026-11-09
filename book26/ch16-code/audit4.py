# Step 3: judge diagnostics, descriptive. Local misdemeanors, cases continuing past arraignment, cohorts through Sep 2025.
import pickle,collections as C,math,random,statistics as St
F,X=pickle.load(open('extract2.pkl','rb'));ix={k:i for i,k in enumerate(F)};g=lambda r,k:r[ix[k]]
def num(s):
    if s in('','NULL'):return None
    try:return float(s)
    except:return None
def ym(r):
    m,_,y=g(r,'First_Arraign_Date').split('/');return int(y),int(m)
rows=[]
for r in X:
    if ym(r)>(2025,9) or g(r,'Release Decision at Arraign') in('Disposed at arraign','Unknown',''):continue
    rel=g(r,'Release Decision at Arraign');c=num(g(r,'First_Bail_Set_Cash'))
    d=int(rel=='Remanded' or (rel=='Bail-set' and g(r,'Bail_Set_and_Not_Posted_at_Arraign')=='Y' and c is not None and c>1))
    v=[num(g(r,k)) for k in('prior_vfo_cnt','prior_nonvfo_cnt','prior_misd_cnt')]
    pos=int(any(a is not None and a>0 for a in v));zero=int(all(a is not None and a==0 for a in v))
    t=g(r,'Disposition_Type');dd=num(g(r,'Days_Arraign_to_Dispo'));pl=None if t=='Plea' and dd is None else int(t=='Plea' and dd is not None and dd<=30)
    rows.append(dict(c=g(r,'Court_Name'),j=g(r,'Judge_Name'),y=ym(r)[0],m=ym(r),d=d,pos=pos,zero=zero,black=int(g(r,'Race')=='Black'),awt=g(r,'Top_Charge_Weight_at_Arraign'),cat=g(r,'Arraign Charge Category'),pl=pl))
print('continuing cases',len(rows),'detained-at-arraign rate %.3f'%(sum(r['d'] for r in rows)/len(rows)))
J=C.Counter((r['c'],r['j']) for r in rows)
keep=[r for r in rows if r['j'] not in('','NULL') and J[(r['c'],r['j'])]>=100]
cm=C.defaultdict(set)
for r in keep:cm[(r['c'],r['m'])].add(r['j'])
keep=[r for r in keep if len(cm[(r['c'],r['m'])])>=2]
print('cases kept (judge>=100 cases, >=2 judges in court-month)',len(keep),'judges',len({(r['c'],r['j']) for r in keep}),'courts',len({r['c'] for r in keep}))
print('judges per court-month: median',St.median(len(v) for k,v in cm.items() if len(v)>=2),'share of kept cases in NYC-type courts (Criminal Court name)',round(sum('Criminal Court' in r['c'] for r in keep)/len(keep),3))
S=C.defaultdict(lambda:[0,0])
for r in keep:
    k=(r['c'],r['j'],r['y']);S[k][0]+=1;S[k][1]+=r['d']
for r in keep:
    t=S[(r['c'],r['j'],r['y'])];r['z']=(t[1]-r['d'])/(t[0]-1) if t[0]>1 else None
keep=[r for r in keep if r['z'] is not None]
def dem(key,var,rows):
    a=C.defaultdict(lambda:[0,0.])
    for r in rows:
        if r[var] is None:continue
        t=a[r[key]];t[0]+=1;t[1]+=r[var]
    return lambda r:r[var]-a[r[key]][1]/a[r[key]][0]
for r in keep:r['cell']=(r['c'],r['m'])
zf=dem('cell','z',keep);
for r in keep:r['zt']=zf(r)
sd=St.pstdev(r['zt'] for r in keep);print('leave-out judge detention rate, within court-month SD %.4f'%sd,'p10/p90',[round(sorted(r['zt'] for r in keep)[int(q*len(keep))],4) for q in(.1,.9)])
def slope(var,rs,reps=100):
    rs=[r for r in rs if r[var] is not None]
    f=dem('cell',var,rs);xy=[(r['zt'],f(r),(r['c'],r['j'])) for r in rs]
    b=lambda w:sum(w[k]*x*y for x,y,k in xy)/sum(w[k]*x*x for x,y,k in xy)
    cl={k for _,_,k in xy};p=b({k:1 for k in cl});random.seed(7);B=[]
    for _ in range(reps):B.append(b({k:random.expovariate(1) for k in cl}))
    B.sort();return p,B[int(.025*reps)],B[int(.975*reps)]
for r in keep:
    r['w_a']=int(r['awt']=='AM');r['theft']=int('Larceny' in r['cat']);r['assault']=int('Assault' in r['cat'])
print('slope on judge rate (within court-month; range resamples judges; descriptive). 1-SD effect = slope x %.4f'%sd)
for v,l in (('d','detained at arraign (first stage)'),('pos','positive prior record'),('zero','zero prior record'),('black','Black'),('w_a','class A misdemeanor'),('theft','larceny charge'),('assault','assault charge'),('pl','plea disposition duration<=30')):
    p,lo,hi=slope(v,keep);print(f'  {l:36s} {p:7.3f} [{lo:7.3f},{hi:7.3f}]  1-SD: {100*p*sd:6.2f} pp')
