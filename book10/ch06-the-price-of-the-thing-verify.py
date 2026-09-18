#!/usr/bin/env python3
"""
ch06-the-price-of-the-thing-verify.py

Book X asks what is held, by whom, and what reaches whom. This chapter asks
it of the simplest case there is: the cost of ending extreme poverty, which
is a number, and which is small.

All figures are [CITED]. The arithmetic on them is done here.

  UNU-WIDER (2024)   $70bn/yr closes the extreme-poverty gap for ~700 million
                     people at the $2.15/day line, in 2023 dollars; 0.1% of
                     OECD high-income GNI.
  OECD (2023)        ODA $224bn, of which $31bn was spent inside donor
                     countries on refugees, leaving $193bn.
  IFPRI / Ceres2030  ~$33bn/yr ADDITIONAL to end hunger sustainably by 2030.
  SIPRI (2025)       world military expenditure $2887bn, 2.5% of global GDP.

Run:  python3 book10/ch06-the-price-of-the-thing-verify.py
"""
FAIL = []
def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)
def show(label, val, unit=""):
    print("      %-52s %s%s" % (label, val, unit))

GAP     = 70e9        # UNU-WIDER, 2023 USD
PEOPLE  = 700e6
ODA     = 224e9
ODA_NET = 193e9
HUNGER  = 33e9        # IFPRI, additional per year
MIL     = 2887e9      # SIPRI 2025
MIL_PCT = 0.025
GDP     = MIL/MIL_PCT
OECD_HI_GNI = GAP/0.001   # implied by "0.1% of OECD high-income GNI"

head(1, "THE NUMBER, AND WHAT IT IS PER PERSON")
show("people in extreme poverty (<$2.15/day)", "%.0f million" % (PEOPLE/1e6))
show("annual cost to close the gap", "$%.0f bn" % (GAP/1e9))
show("per person per year", "$%.0f" % (GAP/PEOPLE))
show("per person per day", "$%.2f" % (GAP/PEOPLE/365))
show("per day, worldwide", "$%.0f million" % (GAP/365/1e6))
print()
print("  One hundred dollars a person a year. That is the whole of it, at the")
print("  line as the World Bank draws it, and it is the figure the rest of this")
print("  chapter is about.")
if abs(GAP/PEOPLE - 100) > 2: FAIL.append("per-person figure moved")

head(2, "AGAINST THINGS THAT ALREADY HAPPEN")
show("as a share of world GDP", "%.4f%%" % (100*GAP/GDP))
show("as a share of OECD high-income GNI", "%.2f%%" % (100*GAP/OECD_HI_GNI))
show("as a share of ODA already spent (gross)", "%.0f%%" % (100*GAP/ODA))
show("as a share of ODA net of in-donor refugee costs", "%.0f%%" % (100*GAP/ODA_NET))
show("world military spending / this figure", "%.0f x" % (MIL/GAP))
show("ending hunger sustainably, additional", "$%.0f bn/yr" % (HUNGER/1e9))
show("  the two together", "$%.0f bn/yr = %.0f%% of ODA"
     % ((GAP+HUNGER)/1e9, 100*(GAP+HUNGER)/ODA_NET))
print()
print("  The money is not merely findable. It is ALREADY BEING SPENT, on aid,")
print("  in an amount larger than the figure -- which is the fact this volume")
print("  is obliged to sit with, because it is not a financing problem and")
print("  therefore cannot be solved by finding money.")
ok = MIL/GAP > 30 and GAP < ODA_NET
print("  [%s] military spending exceeds it by more than 30x, and existing net"
      % ("SHOWN" if ok else "FAIL "))
print("        aid already exceeds it outright")
if not ok: FAIL.append("comparison arithmetic")

