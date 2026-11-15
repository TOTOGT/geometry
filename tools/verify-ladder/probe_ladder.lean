/-
  Kernel axiom probe for the two Ladder files, run through the library targets (import), not by compiling the files directly.
  Nine theorems: six in LadderBound.lean (namespace LadderBound), three in LadderRung.lean (root namespace).
  Count to gate: 9.   grep -c '#print axioms' tools/verify-ladder/probe_ladder.lean
-/
import LadderBound
import LadderRung

#print axioms LadderBound.gap_eq
#print axioms LadderBound.half_gap
#print axioms LadderBound.ladder_abs_error
#print axioms LadderBound.ladder_rel_error
#print axioms LadderBound.ladder_rel_error_of_lt
#print axioms LadderBound.ladder_forbids_nothing
#print axioms ladder_bracket
#print axioms ladder_nearest_rung
#print axioms ladder_nearest_rung_rel
