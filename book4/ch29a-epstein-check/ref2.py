from ref import *
mp.dps=40
def data(x0,y0,s):
    f=lambda x,y:E_series(x,y,s,K=30)
    v=f(x0,y0); fx=diff(f,(x0,y0),(1,0)); fy=diff(f,(x0,y0),(0,1))
    fxx=diff(f,(x0,y0),(2,0)); fyy=diff(f,(x0,y0),(0,2)); fxy=diff(f,(x0,y0),(1,1))
    H=matrix([[fxx,fxy],[fxy,fyy]]); ev=eigsy(H,eigvals_only=True)
    return dict(value=float(v),fx=float(fx),fy=float(fy),fxx=float(fxx),fyy=float(fyy),fxy=float(fxy),ev=[float(e) for e in ev],trace_lhs=float(y0**2*(fxx+fyy)),trace_rhs=float(s*(s-1)*v))
out={}
rho_y=sqrt(3)/2
for s in (2,3,5):
    out[str(s)]={'i':data(mpf(0),mpf(1),s),'rho':data(mpf(1)/2,rho_y,s)}
json.dump(out,open('ref.json','w'),indent=1)
for s in out:
    for k in out[s]: print(s,k,{a:(round(b,8) if isinstance(b,float) else [round(e,8) for e in b]) for a,b in out[s][k].items()})
