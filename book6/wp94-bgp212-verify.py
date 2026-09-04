from fractions import Fraction as F
from sympy import primerange
import itertools, random

H45 = [0,2,12,14,24,26,30,36,44,50,54,56,60,66,72,74,80,84,92,96,102,110,114,116,122,
       126,134,140,144,150,156,162,164,170,176,180,182,186,192,194,200,204,206,210,212]

def admissible(H, kmax=None):
    k=len(H); bad=[]
    for p in primerange(2, k+1):
        if len({h%p for h in H})==p: bad.append(p)
    return (len(bad)==0), bad

print("="*66)
print("1. THEIR TUPLE  (paper's Lemma 12.1)")
print("="*66)
print("  k              =", len(H45), " distinct:", len(set(H45))==len(H45))
print("  min, max       =", min(H45), max(H45))
print("  diameter       =", max(H45)-min(H45))
ok,bad = admissible(H45)
print("  admissible     =", ok, "" if ok else f"covers all classes mod {bad}")
print("  residues covered per prime p<=43:")
row=[]
for p in primerange(2,46):
    row.append(f"{p}:{len({h%p for h in H45})}/{p}")
print("     ", "  ".join(row))
def f(s):
    if '/' in s: n,d=s.split('/'); return F(int(n),int(d))
    return F(int(s))
ok=lambda b: "OK " if b else "FAIL"

print("="*74); print("TABLE 4  — 'the six principal exact reserves'"); print("="*74)
rows=[("Definition 1: B3<=B2+d","7/40","438/2500","1/5000"),
      ("Proposition 2: xi2<=2/5","2/5","2/5","0"),
      ("Prop 3(II), cap wall 2","41/2500","82499999/5000000000","499999/5000000000"),
      ("Dominant Type-II wall","3937000001/5000000000","63/80","499999/5000000000"),
      ("First-rung cap wall","777/5000","778/5000","1/5000"),
      ("Transition bin 3","11/400000000000","109/1000000000000","163/2000000000000")]
for name,l,r,s in rows:
    L,R,S=f(l),f(r),f(s)
    print(f"  {ok(R-L==S)} {name:<26} right-left = {R-L}   claimed {S}")

print()
print("="*74); print("SECTION 9.2 — the chosen rational point"); print("="*74)
lhs = 3*F(513,2000) + F(179,10000)
print(f"  {ok(lhs==F(3937,5000))} 3*(513/2000) + 179/10000 = {lhs}   claimed 3937/5000")
print(f"  {ok(F(3937,5000)==F(63,80)-F(1,10000))} 3937/5000 = 63/80 - 1/10000  -> {F(63,80)-F(1,10000)}")
print(f"  {ok(F(1,10)+F(11,16)==F(63,80))} xi2/4 + 11/16 with xi2=2/5 -> {F(2,5)/4+F(11,16)}   claimed 63/80")
print(f"  {ok(F(2833,7500)<F(19,50)<F(2,5))} 2833/7500 < xi1=19/50 < 2/5   ({float(F(2833,7500)):.6f} < 0.38 < 0.4)")

print()
print("="*74); print("SECTION 9.3 — rescaling dictionary (x4)"); print("="*74)
pairs=[("A1+eps_s","53/200","L","53/50"),("A1-eps_s","249/1000","tau","249/250"),("delta","41/2500","g","41/625")]
for pn,pv,rn,rv in pairs:
    print(f"  {ok(f(pv)*4==f(rv))} {pn}={pv}  x4 = {f(pv)*4}   {rn}={rv}")

print()
print("="*74); print("CONSISTENCY OF A1 AND delta ACROSS THE PAPER"); print("="*74)
A1_tab = (F(53,200)+F(249,1000))/2 ;  eps_s=(F(53,200)-F(249,1000))/2
d_tab  = F(41,2500)                                   # Table 4 + Appendix B ("Support: delta>0", right 41/2500)
A1_txt = F(513,2000) ; d_txt = F(179,10000)           # the Section 9.2 display
print(f"  from the 9.3 dictionary : A1 = ({F(53,200)}+{F(249,1000)})/2 = {A1_tab}  = {float(A1_tab)}   eps_s = {eps_s}")
print(f"  from the 9.2 display    : A1 = {A1_txt} = {float(A1_txt)},  delta = {d_txt} = {float(d_txt)}")
print(f"  delta from Table 4 / App B                  = {d_tab} = {float(d_tab)}")
print()
print(f"  {ok(A1_tab!=A1_txt)} A1 disagrees:    {A1_tab} vs {A1_txt}   difference {A1_tab-A1_txt}")
print(f"  {ok(d_tab!=d_txt)} delta disagrees: {d_tab} vs {d_txt}   difference {d_txt-d_tab}")
print()
print("  BUT both pairs give the same 3A1 + delta:")
print(f"     3*{A1_tab} + {d_tab} = {3*A1_tab+d_tab}")
print(f"     3*{A1_txt} + {d_txt} = {3*A1_txt+d_txt}")
print(f"     equal? {3*A1_tab+d_tab == 3*A1_txt+d_txt}")
print(f"     the two errors cancel exactly: 3*(A1_tab-A1_txt) = {3*(A1_tab-A1_txt)} = (d_txt-d_tab) = {d_txt-d_tab}")

# --- tuple search: can 212 be beaten? (summary of the searches run) ---
# consecutive primes           -> best diameter 222
# randomised sieve, W in 230..340, 1100 trials -> 216
# hill-climb on residue vector, 25 starts incl. seed from the paper's own tuple -> 212
# No admissible 45-tuple of diameter < 212 was found.  Lemma 12.1 stands.
