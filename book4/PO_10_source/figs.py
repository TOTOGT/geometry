import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.rcParams.update({"font.family":"serif","font.size":13,"axes.linewidth":1.0,
                     "savefig.bbox":"tight","savefig.pad_inches":0.03})
EPS=2.0; RSTAR=0.77594059
GOLD="#c8891f"; BLUE="#1c5a8c"; RED="#b03030"; INK="#22222a"

def run(r0,z0=0.0,T=14.0):
    def rhs(t,s):
        r,z=s; e=np.exp(min(-z,200.0))
        return [r*(1-r*r)+EPS*(r-1)*e, r*r-EPS*(r-1)**2*e]
    ev=lambda t,s: s[0]-1e-4
    ev.terminal=True; ev.direction=-1
    return solve_ivp(rhs,(0,T),[r0,z0],method="DOP853",rtol=1e-11,atol=1e-14,
                     events=ev,dense_output=True)

# ---------- FIG 1 : (r,z) phase portrait ----------
fig,ax=plt.subplots(figsize=(7.2,5.4))
for r0 in [3.0,2.0,1.5,1.1,0.90,0.80,0.7760]:
    s=run(r0); ts=np.linspace(0,s.t[-1],1500); y=s.sol(ts)
    ax.plot(y[0],y[1],color=BLUE,lw=1.7,alpha=.85)
for r0 in [0.7755,0.74,0.70,0.60]:
    s=run(r0); ts=np.linspace(0,s.t[-1],1500); y=s.sol(ts)
    ax.plot(y[0],y[1],color=RED,lw=1.7,ls="--",alpha=.9)
ax.axvline(1,color=GOLD,lw=3,zorder=0)
ax.axvline(RSTAR,color=INK,lw=1.2,ls=":",zorder=0)
ax.text(1.02,-7.4,r"$\Gamma$  ($r=1$)",color=GOLD,fontsize=14,fontweight="bold")
ax.text(RSTAR-0.02,-7.4,r"$r_\star$",color=INK,ha="right",fontsize=14)
ax.set_xlim(0.45,3.15); ax.set_ylim(-8,15)
ax.set_xlabel("$r$"); ax.set_ylabel("$z$")
ax.set_title("Trajectories in the $(r,z)$ plane",fontsize=15,pad=10)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.savefig("fig_phase.pdf"); plt.close(fig)

# ---------- FIG 2 : basin of attraction on the r-axis ----------
fig,ax=plt.subplots(figsize=(7.2,1.95))
ax.axhspan(0,1,xmin=0,xmax=(RSTAR-0.4)/2.7,color=RED,alpha=.16)
ax.axhspan(0,1,xmin=(RSTAR-0.4)/2.7,xmax=1,color=BLUE,alpha=.13)
ax.axvspan(2/3,RSTAR,color=GOLD,alpha=.45)
for x,lab,c in [(2/3,r"$2/3$"+"\nGronwall",INK),(RSTAR,r"$r_\star=0.77594$",INK),(1,r"$\Gamma$",GOLD)]:
    ax.axvline(x,color=c,lw=2.2 if x==1 else 1.3,ls="-" if x==1 else ":")
    ax.text(x,1.16,lab,ha="center",va="bottom",fontsize=11.5,color=c)
ax.text(0.52,0.5,"ESCAPE",ha="center",va="center",color=RED,fontweight="bold",fontsize=12)
ax.text(1.9,0.5,"BASIN OF ATTRACTION",ha="center",va="center",color=BLUE,fontweight="bold",fontsize=12)
ax.text((2/3+RSTAR)/2,0.5,"gap",ha="center",va="center",fontsize=10,color="#7a5a10")
ax.set_xlim(0.4,3.1); ax.set_ylim(0,1); ax.set_yticks([])
ax.set_xlabel("$r(0)$")
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
fig.savefig("fig_basin.pdf"); plt.close(fig)

# ---------- FIG 3 : exponential decay, slope -2 ----------
fig,ax=plt.subplots(figsize=(7.2,5.7))
for r0,lab in [(1.10,"$r_0=1.10$"),(1.50,"$r_0=1.50$"),(3.00,"$r_0=3.00$"),(0.90,"$r_0=0.90$")]:
    s=run(r0,T=9); ts=np.linspace(0,9,2000); u=np.abs(s.sol(ts)[0]-1)
    ax.plot(ts,np.log10(u),lw=1.9,label=lab)
t=np.linspace(1.5,8,10)
ax.plot(t,np.log10(0.5)-2*t/np.log(10),color=INK,ls="--",lw=1.6,label=r"slope $\mu=-2$")
ax.set_xlabel("$t$"); ax.set_ylabel(r"$\log_{10}|r(t)-1|$")
ax.set_title(r"Exponential convergence at rate $\mu=-2$",fontsize=15,pad=10)
ax.legend(frameon=False,fontsize=11.5,loc="upper right"); ax.set_ylim(-14,0.6)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.savefig("fig_decay.pdf"); plt.close(fig)

# ---------- FIG 4 : the scaling law r*(lambda) ----------
def rstar_of(lam):
    z0=np.log(EPS/lam); lo,hi=0.001,1.0
    for _ in range(46):
        m=.5*(lo+hi); s=run(m,z0,T=40)
        ok = s.t_events[0].size==0 and abs(s.y[0,-1]-1)<1e-5
        if ok: hi=m
        else: lo=m
    return .5*(lo+hi)
lams=np.linspace(0.35,3.2,26); rs=[rstar_of(l) for l in lams]
fig,ax=plt.subplots(figsize=(7.2,5.7))
ax.plot(lams,rs,color=BLUE,lw=2.4)
ax.axhline(2/3,color=INK,ls=":",lw=1.3); ax.text(3.15,2/3+.012,"$2/3$",ha="right",fontsize=12)
for lam,val,lab in [(1.0,0.57224,r"$\lambda=1$  ($z_0=\log 2$)"),(2.0,RSTAR,r"$\lambda=2$  ($z_0=0$)")]:
    ax.plot([lam],[val],"o",color=GOLD,ms=10,zorder=5,mec=INK,mew=.8)
    ax.annotate(lab+f"\n$r_\\star={val:.5f}$",(lam,val),textcoords="offset points",
                xytext=(12,-34),fontsize=11.5)
ax.set_xlabel(r"$\lambda=\varepsilon\,e^{-z(0)}$"); ax.set_ylabel(r"$r_\star$")
ax.set_title(r"The basin boundary depends on $(\varepsilon,z_0)$ only through $\lambda$",fontsize=14.5,pad=10)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.savefig("fig_lambda.pdf"); plt.close(fig)
print("figures written")
