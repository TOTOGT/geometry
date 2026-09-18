#!/usr/bin/env python3
"""
foundations_evidence.py -- for each numbered claim in the BASE LAYER, what Lean bears on it.

R21 says tag the base before the superstructure, and the order is
book1 -> book2 -> toy -> gcm -> books 3 and 4 -> GTCT. Tagging needs evidence
first: you cannot mark a claim SHOWN without naming what shows it.

This joins the numbered claims of Book I, Book II, the toy model and GCM to
the 82 kernel-checked theorems in TOTOGT/vol1-proofs (58 PrincipiaVol1 +
24 AutophagyDm3). The join is by TOPIC, declared below by hand --
there is no machine link between a prose Result and a Lean name, and inventing
one silently is how the two come apart. Every row says how it was matched.

Run:  python3 tools/foundations_evidence.py
"""
import os, re, io, html

DOC  = "book1/vol1-mathematics.html"
AX   = os.path.expanduser("~/mnt/Desktop/vol1-proofs/tools/axioms.txt")

# claim -> (lean names, how matched, proposed tag, note)
# "named" = the Lean identifier encodes the claim number; "topic" = matched by subject.
MAP_BOOK1 = {
 "Theorem 5.3": (["thm_5_3_is_exactly_existential","nonCommutativity_instance",
                  "nonCommutativity_nondegenerate","exists_order_dependent",
                  "not_forall_order_dependent","commuting_instance","foldMap_not_odd"],
                 "named", "SHOWN (existential only)",
                 "THE PROSE IS STRONGER THAN THE LEAN. See section 2."),
 "Theorem 5.5": (["foldMap_branch_subset","foldSym_branch_subset"], "topic",
                 "PARTIAL", "branch-set containment, not finiteness of B itself"),
 "Theorem 9.1": (["closurePoints_stationary","closurePoints_unbounded",
                  "ordinalNextLevel_is_closure_point","sup_strictMono_isLimit",
                  "sup_lt_of_regular","regeneration_hierarchy_mahlo",
                  "ordinal_regeneration_unbounded","regeneration_unbounded"],
                 "topic", "SHOWN (ordinal core)", "the classification's ordinal machinery"),
 "Theorem 12.1":([], "none", "UNMATCHED", "symplectic preservation -- no Lean found"),
 "Theorem 3.1": ([], "none", "UNMATCHED", "sequential consistency -- no Lean found"),
 "Theorem 5.1": ([], "none", "UNMATCHED", "existence/well-posedness -- no Lean found"),
 "Theorem 5.2": ([], "none", "UNMATCHED", "local determination -- no Lean found"),
 "Theorem 5.4": ([], "none", "UNMATCHED", "irreducibility -- no Lean found"),
 "Theorem T1":  ([], "declared", "OPEN", "already carries [OPEN OBLIGATION - AXLE #14]"),
}

MAP_BOOK2 = {
 "Proposition 4.4":(["epsilon0_of_eq_third_iff","epsilon0_of_three","epsilon0_of_two",
                     "gronwall_radius","gronwall_radius_lt_one","gronwall_radius_pos"],
                    "named", "SHOWN",
                    "eps_0 = 1/3 -- epsilon0_of_eq_third_iff is named for exactly this claim"),
 "Proposition 4.2":(["mu_dm3_neg","mu_canonical","noiseTolerance"], "topic", "SHOWN",
                    "mu_max = -2, kappa_noise = 1, tau = 2; the TO audit re-derived mu_max = -2 exactly"),
 "Theorem 4.1":   (["dm3_hypothesis_nonvacuous"], "topic", "SHOWN (non-vacuity only)",
                   "that an explicit system EXISTS; not that it verifies every clause"),
 "Theorem 5.4":   ([], "declared", "MODEL",
                   "the Mini-Beast table; Neimark-Sacker row repaired 2026-08-07, see CLAUDE.md"),
 "Proposition 5.1":([], "declared", "MODEL", "singularity-bifurcation correspondence"),
 "Theorem 3.5":   ([], "none", "UNMATCHED", "Threshold Equivalence, = Theorem B"),
 "Theorem 3.2":   ([], "none", "UNMATCHED", "geometric implies stochastic"),
 "Theorem 3.4":   ([], "none", "UNMATCHED", "stochastic implies geometric"),
 "Lemma 3.1":     ([], "none", "UNMATCHED", "fold activation produces hyperbolicity"),
 "Lemma 3.3":     ([], "none", "UNMATCHED", "finite tau implies transverse contraction"),
 "Proposition 2.1":([], "none", "UNMATCHED", "regularization of the fold generator"),
 "Proposition 4.3":([], "none", "UNMATCHED", "contact normal form"),
 "Assumption 1.1":([], "n/a", "ASSUMPTION", "imports Volume I's framework wholesale"),
 "Assumption 1.2":([], "n/a", "ASSUMPTION", "imports the dm3 framework wholesale"),
}

MAP_TOY = {
 "Theorem A":     (["basin_asymmetry","Phi_pos","dPhi_pos","V_at_one","V_factored"],
                   "topic", "SHOWN (basin core)", "global attractor"),
 "Theorem D":     (["noiseTolerance","transverse_sum_bound","transverse_sum_bound_general"],
                   "topic", "PARTIAL", "stochastic stability"),
 "Theorem B":     ([], "none", "UNMATCHED", "invariant torus"),
 "Theorem C":     ([], "none", "UNMATCHED", "four bifurcations"),
 "Proposition 5.1":([], "declared", "MODEL", "already carries a 2026-08-07 [MODEL] correction notice"),
}

