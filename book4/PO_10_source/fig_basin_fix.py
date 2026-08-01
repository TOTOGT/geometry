import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"serif","font.size":15,"savefig.bbox":"tight","savefig.pad_inches":0.06})
GOLD="#c8891f"; BLUE="#1c5a8c"; RED="#b03030"; INK="#22222a"; RSTAR=0.77594059
fig,ax=plt.subplots(figsize=(7.2,3.0))
L,R=0.40,3.10; f=lambda x:(x-L)/(R-L)
ax.axhspan(0,1,xmin=0,xmax=f(RSTAR),color=RED,alpha=.15)
ax.axhspan(0,1,xmin=f(RSTAR),xmax=1,color=BLUE,alpha=.12)
ax.axvspan(2/3,RSTAR,color=GOLD,alpha=.60)
ax.axvline(2/3,color=INK,lw=1.4,ls=":"); ax.axvline(RSTAR,color=INK,lw=2.0); ax.axvline(1,color=GOLD,lw=3.4)
ax.text(2/3-0.09,1.66,"$2/3$",ha="center",fontsize=14)
ax.text(2/3-0.09,1.36,"Gronwall",ha="center",fontsize=12,color=INK)
ax.plot([2/3,2/3-0.09],[1.02,1.30],color=INK,lw=.9)
ax.text(RSTAR+0.46,1.62,r"$r_\star=0.77594$",ha="center",fontsize=15,fontweight="bold")
ax.plot([RSTAR,RSTAR+0.34],[1.02,1.52],color=INK,lw=.9)
ax.text(1.0,1.20,r"$\Gamma$",ha="center",fontsize=18,color=GOLD,fontweight="bold")
ax.text(0.53,0.50,"ESCAPE",ha="center",va="center",color=RED,fontweight="bold",fontsize=15)
ax.text(2.05,0.50,"BASIN OF ATTRACTION",ha="center",va="center",color=BLUE,fontweight="bold",fontsize=15)
ax.annotate("the gap",xy=((2/3+RSTAR)/2,0.06),xytext=(1.30,-0.62),fontsize=13,color="#7a5a10",
            ha="center",arrowprops=dict(arrowstyle="->",color="#7a5a10",lw=1.2),annotation_clip=False)
ax.set_xlim(L,R); ax.set_ylim(0,2.0); ax.set_yticks([]); ax.set_xlabel("$r(0)$",labelpad=26)
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_bounds(L,R)
fig.savefig("fig_basin.pdf"); plt.close(fig); print("basin fixed")
