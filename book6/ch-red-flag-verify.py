#!/usr/bin/env python3
"""ch-red-flag-verify.py -- numbers in book6/ch-red-flag-warning-gap.html.

Arithmetic only; nothing here fetches data.
  1. C = Q/h dilution (Theorem 1 of WP39, fixed burden).
  2. PM2.5 AQI from concentration, with the EPA breakpoints in force after the 2024
     revision. Written from memory of the EPA Technical Assistance Document; NOT
     fetched in this session. Compare against the TAD before citing.
  3. The 16 Nov 2026 North Charleston screenshot pair: 57.2 ug/m3 and the AQI printed
     beside it (157). The script reports the difference instead of hiding it.
Run: python3 book6/ch-red-flag-verify.py
"""
import sys

ok = True
def check(name, cond, detail=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name + ((" -- " + detail) if detail else ""))
    ok = ok and cond

Q = 1.0
check("12x shallower layer gives 12x concentration",
      abs((Q / 50) / (Q / 600) - 12.0) < 1e-12, "600 m -> 50 m")

BP = [(0.0, 9.0, 0, 50), (9.1, 35.4, 51, 100), (35.5, 55.4, 101, 150),
      (55.5, 125.4, 151, 200), (125.5, 225.4, 201, 300), (225.5, 325.4, 301, 500)]
def aqi(c):
    c = int(c * 10) / 10.0
    for lo, hi, a, b in BP:
        if lo <= c <= hi:
            return round((b - a) / (hi - lo) * (c - lo) + a)
    raise ValueError(c)
check("AQI(9.0)=50", aqi(9.0) == 50)
check("AQI(35.4)=100", aqi(35.4) == 100)
check("AQI(55.4)=150", aqi(55.4) == 150)
check("AQI(55.5)=151, red starts here", aqi(55.5) == 151)
check("AQI(125.4)=200", aqi(125.4) == 200)
a = aqi(57.2)
check("57.2 ug/m3 is in the Unhealthy (red, 151-200) band", 151 <= a <= 200, "AQI=%d" % a)

shown = 157
print("INFO printed AQI beside 57.2 ug/m3 is %d; breakpoint formula gives %d (difference %d)." % (shown, a, shown - a))
print("INFO likely a NowCast-weighted AQI beside a raw concentration; NOT verified.")
check("both numbers are red-band", 151 <= shown <= 200 and 151 <= a <= 200)

print("\nALL PASS" if ok else "\nFAILED")
sys.exit(0 if ok else 1)
