#!/usr/bin/env python3
"""Recount strict engineering-term coverage per topic; verify every page named in the map exists.
Baseline: git HEAD at run time. Prose pages only (no docs/, _to_delete, _archive, node_modules, zenodo/pt duplicates)."""
import re,glob,os,sys
T={
"Differential & integral calculus":r"differential calculus|integral calculus|fundamental theorem of calculus|line integral|Stokes'? theorem",
"Statics":r"\bstatics\b|free[- ]body|static equilibrium|method of joints|moment of (a )?force",
"Dynamics":r"rigid[- ]body|Newton'?s second law|angular momentum|Lagrangian|equations? of motion",
"Strength of materials":r"strength of materials|bending moment|shear force|Young'?s modulus|von Mises|beam deflection|yield strength|Hooke",
"Stress chain":r"stress chain|force chain|load path",
"Hydraulics":r"hydraulic|Manning|head loss|hydro(power|electric)|run-of-river",
"Fluid dynamics":r"fluid dynamics|Navier.Stokes|Reynolds number|Bernoulli|vorticity|circulation",
"Thermodynamics":r"thermodynamic|Carnot|enthalpy|Gibbs free|Clausius",
"Electric fields":r"electric field|Gauss'?s law|Coulomb'?s law|Maxwell'?s equations|Faraday",
"Circuits":r"Kirchhoff|\bresistor|\bcapacitor|\binductor|Ohm'?s law|RLC",
"Nature & property of materials":r"crystal lattice|elastic modulus|alloy|polymer|phase diagram|dislocation|Bravais",
"Particle/aggregate to properties":r"granular|particle packing|aggregate (structure|strength)|percolation|homogeni[sz]ation|effective medium",
"Beltdraulic vs hydraulic":r"beltdraulic|belt drive|conveyor",
"Optics":r"\boptics\b|Snell|refractive index|diffraction|Fermat'?s principle|geometrical optics",
"Heat transfer":r"heat transfer|Fourier'?s law|thermal conductivity|heat equation|convective heat|Nusselt",
"Soil mechanics":r"soil mechanics|Mohr.Coulomb|effective stress|consolidation|bearing capacity|pore pressure|Terzaghi",
"Electronics":r"electronics|transistor|semiconductor|\bdiode|operational amplifier|op-amp",
}
skip=("node_modules","_to_delete","_archive","docs/","zenodo","-pt.html","/index","ml-evidence")
files=[f for f in glob.glob("**/*.html",recursive=True) if not any(x in f for x in skip) and not os.path.basename(f).startswith("index")]
print(f"prose pages scanned: {len(files)}")
txt={}
for f in files:
    s=open(f,errors="ignore").read()
    s=re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>"," ",s,flags=re.S|re.I)
    txt[f]=s
print("| topic | pages | hits | top pages |\n|---|---|---|---|")
for t,p in T.items():
    c={f:len(re.findall(p,s,re.I)) for f,s in txt.items()}
    c={f:n for f,n in c.items() if n}
    top=sorted(c.items(),key=lambda x:-x[1])[:3]
    print(f"| {t} | {len(c)} | {sum(c.values())} | "+"; ".join(f"{f} ({n})" for f,n in top)+" |")
named=["book7/ch-clapeyron-gibbs.html","book8/ch10-thermodynamics.html","ch-energy-entropy.html","book7/ch-maxwell.html","book7/ch-faraday.html","book4/ch-faraday.html","book4/ch16-crystal-lattice.html","book4/ch17-magnetic-lattice.html","book4/ch18-seismic-lattice.html","book4/ch19-acoustic-lattice.html","book4/ch20-defect-lattice.html","HVEH/ch-build-2river.html","HVEH/case-belleville-second-river.html","HVEH/cfd/README.md","HVEH/rotor_geometry.py","book7/ch-feynman.html","book7/wp59-dark-matter-lensing.html","book6/ch-phase.html","book7/ch-strang.html"]
miss=[n for n in named if not os.path.exists(n)]
print("\nnamed pages missing:",miss or "none")
sys.exit(1 if miss else 0)