MAP_GCM = {
 "Proposition 6.1":(["gronwall_radius","gronwall_radius_pos","gronwall_radius_lt_one",
                     "V_critical_at_one","V_second_deriv_at_one","V_second_deriv_ne_zero"],
                    "topic", "SHOWN", "Gronwall basin estimate"),
 "Theorem A":     ([], "none", "UNMATCHED", "existence"),
 "Theorem B":     ([], "none", "UNMATCHED", "unification"),
 "Theorem C":     ([], "none", "UNMATCHED", "normal form"),
 "Theorem D":     ([], "none", "UNMATCHED", "stability"),
 "Definition 3.1":([], "n/a", "DEFINITION", "unification operator"),
}

DOCS = [("Book I  · vol1-mathematics", "book1/vol1-mathematics.html", MAP_BOOK1),
        ("Book II · vol2-contact",     "book2/vol2-contact.html",     MAP_BOOK2),
        ("toy     · vol2-toymodel",    "vol2-toymodel.html",          MAP_TOY),
        ("gcm     · gcm-framework",    "gcm-framework.html",          MAP_GCM)]

def names():
    if not os.path.exists(AX): return set()
    return {m.group(1) for m in
            re.finditer(r"^'(?:PrincipiaVol1|AutophagyDm3)\.([^']+)'",
                        io.open(AX,encoding="utf-8").read(), re.M)}

L = names()
print("="*78); print("THE BASE LAYER -- CLAIMS AND THE LEAN THAT BEARS ON THEM"); print("="*78)
print("  lean: TOTOGT/vol1-proofs tools/axioms.txt -- %d theorems (58 PrincipiaVol1 + 24 AutophagyDm3)" % len(L))
print("  order: book1 -> book2 -> toy -> gcm -> books 3 and 4 -> GTCT   (R21)")
grand={}
for label, doc, M in DOCS:
    print(); print("-"*78); print("  %s   [%s]" % (label, doc)); print("-"*78)
    for k,(ns,how,tag,note) in M.items():
        grand[tag]=grand.get(tag,0)+1
        missing=[n for n in ns if n not in L]
        print("    %-17s %-26s %-9s %s" % (k, tag, how, ", ".join(ns[:3]) + (" +%d"%(len(ns)-3) if len(ns)>3 else "") if ns else "--"))
        if note: print("    %-17s   %s" % ("", note))
        if missing: print("    %-17s   !! NOT IN THE REPORT: %s" % ("", ", ".join(missing)))
print()
print("="*78); print("TALLY"); print("="*78)
tot=sum(grand.values())
for k,v in sorted(grand.items(), key=lambda x:-x[1]):
    print("  %-28s %3d   %4.0f%%" % (k, v, 100*v/tot))
print("  %-28s %3d" % ("TOTAL", tot))
un=sum(v for k,v in grand.items() if k=="UNMATCHED")
print()
print("  %d of %d claims in the base layer have NO Lean found -- %.0f%%." % (un, tot, 100*un/tot))
print("  UNMATCHED is not UNPROVED. See gap S2.")

print()
print("="*78); print("2 -- THEOREM 5.3: THE PROSE IS STRONGER THAN THE LEAN"); print("="*78)
print("""  Book I, Theorem 5.3, reads:

      "The operators C, K, F, U do not commute; the sequence is
       order-dependent."

  The second clause is universal. The Lean is not. Among the seven theorems
  on this topic are, by name:

      exists_order_dependent          -- SOME ordering is order-dependent
      not_forall_order_dependent      -- the UNIVERSAL claim is FALSE
      thm_5_3_is_exactly_existential  -- named to say precisely this
      commuting_instance              -- an instance where they DO commute

  So the corpus already knows. A theorem exists whose only job is to record
  that 5.3 is existential, and another proving the universal reading false --
  and the prose in Book I still states the universal reading.

  The repair is one clause, not a proof: "the sequence is order-dependent"
  -> "some orderings are order-dependent; not all are". [OPEN] -- not applied
  here, because editing a numbered Result in the foundational document is the
  author's call.""")

print()
print("="*78); print("GAPS"); print("="*78)
for g in [
 "S1  THE JOIN IS DECLARED BY HAND, in the MAP_ tables above. There is no machine link",
 "    from a numbered Result to a Lean name anywhere in either repository.",
 "    EIGHTEEN of thirty-four claims are UNMATCHED -- which may mean no Lean",
 "    exists, or that this script's topic matching missed it. It cannot tell",
 "    those apart, and 53% is too large a fraction to leave undecided.",
 "",
 "S2  'UNMATCHED' IS NOT 'UNPROVED'. 3.1, 5.1, 5.2, 5.4 and 12.1 have no Lean",
 "    found. Whether they are provable, proved elsewhere, or modelling",
 "    assumptions dressed as theorems is not decided here.",
 "",
 "S3  NO TAG IS APPLIED. This proposes; it edits nothing. Marking a claim in",
 "    the foundational document is the author's call, and section 2 is the",
 "    reason to be careful about it.",
 "",
 "S4  ASSUMPTIONS AND DEFINITIONS need a convention and none exists. Book I",
 "    has 6 and 5; Book II imports Volume I and dm3 wholesale in Assumptions",
 "    1.1 and 1.2, which means Book II's whole edifice inherits Book I's",
 "    tags -- including 5.3's, which was wrong until today.",
 "",
 "S5  THE LEAN IS IN ANOTHER REPO and has not been rebuilt at v4.32 -- see",
 "    R22 and the port branch. If the port fails, the 'SHOWN' rows above are",
 "    resting on a build nobody has reproduced since the pin moved.",
]: print("  "+g)
print(); print("="*78)
print("Proposal only. Theorem 5.3 was the one repair applied, 2026-09-18.")
print("5 gaps recorded above remain open.")
print("="*78)
