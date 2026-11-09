# Judge diagnostics on all arraignments with known decisions, including dispositions at arraignment; continuation as an outcome. Descriptive.
import pickle,collections as C,random,statistics as St
F,X=pickle.load(open('extract2.pkl','rb'));ix={k:i for i,k in enumerate(F)};g=lambda r,k:r[ix[k]]
def num(s):
    if s in('','NULL'):return None
    try:return float(s)
    except:return None
def ym(r):
    m,_,y=g(r,'First_Arraign_Date').split('/');return int(y),int(m)
rows=[]
for r in X:
    if ym(r)>(2025,9):continue
    rel=g(r,'Release Decision at Arraign')
    if rel in('Unknown',''):continue
    j=g(r,'Judge_Name')
    if j in('','NULL'):continue
    c=num(g(r,'First_Bail_Set_Cash'))
    d=int(rel=='Remanded' or (rel=='Bail-set' and g(r,'Bail_Set_and_Not_Posted_at_Arraign')=='Y' and c is not None and c>1))
    v=[num(g(r,k)) for k in('prior_vfo_cnt','prior_nonvfo_cnt','prior_misd_cnt')]
    pos=int(any(a is not None and a>0 for a in v));zero=int(all(a is not None and a==0 for a in v))
    ac=g(r,'arr_cycle_id')
    rows.append(dict(c=g(r,'Court_Name'),j=j,y=ym(r)[0],cell=(g(r,'Court_Name'),ym(r)),cont=int(rel!='Disposed at arraign'),d=d,pos=pos,zero=zero,unk=int(not pos and not zero),black=int(g(r,'Race')=='Black'),A=int(g(r,'Top_Charge_Weight_at_Arraign')=='AM'),assault=int('Assault' in g(r,'Arraign Charge Category')),larc=int('Larceny' in g(r,'Arraign Charge Category')),ac=ac))
J=C.Counter((r['c'],r['j']) for r in rows if r['cont'])
keep=[r for r in rows if J[(r['c'],r['j'])]>=100]
cm=C.defaultdict(set)
for r in keep:cm[r['cell']].add(r['j'])
keep=[r for r in keep if len(cm[r['cell']])>=2]
print('all arraignments kept',len(keep),'continuing',sum(r['cont'] for r in keep),'judges',len({(r['c'],r['j']) for r in keep}))
# leave-out: remove all dockets of the same arrest cycle in the judge-year; blank cycle ids remove only the row
S=C.defaultdict(lambda:[0,0]);Cy=C.defaultdict(lambda:[0,0])
for r in keep:
    if r['cont']:
        k=(r['c'],r['j'],r['y']);S[k][0]+=1;S[k][1]+=r['d']
        if r['ac'] not in('','NULL'):Cy[k+(r['ac'],)][0]+=1;Cy[k+(r['ac'],)][1]+=r['d']
out=[]
for r in keep:
    k=(r['c'],r['j'],r['y']);n,s=S[k]
    if r['ac'] not in('','NULL') and (k+(r['ac'],)) in Cy:
        a,b=Cy[k+(r['ac'],)];n-=a;s-=b
    elif r['cont']:n-=1;s-=r['d']
    if n>0:r['z']=s/n;out.append(r)
keep=out
def dem(var,rs):
    a=C.defaultdict(lambda:[0,0.])
    for r in rs:a[r['cell']][0]+=1;a[r['cell']][1]+=r[var]
    return lambda r:r[var]-a[r['cell']][1]/a[r['cell']][0]
f=dem('z',keep)
for r in keep:r['zt']=f(r)
sd=St.pstdev(r['zt'] for r in keep);print('leave-out strictness: detained at arraign = remanded or bail >$1 not posted; judge-year mean over continuing cases, excluding the same arrest cycle (or the row if no id); demeaned by court-month. SD %.4f'%sd)
def slope(var,rs,reps=1000):
    h=dem(var,rs);A=C.defaultdict(lambda:[0.,0.])
    for r in rs:
        k=(r['c'],r['j']);A[k][0]+=r['zt']*h(r);A[k][1]+=r['zt']**2
    V=list(A.values());p=sum(a for a,b in V)/sum(b for a,b in V);B=[]
    for _ in range(reps):
        n=d=0.
        for a_,b_ in V:
            e=random.expovariate(1);n+=e*a_;d+=e*b_
        B.append(n/d)
    B.sort();return p,B[int(.025*reps)],B[int(.975*reps)]
random.seed(5)
for lab,rs in (('ALL arraignments incl. disposed at arraignment',keep),('continuing only',[r for r in keep if r['cont']])):
    print('\n',lab,len(rs))
    for v,l in (('cont','continues past arraignment'),('pos','positive history'),('zero','all history zero'),('unk','history unknown'),('black','Black'),('A','class A misdemeanor'),('assault','assault'),('larc','larceny')):
        if v=='cont' and not lab.startswith('ALL'):continue
        p,lo,hi=slope(v,rs);print(f'  {l:30s} 1-SD: {100*p*sd:6.2f} pp [{100*lo*sd:6.2f},{100*hi*sd:6.2f}]')
