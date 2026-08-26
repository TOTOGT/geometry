#!/usr/bin/env python3
"""
gates.py — the three CFD acceptance criteria for the HVEH helical rotor.

These are not new. `rotor_geometry.py` already prints them as the conditions a
CFD pass must establish before fabrication, and ch-build-2river.html §8 calls
that pass the critical-path item. This file turns three printed sentences into
three computable verdicts, so a candidate geometry can be scored automatically
instead of judged by eye.

    1. torque_dominance   T_z·ω / (F_z·U_z) >> 1
       The rotor must extract ROTATIONAL kinetic energy, not axial momentum.
       This is the gate that distinguishes an HVEH rotor from an off-shelf
       Darrieus or H-rotor. ch-build-2river §8: installing an H-rotor at the
       confluence "is equivalent to the F-before-K error: you get turbulence,
       not a coherent vortex, and zero net generation."

    2. swirl_extraction   V_theta -> 0 downstream, in the active annulus
       Energy actually leaves the flow. A rotor that spins while the swirl
       passes through unchanged is a flow meter, not a generator.

    3. core_stability     no vortex breakdown for r < r*
       The Rankine core must survive. r* = 0.77594059 is where the blades
       start; inside it there are none, by design.

WHAT A THRESHOLD IS HERE
------------------------
Every threshold below is an ENGINEERING CHOICE, not a derived constant. ">> 1"
is not a number. The defaults are stated, their justification is one line
each, and they are overridable. Do not let a default acquire the status of a
result: the corpus has already had to withdraw one claim (`g6_equals_schumann`)
whose two sides were both `def := 33`, and one (`basin_asymmetry`) reported as
machine-checking a physical prediction when it compared two rationals.

WHAT THIS FILE DOES NOT DO
--------------------------
It does not run CFD, and it does not validate the solver. It reads quantities
someone else extracted and applies criteria to them. Feed it wrong numbers and
it will pass wrong numbers. The extraction step is deliberately separate so it
can be swapped without touching the criteria -- and so a change to either is
visible in the diff of exactly one file.

It also says nothing about cavitation, fatigue, debris strike, bearing loads or
biofouling. A hydrokinetic rotor in an urban river fails in ways a CFD pass
cannot see. Passing all three gates means the hydrodynamics are worth taking to
a flume, not that the machine works.

Usage
-----
    python3 gates.py case.json
    python3 gates.py case.json --json report.json
"""

import argparse
import json
import sys

R_STAR = 0.77594059          # normalised; blades occupy r* <= r <= 1

DEFAULTS = {
    # Ratio of rotational power extracted to axial-thrust power. 5.0 is the
    # working reading of ">> 1": an order of magnitude is the ambition, 5 is
    # the floor below which the design is not doing the thing it exists to do.
    "torque_dominance_min": 5.0,
    # Fraction of upstream swirl still present downstream in the active
    # annulus. 0.30 means at least 70 % of the tangential momentum was taken.
    "swirl_residual_max": 0.30,
    # Axial velocity on the core axis, normalised by freestream. Vortex
    # breakdown is marked classically by axial stagnation or reversal, so any
    # value <= 0 is a fail. A small positive margin is required so that a
    # marginal case is not read as a pass.
    "core_axial_min": 0.05,
}

REQUIRED = {
    "torque_dominance": ["torque_Nm", "omega_rad_s", "axial_force_N", "U_axial_m_s"],
    "swirl_extraction": ["V_theta_upstream_m_s", "V_theta_downstream_m_s"],
    "core_stability":   ["U_axial_core_min_normalised"],
}


class MissingData(Exception):
    pass


def _need(case, keys, gate):
    missing = [k for k in keys if k not in case or case[k] is None]
    if missing:
        raise MissingData("gate %r needs %s, absent from the case file"
                          % (gate, ", ".join(missing)))
    return [float(case[k]) for k in keys]


def torque_dominance(case, cfg):
    T, w, F, U = _need(case, REQUIRED["torque_dominance"], "torque_dominance")
    p_axial = F * U
    if p_axial == 0:
        # Not a pass. Zero axial power makes the ratio undefined, and an
        # undefined ratio reported as infinite is how a divide-by-zero becomes
        # a headline number.
        raise MissingData("axial power is exactly zero -- ratio undefined, "
                          "not infinite; check the extraction")
    ratio = (T * w) / p_axial
    lim = cfg["torque_dominance_min"]
    return ratio >= lim, ratio, "T_z*omega / (F_z*U_z) = %.3f  (need >= %.1f)" % (ratio, lim)


def swirl_extraction(case, cfg):
    up, down = _need(case, REQUIRED["swirl_extraction"], "swirl_extraction")
    if up == 0:
        raise MissingData("upstream swirl is zero -- there is nothing to "
                          "extract, so this case cannot be scored")
    residual = abs(down) / abs(up)
    lim = cfg["swirl_residual_max"]
    return residual <= lim, residual, ("V_theta_down / V_theta_up = %.3f  (need <= %.2f)"
                                       % (residual, lim))


def core_stability(case, cfg):
    (u_min,) = _need(case, REQUIRED["core_stability"], "core_stability")
    lim = cfg["core_axial_min"]
    return u_min >= lim, u_min, ("min axial velocity for r < r* = %.3f  (need >= %.2f; "
                                 "<= 0 is reversal, i.e. breakdown)" % (u_min, lim))


GATES = [
    ("torque_dominance", torque_dominance),
    ("swirl_extraction", swirl_extraction),
    ("core_stability", core_stability),
]


def evaluate(case, cfg=None):
    cfg = dict(DEFAULTS, **(cfg or {}))
    cfg.update(case.get("thresholds", {}))
    results, errors = [], []
    for name, fn in GATES:
        try:
            ok, value, detail = fn(case, cfg)
            results.append({"gate": name, "pass": bool(ok),
                            "value": value, "detail": detail})
        except MissingData as e:
            errors.append({"gate": name, "error": str(e)})
    return results, errors, cfg


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case", help="JSON of extracted CFD quantities")
    ap.add_argument("--json", metavar="PATH", help="also write the report as JSON")
    args = ap.parse_args(argv[1:])

    case = json.load(open(args.case, encoding="utf-8"))
    results, errors, cfg = evaluate(case)

    label = case.get("label", args.case)
    print("gates.py  case=%s  r* = %.8f" % (label, R_STAR))
    for r in results:
        print("  %-18s %s   %s" % (r["gate"], "PASS" if r["pass"] else "FAIL", r["detail"]))
    for e in errors:
        print("  %-18s ERROR  %s" % (e["gate"], e["error"]))

    # An unevaluated gate is not a passed gate. Without this, a case file
    # missing every field prints three ERROR lines and, if the caller only
    # checks for "FAIL", reads as clean. Three gates exist; three must be
    # evaluated for the verdict to mean anything.
    evaluated = len(results)
    print("  evaluated %d of %d gates" % (evaluated, len(GATES)))
    if evaluated < len(GATES):
        print("VERDICT: INCOMPLETE -- an unevaluated gate is not a passed gate.")
        return 2

    verdict = all(r["pass"] for r in results)
    print("VERDICT: %s" % ("PASS (hydrodynamics only -- take it to a flume)"
                           if verdict else "FAIL"))

    if args.json:
        json.dump({"label": label, "results": results, "errors": errors,
                   "thresholds": cfg, "verdict": verdict, "evaluated": evaluated},
                  open(args.json, "w", encoding="utf-8"), indent=2)
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