head(3, "THREE ANSWERS TO 'WHY DON'T WE', AND THEY ARE NOT COMPATIBLE")
for s in [
 "  A. WE DO NOT HAVE THE RESOURCES.",
 "     Refuted by §2. This is the only one of the three that the arithmetic",
 "     settles, and it settles it against.",
 "",
 "  B. WE HAVE THEM AND THE TRANSFER IS THE PROBLEM.",
 "     Moyo's argument, and the subject of ch03 of this volume: sustained",
 "     government-to-government transfers corrode the institutions they pass",
 "     through, so more of the same makes it worse. On this account the $70bn",
 "     is available, has largely been spent, and spending it again is not the",
 "     move.",
 "",
 "  C. WE HAVE THEM AND NOBODY MOVES FIRST.",
 "     A coordination account: the low-action state is a stable equilibrium",
 "     and stays stable however much accumulates beside it. Modelled in",
 "     book6/wp126-not-the-parameter.html, where the stuck equilibrium sits",
 "     under 1.2% of actors acting and the intervention that tips it is under",
 "     a fifth of the programme.",
 "",
 "  B AND C POINT OPPOSITE WAYS. B says the flow is the damage and should be",
 "  cut. C says the flow is too small and uncoordinated and should be tipped.",
 "  They cannot both be the main story, and this chapter does not adjudicate",
 "  between them -- see GAPS P3. What it does is refuse to let A stand in for",
 "  either, because A is the answer people reach for and it is the one that",
 "  is false.",
]: print(s)

head(4, "WHAT THE FIGURE IS NOT")
for s in [
 "  NOT THE COST OF ENDING POVERTY. It is the cost of closing the income gap",
 "  to a line, by transfer, for one year, assuming perfect targeting. UNU-",
 "  WIDER say so themselves: delivery and administration are on top.",
 "",
 "  NOT A ONE-OFF. It is per year, and it buys the line being crossed, not",
 "  the capacity to stay across it. Ending hunger SUSTAINABLY is the separate",
 "  $33bn, and that one is investment rather than transfer.",
 "",
 "  NOT APPLICABLE TO FAMINE. Acute famine today -- Sudan, Gaza, Yemen -- is",
 "  conflict famine, and its binding constraint is access. No transfer reaches",
 "  a besieged population, and a chapter that let a poverty figure stand in",
 "  for a famine figure would be making the same category error it accuses",
 "  others of in §3.",
 "",
 "  NOT A PLAN. It is a price. The distance between a price and a plan is",
 "  where this entire volume lives.",
]: print(s)

head("GAPS", "what this script does not establish")
for g in [
 "P1  EVERY FIGURE IS CITED. Nothing here is measured. The arithmetic is",
 "    checked; the inputs are taken on the authority of UNU-WIDER, OECD,",
 "    IFPRI and SIPRI, and the chapter is worth exactly what they are.",
 "",
 "P2  THE $2.15 LINE IS A CHOICE. It is the World Bank's extreme-poverty",
 "    line. At $3.65 or $6.85 the headcount and the cost are both several",
 "    times larger, and no figure for those is computed here.",
 "",
 "P3  B VERSUS C IS NOT ADJUDICATED. §3 sets out two incompatible accounts",
 "    and declines to choose. That is honest and it is also unfinished: the",
 "    evidence that would separate them exists, and reading it is the next",
 "    piece of work, not a gap that can be closed by argument.",
 "",
 "P4  PER-PERSON COST ASSUMES PERFECT TARGETING. $100/person/year is the",
 "    poverty gap divided by the headcount. Real transfer programmes reach",
 "    the wrong people and miss the right ones, and the literature on that",
 "    is not read here.",
 "",
 "P5  THE WORLD GDP FIGURE IS DERIVED, not sourced: SIPRI's $2887bn at 2.5%",
 "    of GDP, divided out. It is a division of two cited numbers.",
 "",
 "P6  NO TIME SERIES. Every figure is a snapshot between 2023 and 2025. The",
 "    headcount has moved a great deal in the last decade and this chapter",
 "    shows none of that movement.",
]:
    print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 6 gaps recorded above remain open.")
print("=" * 78)
