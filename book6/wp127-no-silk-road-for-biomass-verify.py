#!/usr/bin/env python3
"""
wp127-no-silk-road-for-biomass-verify.py

A global network of scattered smallholder co-ops, connected to a highway --
a Silk Road for feedstock. This paper says why that particular shape cannot
work, and what shape does, and it is arithmetic rather than opinion.

THE CLAIM: the Silk Road carried silk because silk's break-even haul is about
750,000 km. Date palm residue's is 188 km. You cannot build a Silk Road out
of a material that cannot afford to travel.

WHAT FOLLOWS is the structure G6's own two briefs already have: cashew apple
in Brazil, date palm residue in Saudi Arabia, the SAME process chemistry and
DIFFERENT local feedstock. The network is real, and what travels along it is
the method, not the material.

  A. Value density and break-even haul, nine goods.
  B. Densification: what a first-stage node actually buys.
  C. A plant-scale model -- and an honest negative result: for cashew apple
     at plausible densities, transport does NOT limit plant size. The
     resource does. The textbook biomass-radius story does not bind here and
     this script says so rather than forcing it.
  D. The TBFCo date palm brief's arithmetic, checked, with the yield band
     made explicit rather than buried.

Run:  python3 book6/wp127-no-silk-road-for-biomass-verify.py
"""
import math
FAIL = []
def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)

CT = 0.08     # USD per tonne-km, rural road freight. Order of magnitude; see GAPS.

# ---------------------------------------------------------------------------
head(1, "WHY THE SILK ROAD CARRIED SILK")
# ---------------------------------------------------------------------------
GOODS = [("saffron", 3_000_000), ("silk", 60_000), ("black pepper", 6_000),
         ("SAF (jet fuel)", 1_800), ("palm oil", 1_000), ("ethanol", 600),
         ("wood pellets", 180), ("cashew apple (fresh)", 25),
         ("date palm residue (dry)", 15)]
print("  Freight at $%.2f per tonne-km. 'Break-even' is the haul at which" % CT)
print("  freight equals the whole value of the cargo.")
print()
print("      %-26s %10s %16s %16s" % ("good", "$/tonne", "freight/1000km", "break-even km"))
for n, v in GOODS:
    print("      %-26s %10.0f %15.1f%% %16.0f" % (n, v, 100*CT*1000/v, v/CT))
print()
silk = 60_000; palm = 15; caju = 25
print("      silk : cashew apple      %.0f x" % (silk/caju))
print("      silk : date palm residue %.0f x" % (silk/palm))
print()
print("  Silk can be carried eighteen times around the Earth before freight")
print("  eats it. Date palm residue makes it 188 km. That is the whole")
print("  argument: THE SILK ROAD IS A SHAPE THAT ONLY HIGH VALUE DENSITY CAN")
print("  AFFORD, and biomass is the defining case of the opposite.")
ok = (silk/CT) > 500_000 and (palm/CT) < 300
print("  [%s] silk break-even > 500,000 km and residue break-even < 300 km"
      % ("SHOWN" if ok else "FAIL "))
if not ok: FAIL.append("break-even comparison")

# ---------------------------------------------------------------------------
head(2, "SO WHAT TRAVELS INSTEAD -- densification, measured")
# ---------------------------------------------------------------------------
JUICE, SUGAR, YIELD = 0.85, 0.11, 0.48    # juice fraction; sugar in juice; ethanol from sugar
et_kg = 1000*JUICE*SUGAR*YIELD
v_apple, v_etoh = 25.0, 0.60*et_kg
print("  One tonne of fresh cashew apple, juiced and fermented on site:")
print("      ethanol out            %.0f kg      (mass ratio %.0f : 1)" % (et_kg, 1000/et_kg))
print("      value in / value out   $%.2f / $%.2f   (%.0f%% retained)"
      % (v_apple, v_etoh, 100*v_etoh/v_apple))
