#!/usr/bin/env python3
"""
book1_evidence.py -- for each numbered claim in Book I, what Lean bears on it.

R21 says tag the base before the superstructure, and the order is
book1 -> book2 -> toy -> gcm -> books 3 and 4 -> GTCT. Tagging needs evidence
first: you cannot mark a claim SHOWN without naming what shows it.

This joins Book I's numbered claims to the 58 kernel-checked PrincipiaVol1
theorems in TOTOGT/vol1-proofs. The join is by TOPIC, declared below by hand --
there is no machine link between a prose Result and a Lean name, and inventing
one silently is how the two come apart. Every row says how it was matched.

Run:  python3 tools/book1_evidence.py
"""
import os, re, io, html

DOC  = "book1/vol1-mathematics.html"
AX   = os.path.expanduser("~/mnt/Desktop/vol1-proofs/tools/axioms.txt")

# claim -> (lean names, how matched, proposed tag, note)
# "named" = the Lean identifier encodes the claim number; "topic" = matched by subject.
MAP = {
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

def names():
    if not os.path.exists(AX): return set()
    return {m.group(1) for m in
            re.finditer(r"^'PrincipiaVol1\.([^']+)'", io.open(AX,encoding="utf-8").read(), re.M)}

L = names()
print("="*78); print("BOOK I -- CLAIMS AND THE LEAN THAT BEARS ON THEM"); print("="*78)
print("  source doc : %s" % DOC)
print("  lean       : TOTOGT/vol1-proofs tools/axioms.txt -- %d PrincipiaVol1 theorems" % len(L))
print()
print("  %-14s %-26s %-9s %s" % ("claim","proposed tag","matched","lean names"))
counts={}
for k,(ns,how,tag,note) in MAP.items():
    counts[tag]=counts.get(tag,0)+1
    missing=[n for n in ns if n not in L]
    print("  %-14s %-26s %-9s %s" % (k, tag, how, ", ".join(ns) if ns else "--"))
    if note: print("  %-14s   note: %s" % ("", note))
    if missing: print("  %-14s   !! NOT IN THE REPORT: %s" % ("", ", ".join(missing)))
print()
print("  " + "  ".join("%s=%d" % (k,v) for k,v in sorted(counts.items())))

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
 "S1  THE JOIN IS DECLARED BY HAND, in MAP above. There is no machine link",
 "    from a numbered Result to a Lean name anywhere in either repository.",
 "    Five of the nine theorems are UNMATCHED -- which may mean no Lean",
 "    exists, or that this script's topic matching missed it. It cannot tell",
 "    those apart.",
 "",
 "S2  'UNMATCHED' IS NOT 'UNPROVED'. 3.1, 5.1, 5.2, 5.4 and 12.1 have no Lean",
 "    found. Whether they are provable, proved elsewhere, or modelling",
 "    assumptions dressed as theorems is not decided here.",
 "",
 "S3  NO TAG IS APPLIED. This proposes; it edits nothing. Marking a claim in",
 "    the foundational document is the author's call, and section 2 is the",
 "    reason to be careful about it.",
 "",
 "S4  ASSUMPTIONS AND DEFINITIONS ARE OUT OF SCOPE. Book I has 6 and 5 of",
 "    them. They are not claims and do not take SHOWN/CITED, but they DO need",
 "    a convention, and none exists.",
 "",
 "S5  THE LEAN IS IN ANOTHER REPO and has not been rebuilt at v4.32 -- see",
 "    R22 and the port branch. If the port fails, the 'SHOWN' rows above are",
 "    resting on a build nobody has reproduced since the pin moved.",
]: print("  "+g)
print(); print("="*78)
print("Proposal only. 5 gaps recorded above remain open.")
print("="*78)
