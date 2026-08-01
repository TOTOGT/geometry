#!/usr/bin/env python3
"""
rotor_geometry.py — HVEH Second River Pilot · Helical Rotor Point Cloud
Contact-geometric blade surface from α = dz − r²dθ

Author : Pablo Nogueira Grossi · G6 LLC · Newark NJ · 2026
Repo   : github.com/TOTOGT/AXLE
DOI    : 10.5281/zenodo.19117400

Blade geometry
--------------
Active zone    : r* ≤ r ≤ 1.0  (normalised)   r* = 0.77594059
Core zone      : 0 ≤ r < r*    — no blades (vortex stability, Rankine core)
Pitch equation : tan φ(r) = r   (annihilates contact form α = dz − r²dθ at each r)
Chord scaling  : C(r) = C_tip × R_outer / r   (wider inward, constant solidity)
Profile        : NACA 0012 symmetric  (zero camber → no axial lift component)

Physical parameters (Second River, Belleville NJ — 1.2 m diameter unit)
------------------------------------------------------------------------
R_outer  = 0.60 m    outer blade radius  (rotor diameter 1.2 m)
L_axial  = 0.90 m    axial span at tip   (θ_sweep = π rad, 180° helical arc)
C_tip    = 0.06 m    chord at r = 1.0  (10 % of outer radius)
t_ratio  = 0.12      NACA 0012 thickness ratio
n_blades = 3         blade count, 120° stagger

Axial scale relation
--------------------
Z_physical = r² × θ × R_z      (integrates the contact condition dz = r² dθ)
R_z = L_axial / θ_sweep = 0.9 / π  ≈  0.2865 m/rad

At r* = 0.77594059: Z_inner = r*² × π × R_z  ≈  0.542 m
At r  = 1.00 : Z_outer =    1² × π × R_z   =  0.900 m

CFD validation criteria (Phase 2 pass gates)
-------------------------------------------
  1.  T_z · ω / (F_z · U_z)  >>  1     (torque dominates over thrust)
  2.  Tangential velocity collapses to near-zero for r* ≤ r ≤ 1.0 downstream
  3.  No vortex core breakdown at r < r*      (Rankine core stays coherent)

Hardware (Phase 3)
------------------
  Material : 5083 aluminium or CFRP laminate
  Shroud   : outer ring or neutral-profile struts (no central cantilever)
  CAM      : G³ NURBS surface fitted to this cloud → STEP export for 5-axis mill

Usage
-----
  python rotor_geometry.py [output_path]

  Default output: rotor_cloud.csv in the same directory as this script.
  Import into FreeCAD → Surface Workbench → Filling / BSpline Surface,
  then export .STEP for HAAS/Mazak 5-axis CAM.
"""

import numpy as np
import csv
import os
import sys

# ── Physical parameters ───────────────────────────────────────────────────────
R_OUTER     = 0.60          # m  outer blade radius
R_STAR      = 0.77594059    # normalised inner boundary (certified: certify_rstar.py, DOP853)
N_BLADES    = 3
THETA_SWEEP = np.pi         # rad  180° helical sweep per blade
L_AXIAL     = 0.90          # m  desired axial span at outer tip
C_TIP       = 0.06          # m  chord length at r = 1.0
T_RATIO     = 0.12          # NACA 4-digit thickness ratio → 0012

# Axial scale:  Z = r² × θ × R_z;  at r=1, θ=THETA_SWEEP → Z = L_AXIAL
R_Z = L_AXIAL / THETA_SWEEP         # ≈ 0.2865 m/rad

# ── Resolution ────────────────────────────────────────────────────────────────
N_RADIAL = 32       # radial stations r* → 1.0
N_THETA  = 64       # angular stations along helical sweep
N_CHORD  = 21       # chord stations per profile (0=LE … 1=TE)

# ── NACA 4-digit half-thickness ───────────────────────────────────────────────
def naca_ht(x: np.ndarray, t: float = 0.12) -> np.ndarray:
    """
    Half-thickness y_t at normalised chord station x ∈ [0, 1].
    NACA 4-digit formula (closed trailing edge variant).
    """
    return (t / 0.20) * (
        0.2969 * np.sqrt(np.maximum(x, 0.0))
      - 0.1260 * x
      - 0.3516 * x ** 2
      + 0.2843 * x ** 3
      - 0.1015 * x ** 4
    )


