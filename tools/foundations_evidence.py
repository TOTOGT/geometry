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
    """Fully-qualified declarations, and the short-name -> namespaces index.

    Corrected 2026-09-19. The first version of this function stripped the
    namespace and returned a SET of short names. Thirteen declarations exist
    under BOTH PrincipiaVol1 and AutophagyDm3, so the set collapsed 82 theorems
    to 69 -- and the header line went on printing "58 + 24", which is 82. The
    script contradicted itself in its own first line of output for a day.
    It matters beyond the count: a row that cites `mu_dm3_neg` does not say
    WHICH `mu_dm3_neg`, and the two are different theorems in different files.
    """
    if not os.path.exists(AX): return set(), {}
    txt = io.open(AX,encoding="utf-8").read()
    full = {m.group(1) for m in re.finditer(r"^'([^']+)'", txt, re.M)}
    idx = {}
    for f in full:
        nsp, short = f.split(".", 1)
        idx.setdefault(short, set()).add(nsp)
    return full, idx

FULL, IDX = names()
L = set(IDX)                      # short names, for the MAP rows, which are short
AMBIG = {k for k,v in IDX.items() if len(v) > 1}
print("="*78); print("THE BASE LAYER -- CLAIMS AND THE LEAN THAT BEARS ON THEM"); print("="*78)
print("  lean: TOTOGT/vol1-proofs tools/axioms.txt -- %d theorems (%d PrincipiaVol1 + %d AutophagyDm3)"
      % (len(FULL),
         sum(1 for f in FULL if f.startswith("PrincipiaVol1.")),
         sum(1 for f in FULL if f.startswith("AutophagyDm3."))))
print("  %d short names live in BOTH namespaces -- a bare name does not identify a theorem." % len(AMBIG))
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
        amb=[n for n in ns if n in AMBIG]
        if amb: print("    %-17s   ?? AMBIGUOUS -- in both namespaces: %s" % ("", ", ".join(amb)))
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
 "S6  FOUR ROWS CITE A NAME THAT IS NOT UNIQUE. Propositions 4.2, 4.4 and 6.1",
 "    and Theorem A rest on declarations that exist under both PrincipiaVol1",
 "    and AutophagyDm3. Until each row names the namespace, those four say",
 "    less than they appear to. Marked ?? above.",
 "",
 "S5  THE LEAN IS IN ANOTHER REPO and has not been rebuilt at v4.32 -- see",
 "    R22 and the port branch. If the port fails, the 'SHOWN' rows above are",
 "    resting on a build nobody has reproduced since the pin moved.",
]: print("  "+g)

print()
print("="*78); print("3 -- THE EIGHTEEN UNMATCHED, READ ONE BY ONE (2026-09-19)"); print("="*78)
print("""  UNMATCHED meant "this script's topic matching found nothing". It could not
  tell that apart from "no Lean exists". Both documents and the Lean were read
  on 2026-09-19 and the eighteen are now decided. THE HEADLINE IS THAT MOST OF
  THEM HAVE NO LEAN AT ALL -- which is a fine thing for a claim to be, and a
  bad thing for a corpus to leave undeclared.""")
for row in [
 ("BOOK I", ""),
 ("Theorem 12.1", "NO LEAN. Symplectic preservation, F*omega = omega. Nothing in the"),
 ("",            "82 touches differential forms."),
 ("Theorem 3.1",  "NO LEAN. Sequential consistency of K then F."),
 ("Theorem 5.1",  "NO LEAN. Well-posedness of G = U.F.K.C on piecewise-C2 paths."),
 ("Theorem 5.2",  "NO LEAN. Local determination."),
 ("Theorem 5.4",  "CUTS AGAINST IT. Irreducibility says no operator can be removed."),
 ("",             "compression_permits_identity proves there EXISTS a compression"),
 ("",             "operator equal to the identity. In that instance C removes"),
 ("",             "nothing. Same shape as 5.3: the Lean bounds the claim rather"),
 ("",             "than supporting it, and nothing on the page says so."),
 ("BOOK II", ""),
 ("Theorem 3.5",  "NUMERIC INSTANCE ONLY. The claim is an equivalence."),
 ("",             "dPhi_at_threshold proves 0 < dPhi (9/50) -- one point, one"),
 ("",             "direction, no equivalence."),
 ("Theorem 3.2",  "ARITHMETIC ONLY. gronwall_contraction_below_stability_radius and"),
 ("",             "noiseTolerance evaluate the canonical constants; neither proves"),
 ("",             "the implication the theorem states."),
 ("Theorem 3.4",  "NO LEAN. The converse direction has nothing."),
 ("Lemma 3.1",    "NO LEAN. See section 4 for why mu_dm3_neg is not evidence."),
 ("Lemma 3.3",    "ALREADY DISCLOSED. The document itself prints SORRY on this one."),
 ("Proposition 2.1","ADJACENT, NOT THE CLAIM. contactCoeff_neg gives contactCoeff rho"),
 ("",             "< 0 for rho > 0. The claim is that H_diss smoothly regularizes S."),
 ("Proposition 4.3","A DEFINITION IS NOT EVIDENCE. The claim is that the system TAKES"),
 ("",             "the contact normal form with (mu_max, omega, beta) = (-2, 1, 1)."),
 ("",             "canonicalTriple ASSIGNS mu_max := -2. Assigning a value is not"),
 ("",             "deriving it."),
 ("Theorem B",    "THREE DIFFERENT CLAIMS UNDER ONE LABEL -- and it is stated, not"),
 ("",             "merely listed, in all three: Book II's is Threshold Equivalence,"),
 ("",             "the toy model's is the invariant torus with mu_perp = -3, gcm's"),
 ("",             "is closure under unification, tau_12 <= min(tau_1, tau_2)."),
]:
    k,v = row
    if v == "": print("  " + "-"*60 if k else ""); print("  %s"%k) if k else None
    else: print("    %-17s %s" % (k, v))

print()
print("="*78); print("4 -- MINUS TWO AND MINUS THREE"); print("="*78)
print("""  Two Lyapunov exponents run through this corpus and nothing reconciles them.

      PrincipiaVol1.mu_canonical   -(V'' 1) / 2 = -3     docstring: "Canonical
                                                         Lyapunov exponent from
                                                         Whitney fold"
      PrincipiaVol1.mu_dm3_neg     (-2 : R) < 0          docstring: "dm3
                                                         transverse Lyapunov
                                                         exponent mumax = -2"

  They sit four lines apart in PrincipiaVol1.lean. The first DERIVES -3. The
  second proves that the literal -2 is negative -- the identification of mumax
  with -2 is in the docstring, not in the theorem. canonicalTriple then ASSIGNS
  mu_max := -2 by definition.

  The documents do the same thing. The toy model's Theorem B gives the
  transverse Lyapunov exponent as -3. Book II's Proposition 4.3 gives
  mu_max = -2 in the contact normal form.

  These may well be two different quantities -- a canonical exponent from the
  Whitney fold and a transverse exponent of the limit cycle are not obviously
  the same number. THAT IS THE POINT: nothing in either repo says which, and a
  reader meeting mu_canonical four lines above mu_dm3_neg has no way to tell
  whether -2 and -3 are a distinction or a discrepancy. `[OPEN]`

  What would settle it: one sentence in PrincipiaVol1.lean naming the two
  quantities, and one in Book II saying which of them Proposition 4.3 uses.""")

print(); print("="*78)
print("Proposal only. Theorem 5.3 was the one repair applied, 2026-09-18.")
print("The eighteen UNMATCHED were read and decided 2026-09-19 -- section 3.")
print("6 gaps recorded above remain open.")
print("="*78)
