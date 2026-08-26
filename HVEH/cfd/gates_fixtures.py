#!/usr/bin/env python3
"""
gates_fixtures.py — proof that gates.py rejects.

A gate that has never rejected anything is not known to work. Each case below
has a verdict decided by hand, and the file asserts gates.py agrees.

The cases that matter most are the last three. They are not "bad designs" --
they are shapes in which a naive checker returns a clean answer while having
established nothing:

  · every field missing        -> three ERRORs and zero FAILs. A caller
                                  watching for "FAIL" sees none and calls it
                                  clean. gates.py returns INCOMPLETE.
  · axial power exactly zero   -> the ratio is undefined, and an undefined
                                  ratio reported as infinite becomes a
                                  headline number. gates.py refuses it.
  · upstream swirl zero        -> nothing to extract, so extraction cannot be
                                  scored. A ratio of 0/0 is not a pass.

Run:  python3 gates_fixtures.py
"""

import sys
import gates

CASES = [
    # label, case dict, expected (all_pass, n_evaluated, n_errors)
    ("clean design", {
        "torque_Nm": 40.0, "omega_rad_s": 12.0,
        "axial_force_N": 30.0, "U_axial_m_s": 0.8,
        "V_theta_upstream_m_s": 0.50, "V_theta_downstream_m_s": 0.10,
        "U_axial_core_min_normalised": 0.35,
    }, (True, 3, 0)),

    ("axial-momentum machine (an H-rotor in disguise)", {
        "torque_Nm": 4.0, "omega_rad_s": 3.0,
        "axial_force_N": 60.0, "U_axial_m_s": 0.9,
        "V_theta_upstream_m_s": 0.50, "V_theta_downstream_m_s": 0.12,
        "U_axial_core_min_normalised": 0.30,
    }, (False, 3, 0)),

    ("spins but extracts nothing (a flow meter)", {
        "torque_Nm": 40.0, "omega_rad_s": 12.0,
        "axial_force_N": 30.0, "U_axial_m_s": 0.8,
        "V_theta_upstream_m_s": 0.50, "V_theta_downstream_m_s": 0.48,
        "U_axial_core_min_normalised": 0.35,
    }, (False, 3, 0)),

    ("vortex breakdown: axial reversal in the core", {
        "torque_Nm": 40.0, "omega_rad_s": 12.0,
        "axial_force_N": 30.0, "U_axial_m_s": 0.8,
        "V_theta_upstream_m_s": 0.50, "V_theta_downstream_m_s": 0.10,
        "U_axial_core_min_normalised": -0.02,
    }, (False, 3, 0)),

    ("marginal core, positive but under the margin", {
        "torque_Nm": 40.0, "omega_rad_s": 12.0,
        "axial_force_N": 30.0, "U_axial_m_s": 0.8,
        "V_theta_upstream_m_s": 0.50, "V_theta_downstream_m_s": 0.10,
        "U_axial_core_min_normalised": 0.01,
    }, (False, 3, 0)),

    ("SILENT-PASS TRAP: no data at all", {}, (None, 0, 3)),

    ("SILENT-PASS TRAP: axial power exactly zero", {
        "torque_Nm": 40.0, "omega_rad_s": 12.0,
        "axial_force_N": 0.0, "U_axial_m_s": 0.8,
        "V_theta_upstream_m_s": 0.50, "V_theta_downstream_m_s": 0.10,
        "U_axial_core_min_normalised": 0.35,
    }, (None, 2, 1)),

    ("SILENT-PASS TRAP: no upstream swirl to extract", {
        "torque_Nm": 40.0, "omega_rad_s": 12.0,
        "axial_force_N": 30.0, "U_axial_m_s": 0.8,
        "V_theta_upstream_m_s": 0.0, "V_theta_downstream_m_s": 0.0,
        "U_axial_core_min_normalised": 0.35,
    }, (None, 2, 1)),
]


def main():
    width = max(len(c[0]) for c in CASES)
    failures = 0
    for label, case, (want_pass, want_eval, want_err) in CASES:
        results, errors, _ = gates.evaluate(case)
        got_eval, got_err = len(results), len(errors)
        got_pass = all(r["pass"] for r in results) if got_eval == len(gates.GATES) else None
        ok = (got_pass == want_pass and got_eval == want_eval and got_err == want_err)
        failures += not ok
        print("%-*s  %s   evaluated=%d errors=%d verdict=%s"
              % (width, label, "PASS" if ok else "**MISMATCH**",
                 got_eval, got_err,
                 {True: "pass", False: "fail", None: "incomplete"}[got_pass]))
        if not ok:
            print("      expected evaluated=%d errors=%d verdict=%s"
                  % (want_eval, want_err,
                     {True: "pass", False: "fail", None: "incomplete"}[want_pass]))

    print()
    print("%d/%d cases behave as specified" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