# ── Blade point cloud ─────────────────────────────────────────────────────────
def blade_points(blade_k: int) -> np.ndarray:
    """
    Generate surface points for blade k  (k = 0, 1, 2).

    Returns ndarray of shape (M, 7):
        col 0-2 : x, y, z  in physical metres
        col   3 : blade index
        col   4 : normalised radius r_n
        col   5 : normalised chord position x_c  (0 = LE, 1 = TE)
        col   6 : surface side  (+1 = suction / upper,  -1 = pressure / lower)
    """
    theta_offset = 2.0 * np.pi * blade_k / N_BLADES

    r_vals  = np.linspace(R_STAR, 1.0, N_RADIAL)
    th_vals = np.linspace(0.0, THETA_SWEEP, N_THETA)
    x_chord = np.linspace(0.0, 1.0, N_CHORD)
    ht_norm = naca_ht(x_chord, T_RATIO)         # normalised half-thickness

    pts = []

    for r_n in r_vals:
        rho   = r_n * R_OUTER                   # physical radius [m]
        chord = C_TIP / r_n                      # physical chord [m]  (1/r scaling; C_TIP is physical at r=1)
        ht    = ht_norm * chord                  # physical half-thickness vector [m]

        for th in th_vals:
            theta = th + theta_offset

            # ── Centerline on the contact-integral manifold ───────────────
            # z_cl = r² × θ × R_z   (integrates dz = r² dθ)
            z_cl = r_n ** 2 * theta * R_Z
            x_cl = rho * np.cos(theta)
            y_cl = rho * np.sin(theta)

            # ── Helix tangent t̂  (∂/∂θ of centerline, normalised) ─────────
            tx = -rho * np.sin(theta)
            ty =  rho * np.cos(theta)
            tz =  r_n ** 2 * R_Z
            t_len = np.sqrt(tx * tx + ty * ty + tz * tz)
            tx /= t_len;  ty /= t_len;  tz /= t_len

            # ── Outward radial unit vector n̂_r ────────────────────────────
            nr = np.array([np.cos(theta), np.sin(theta), 0.0])

            # ── Blade normal n̂ = t̂ × n̂_r  (thickness direction) ──────────
            t_vec = np.array([tx, ty, tz])
            n_vec = np.cross(t_vec, nr)
            n_len = np.linalg.norm(n_vec)
            if n_len < 1e-12:
                continue
            n_vec /= n_len

            # ── NACA profile at this (r, θ) station ───────────────────────
            # Chord runs along t̂; midchord at (x_cl, y_cl, z_cl)
            # x_c = 0 → leading edge;  x_c = 1 → trailing edge
            cl = np.array([x_cl, y_cl, z_cl])
            for i, xc in enumerate(x_chord):
                shift = (xc - 0.5) * chord          # displacement from midchord
                base  = cl + shift * t_vec
                for side in (+1, -1):
                    pt = base + side * ht[i] * n_vec
                    pts.append([pt[0], pt[1], pt[2],
                                blade_k, r_n, xc, side])

    return np.array(pts)


# ── Summary output ────────────────────────────────────────────────────────────
def print_summary(pts: np.ndarray) -> None:
    z_inner = R_STAR ** 2 * THETA_SWEEP * R_Z
    z_outer = 1.0    ** 2 * THETA_SWEEP * R_Z

    print()
    print("  HVEH Second River · Contact-Geometric Helical Rotor")
    print("  " + "─" * 50)
    print(f"  Blades           : {N_BLADES} × 120° stagger")
    print(f"  Outer diameter   : {2*R_OUTER*1000:.0f} mm  (R_outer = {R_OUTER*1000:.0f} mm)")
    print(f"  Core boundary    : r* = {R_STAR}  → ρ* = {R_STAR*R_OUTER*1000:.1f} mm")
    print(f"  Blade pitch r*   : φ(r*) = arctan({R_STAR}) = {np.degrees(np.arctan(R_STAR)):.2f}°")
    print(f"  Blade pitch tip  : φ(1)  = arctan(1)  = 45.00°")
    print(f"  Axial span tip   : {z_outer*1000:.1f} mm  (θ_sweep = 180°)")
    print(f"  Axial span r*    : {z_inner*1000:.1f} mm")
    print(f"  Chord at tip     : {C_TIP*1000:.0f} mm")
    print(f"  Chord at r*      : {C_TIP/R_STAR*1000:.1f} mm")
    print(f"  Profile          : NACA 00{int(T_RATIO*100):02d}  (t/c = {T_RATIO:.0%}, zero camber)")
    print(f"  Axial scale R_z  : {R_Z*1000:.2f} mm/rad")
    print(f"  Total points     : {len(pts):,}")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    out_path = sys.argv[1] if len(sys.argv) > 1 else \
               os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'rotor_cloud.csv')

    print("Generating contact-geometric rotor surface...")

    all_pts = []
    for k in range(N_BLADES):
        bp = blade_points(k)
        all_pts.append(bp)
        print(f"  blade {k}  (θ-offset {np.degrees(2*np.pi*k/N_BLADES):.0f}°) "
              f"→ {len(bp):,} surface points")

    pts = np.vstack(all_pts)
    print_summary(pts)

    with open(out_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['x_m', 'y_m', 'z_m', 'blade', 'r_norm', 'x_chord', 'side'])
        for row in pts:
            w.writerow([
                f'{row[0]:.6f}', f'{row[1]:.6f}', f'{row[2]:.6f}',
                int(row[3]), f'{row[4]:.4f}', f'{row[5]:.4f}', int(row[6])
            ])

    print(f"  Saved → {out_path}")
    print()
    print("  Next step: FreeCAD → Surface Workbench → BSpline Surface")
    print("  Fit G³-continuous NURBS surface to each blade's point cloud.")
    print("  Export as .STEP for 5-axis CAM (HAAS VF series or Mazak Variaxis).")
    print()
    print("  CFD pass gates before fabrication:")
    print("    1. T_z·ω / (F_z·U_z) >> 1   (torque dominates over thrust)")
    print("    2. V_θ → 0 downstream in active zone  (energy extracted)")
    print("    3. No vortex core breakdown for r < r*  (Rankine core stable)")


if __name__ == '__main__':
    main()
