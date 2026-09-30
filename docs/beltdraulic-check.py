#!/usr/bin/env python3
"""Arithmetic checks on published Beltdraulic (RISE Robotics) claims. Inputs are the vendor/partner figures as quoted in
docs/engineering-coverage-map.md sec. 5; nothing here tests the device. Sources: Machine Design 2026-02-10 (Grodzki, Turntide);
BusinessWire 2022-12-22 (US 11,255,416)."""
psi=6894.757
p=1400*psi
print(f"1,400 psi = {p/1e6:.2f} MPa (belt-pulley interface pressure, quoted as 'in excess of')")
# energy ratio implied by the two efficiencies quoted
eh,eb=0.211,0.85
saving=1-eh/eb
print(f"hydraulic 21.1% vs belt 85% -> energy for same work: {eh/eb:.3f} of hydraulic = {saving*100:.1f}% less")
need=0.85*(1-0.90)
print(f"'up to 90% less energy' at 85% belt efficiency needs hydraulic efficiency <= {need*100:.1f}% ")
# block and tackle: N supporting strands, ideal
for N in (2,4,6,8):
    print(f"N={N}: force x{N}, speed /{N}, ideal power unchanged; at 85% eff output = {0.85:.2f} x input")
# 2-ton cylinder force
F=2*2000*4.4482
print(f"2 short tons-force = {F/1000:.2f} kN; 2 metric tonnes-force = {2000*9.80665/1000:.2f} kN (unit not stated in source)")
assert abs(saving-0.7519)<0.001