print("      freight per $ of value falls by %.0f x" % ((1000/et_kg)*(v_apple/v_etoh)))
print()
print("      break-even haul, fresh apple     %4.0f km" % (v_apple/CT))
print("      break-even haul, ethanol         %4.0f km" % (600/CT))
print()
print("  A first-stage node turns a 312 km commodity into a 7500 km one, at")
print("  no loss of value. THAT is how the highway is reached -- not by")
print("  hauling feedstock to the road, but by making something road-worthy")
print("  where the feedstock already is.")
ratio = (1000/et_kg)*(v_apple/v_etoh)
print("  [%s] densification improves freight-per-value by more than 10x"
      % ("SHOWN" if ratio > 10 else "FAIL "))
if ratio <= 10: FAIL.append("densification ratio")

# ---------------------------------------------------------------------------
head(3, "AN HONEST NEGATIVE RESULT -- transport is not what limits plant size")
# ---------------------------------------------------------------------------
RHO, TAU, CRF = 150.0, 1.4, 0.147      # t/km2/yr collectable; road tortuosity; 12% / 15 yr
C0, Q0, SC = 40e6, 100_000.0, 0.65     # capital $ at reference throughput; six-tenths rule
def cost(Q):
    cap = C0*(Q/Q0)**SC*CRF/Q
    r = math.sqrt(Q/(math.pi*RHO))
    return cap + CT*(2/3)*r*TAU, cap, CT*(2/3)*r*TAU, r
print("  The textbook story: plant capital scales as Q^0.65 but the collection")
print("  radius grows as sqrt(Q), so total cost has a minimum and biorefineries")
print("  are therefore small. Tested, with cashew-apple densities:")
print()
print("      %-12s %10s %10s %12s %10s" % ("Q t/yr", "$/t total", "capital", "transport", "radius km"))
for q in (20e3, 100e3, 400e3, 1.6e6, 5e6):
    t, c, tr, r = cost(q)
    print("      %-12.0f %10.2f %10.2f %12.2f %10.1f" % (q, t, c, tr, r))
print()
print("  There is no interior minimum. Cost falls monotonically to the edge of")
print("  the resource: at 5 Mt/yr the radius is 103 km and transport is still")
print("  only %.0f%% of cost." % (100*cost(5e6)[2]/cost(5e6)[0]))
print()
print("  So the famous biomass-radius result DOES NOT BIND HERE, and this")
print("  paper will not pretend it does. With these parameters the binding")
print("  constraints are elsewhere:")
print("      - how much feedstock actually exists inside any radius, and")
print("      - PERISHABILITY. Cashew apple ferments within a day or two, so")
print("        its radius is set by hours, not by dollars, and no freight")
print("        rate enters the calculation at all.")
mono = cost(5e6)[0] < cost(1.6e6)[0] < cost(400e3)[0]
print("  [%s] cost is monotone decreasing in Q over the tested range"
      % ("SHOWN" if mono else "FAIL "))
if not mono: FAIL.append("scale behaviour changed")
for hrs in (4, 8, 12):
    print("      perishability radius at %2dh, 45 km/h, tortuosity %.1f:  %3.0f km"
          % (hrs, TAU, hrs*45/TAU))

# ---------------------------------------------------------------------------
head(4, "THE DATE PALM BRIEF, ARITHMETIC CHECKED")
# ---------------------------------------------------------------------------
TREES, KG_TREE = 32e6, 20.0
res = TREES*KG_TREE/1000
print("  TBFCo brief (G6, September 2026) states 32 million date palms in the")
print("  Kingdom at roughly 20 kg/yr of surface fibre, fronds and seeds each.")
print()
print("      residue                      %6.0f kt/yr" % (res/1000))
print()
print("  Converted to SAF by a lignocellulosic route. The mass yield is the")
print("  single softest number, so it is shown as a BAND and never as a point:")
print()
print("      %-16s %-14s %-18s" % ("mass yield", "SAF kt/yr", "million L/yr"))
B100 = 36.0
for y, lbl in ((0.12, "conservative"), (0.175, "mid"), (0.22, "optimistic")):
    saf = res*y; L = saf*1000/0.80/1e6
    print("      %-16s %-14.0f %-18.0f" % ("%.0f%% (%s)" % (100*y, lbl), saf/1000, L))
mid = res*0.175*1000/0.80/1e6
print()
print("      TBFCo's stated B100 target   %6.0f million L/yr" % B100)
print("      date palm track at mid yield %6.0f million L/yr = %.1fx that volume"
      % (mid, mid/B100))
