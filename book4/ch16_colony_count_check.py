"""ch16 check (2026-11-14), integers only.
Model = the expand operator as stated in DM3Bridge.lean conjunct (a):
  expand.cells = cells U biUnion (c in cells) {(h, c.stage+1) : h in hexNeighbors c.coord}
Cells carry a stage tag, so the SAME coordinate can occur at several stages.
Compares |cells| with |distinct coordinates| and with cHex(n)=1+3n(n+1).
NOTE: Colony.lean / colony_depth2_cells are not in this repo (only a July backup of DM3Bridge.lean); if the
real Colony.expand differs from conjunct (a), rerun against it. Exit 0 iff coordinate counts == cHex."""
import sys
D=[(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]
def expand(cells):
    new=set(cells)
    for q,r,s in cells:
        for dq,dr in D: new.add((q+dq,r+dr,s+1))
    return new
c={(0,0,0)}; ok=True
for n in range(5):
    coords={(q,r) for q,r,s in c}; ch=1+3*n*(n+1)
    print(f"depth {n}: cells(coord,stage)={len(c)}  distinct coords={len(coords)}  cHex={ch}")
    ok&=(len(coords)==ch); c=expand(c)
sys.exit(0 if ok else 1)
