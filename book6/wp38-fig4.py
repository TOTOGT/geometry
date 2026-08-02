import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter

PAPER="#f6f3ec"; INK="#12141a"; DIM="#6f6857"; RULE="#c4bba8"
NAVY="#17435f"; GOLD="#c9a84c"; RED="#8b1a1a"
plt.rcParams.update({"font.family":"DejaVu Serif","text.usetex":False,
                     "svg.fonttype":"none","figure.facecolor":"white","axes.facecolor":"white"})

rows=[  # label, multiple, detail, colour
 ("Henry Hub\nUri, Feb 2021",              6.0,  "3.76 → 23.86 $/MMBtu",   NAVY),
 ("Panama Canal slot\nNov 2023 · $3.98m",  10.0, "vs ~$400k standard toll",GOLD),
 ("COMEX–London gold\n24 Mar 2020",        50.0, "1–2 → 70–80 $/oz spread",GOLD),
 ("Waha hub\nUri, Feb 2021",               82.0, "→ $206.19/MMBtu",        NAVY),
 ("Oklahoma spot gas\nUri, Feb 2021",     400.0, "~3 → >1,200 $/Mcf",      NAVY),
]
fig,ax=plt.subplots(figsize=(9.4,4.5))
y=range(len(rows))
ax.barh(list(y),[r[1] for r in rows],height=.52,
        color=[r[3] for r in rows],edgecolor="none",zorder=3)
for i,(lab,v,det,c) in enumerate(rows):
    ax.text(v*1.16,i,f"{v:.0f}×",va="center",ha="left",fontsize=11.5,
            fontweight="bold",color=INK,zorder=4)
    ax.text(v*1.16,i-.30,det,va="center",ha="left",fontsize=8.2,color=DIM,zorder=4)

ax.set_xscale("log"); ax.set_xlim(1,4200); ax.set_ylim(-.72,len(rows)-.22)
ax.set_yticks(list(y)); ax.set_yticklabels([r[0] for r in rows],fontsize=9.6,color=INK)
ax.xaxis.set_major_locator(LogLocator(base=10,numticks=5))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.tick_params(axis="x",labelsize=9.5,colors=DIM); ax.tick_params(axis="y",length=0)
ax.set_xlabel("positional rent — multiple of pre-event baseline  (log scale)",
              fontsize=9.8,color=DIM,labelpad=8)
ax.grid(axis="x",which="major",color=RULE,lw=.6,alpha=.55,zorder=0)
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(RULE)
ax.set_title("Five episodes where λ → 0 exogenously",fontsize=13,color=INK,
             loc="left",pad=14)

# WTI note moved OUT of the axes, below the x-label, on its own rule
fig.subplots_adjust(left=.205,right=.985,top=.885,bottom=.30)
fig.add_artist(plt.Line2D([.205,.985],[.145,.145],color=RULE,lw=.8))
fig.text(.205,.115,
 "Sixth episode, off-scale:  WTI May-2020 (20 Apr) settled at −$37.63 — a sign inversion, not a "
 "multiple.\nPosition = empty tank space. Excluded from the ratio axis; it is the reason the set "
 "identifies.",fontsize=8.6,color=RED,va="top",linespacing=1.55)
fig.savefig("/tmp/fig4.svg",format="svg",bbox_inches=None)
print("ok")