print()
print("  The brief's framing survives its own arithmetic: the residue stream is")
print("  the same order as the existing business and plausibly several times")
print("  it. What the brief should NOT say is a single litre figure, because")
print("  the conservative and optimistic ends differ by %.1fx." % (0.22/0.12))
ok = 1.5 < mid/B100 < 8
print("  [%s] mid-yield estimate is a small multiple of current volume"
      % ("SHOWN" if ok else "FAIL "))
if not ok: FAIL.append("date palm multiple out of range")

# ---------------------------------------------------------------------------
head(5, "WHAT THE NETWORK IS FOR")
# ---------------------------------------------------------------------------
for s in [
 "  Sections 1-3 say the material cannot travel. Section 4 says the resource",
 "  is real and local. Put those together and the scattered-co-op network is",
 "  not a logistics network, because there is nothing to haul along it.",
 "",
 "  IATA's global feedstock assessment says the same thing from the other",
 "  end: feedstock is regionally determined -- agricultural residues in North",
 "  America, sugar and starch in Brazil, over 80% of the world's palm oil in",
 "  ASEAN, rice and wheat residues in India and China -- and smallholders",
 "  'lack resources, incentives, or organizational structures necessary to",
 "  participate in formal biomass markets', needing intermediary hubs and",
 "  cooperative models. [CITED]",
 "",
 "  So the network carries the METHOD, not the material: process, catalyst,",
 "  specification, certification, offtake contracts and the certification",
 "  chain that lets a litre made in Ceara and a litre made in Al-Ahsa satisfy",
 "  the same CORSIA obligation. That is a licensing and standards network",
 "  with local conversion at every node.",
 "",
 "  G6's own two briefs are already built that way -- cashew apple in Brazil",
 "  and date palm residue in Saudi Arabia, same chemistry class, different",
 "  local feedstock. The paper's contribution is only to say WHY that is the",
 "  right shape, in numbers, so that the next node can be chosen rather than",
 "  found.",
]: print(s)

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
for g in [
 "Q1  EVERY PRICE IS AN ORDER OF MAGNITUDE. The nine values in section 1 are",
 "    representative figures, not quotes from any market on any date. The",
 "    RATIOS are robust to being wrong by a factor of two; the break-even",
 "    distances are not, and should be read as one significant figure.",
 "",
 "Q2  ONE FREIGHT RATE FOR EVERYTHING. $0.08/tonne-km is applied to saffron",
 "    and to wet biomass alike. Real freight is mode-dependent and bulk wet",
 "    material is worse than the flat rate suggests, which strengthens the",
 "    conclusion and is still not modelled.",
 "",
 "Q3  THE CASHEW CONVERSION CHAIN IS ASSUMED. 85% juice, 11% sugars, 48%",
 "    ethanol from sugar are textbook values, not measurements from G6's own",
 "    process, and the 108% value retention in section 2 is therefore a",
 "    coincidence of two rough numbers rather than a finding.",
 "",
 "Q4  SECTION 3'S PLANT MODEL IS A TOY. Two cost terms, no labour, no",
 "    storage, no seasonality -- cashew apple is harvested over a few months,",
 "    which alone could dominate the whole scale question and is absent.",
 "",
 "Q5  THE DATE PALM YIELD BAND IS NOT SOURCED. 12-22% mass yield to SAF is a",
 "    plausible range for lignocellulosic routes and no specific study of",
 "    date palm residue was consulted. The brief cites a 2026 UAE pyrolysis",
 "    study for FEASIBILITY, which is not the same as a yield.",
 "",
 "Q6  32 MILLION TREES AT 20 kg IS THE BRIEF'S OWN FIGURE, carried through",
 "    unchecked. If either number is wrong everything in section 4 moves",
 "    proportionally, and neither was verified against a Saudi agricultural",
 "    census here.",
 "",
 "Q7  NO SUSTAINABILITY OR ILUC ACCOUNTING. Oil-palm-based SAF is restricted",
 "    under EU rules on land-use-change grounds. Nothing here addresses",
 "    whether any pathway discussed would certify under CORSIA, ReFuelEU or",
 "    RenovaBio, and that is a gating question, not a detail.",
]: print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 7 gaps recorded above remain open.")
print("=" * 78)
