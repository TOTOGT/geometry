import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.rcParams.update({"font.family":"serif","font.size":15,"axes.linewidth":1.1,
                     "savefig.bbox":"tight","savefig.pad_inches":0.04})
EPS=2.0; RSTAR=0.77594059
GOLD="#c8891f"; BLUE="#1c5a8c"; RED="#b03030"; INK="#22222a"
def run(r0,z0=0.0,T=8.0):
    def rhs(t,s):
        r,z=s; e=np.exp(min(-z,200.0))
        return [r*(1-r*r)+EPS*(r-1)*e, r*r-EPS*(r-1)**2*e]
    ev=lambda t,s: s[0]-1e-4
    ev.terminal=True; ev.direction=-1
    return solve_ivp(rhs,(0,T),[r0,z0],method="DOP853",rtol=1e-11,atol=1e-14,events=ev,dense_output=True)

# ---- FIG 1 (replacement): r(t) — the basin story, legible at 2 m ----
fig,ax=plt.subplots(figsize=(7.2,6.3))
for r0 in [2.6,2.0,1.5,1.15,0.95,0.85,0.7765]:
    s=run(r0); ts=np.linspace(0,s.t[-1],1200)
    ax.plot(ts,s.sol(ts)[0],color=BLUE,lw=2.4,alpha=.9)
for r0 in [0.7750,0.75,0.70,0.62]:
    s=run(r0); ts=np.linspace(0,s.t[-1],1200)
    ax.plot(ts,s.sol(ts)[0],color=RED,lw=2.4,ls="--",alpha=.95)
ax.axhline(1,color=GOLD,lw=3.4,zorder=0)
ax.axhline(RSTAR,color=INK,lw=1.4,ls=":",zorder=0)
ax.text(7.75,1.045,r"$\Gamma$  ($r=1$)",color=GOLD,fontsize=17,fontweight="bold",ha="right")
ax.text(0.12,RSTAR-0.075,r"$r_\star$",color=INK,fontsize=17)
ax.text(5.6,0.28,"escape",color=RED,fontsize=17,style="italic")
ax.text(5.6,2.05,"converge",color=BLUE,fontsize=17,style="italic")
ax.set_xlim(0,8); ax.set_ylim(0,2.75)
ax.set_xlabel("$t$"); ax.set_ylabel("$r(t)$")
ax.set_title(r"Orbits either reach $\Gamma$ or collapse — nothing in between",fontsize=16,pad=11)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.savefig("fig_phase.pdf"); plt.close(fig)

# ---- FIG 2 (fixed labels): basin bar ----
fig,ax=plt.subplots(figsize=(7.2,2.5))
L,R=0.40,3.10; f=lambda x:(x-L)/(R-L)
ax.axhspan(0,1,xmin=0,xmax=f(RSTAR),color=RED,alpha=.15)
ax.axhspan(0,1,xmin=f(RSTAR),xmax=1,color=BLUE,alpha=.12)
ax.axvspan(2/3,RSTAR,color=GOLD,alpha=.55)
ax.axvline(2/3,color=INK,lw=1.4,ls=":")
ax.axvline(RSTAR,color=INK,lw=1.8)
ax.axvline(1,color=GOLD,lw=3.2)
ax.annotate(r"$2/3$"+"\nGronwall",(2/3,1.02),xytext=(-46,26),textcoords="offset points",
            fontsize=13,ha="center",arrowprops=dict(arrowstyle="-",color=INK,lw=1))
ax.annotate(r"$r_\star=0.77594$",(RSTAR,1.02),xytext=(30,52),textcoords="offset points",
            fontsize=13.5,ha="center",fontweight="bold",
            arrowprops=dict(arrowstyle="-",color=INK,lw=1))
ax.annotate(r"$\Gamma$",(1,1.02),xytext=(30,20),textcoords="offset points",
            fontsize=16,color=GOLD,fontweight="bold",
            arrowprops=dict(arrowstyle="-",color=GOLD,lw=1.4))
ax.text(0.53,0.46,"ESCAPE",ha="center",va="center",color=RED,fontweight="bold",fontsize=14)
ax.text(2.0,0.46,"BASIN OF ATTRACTION",ha="center",va="center",color=BLUE,fontweight="bold",fontsize=14)
ax.annotate("the gap",( (2/3+RSTAR)/2,0.10),xytext=(-10,-34),textcoords="offset points",
            fontsize=12,color="#7a5a10",ha="center",
            arrowprops=dict(arrowstyle="->",color="#7a5a10",lw=1.1))
ax.set_xlim(L,R); ax.set_ylim(0,1); ax.set_yticks([]); ax.set_xlabel("$r(0)$")
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
fig.savefig("fig_basin.pdf"); plt.close(fig)
print("regenerated")
