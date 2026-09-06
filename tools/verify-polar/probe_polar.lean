/-! Kernel probe for the polar-polygon trio.

    Named here so the Tier-1 figure in the registry cannot be typed: it exists
    only because this file elaborated and `#print axioms` answered. Twenty
    declarations, which is `grep -c '^#print axioms'` on this file
    (anchored: the unanchored form counts this docstring too). Adding a
    theorem to any of the three modules without adding its line here leaves it
    OUT of Tier 1 — that is the intended failure mode, not an oversight.
-/
import PolarTriadClosure
import PolarPolygonCommonRefinement
import ChladniPolygon

-- PolarTriadClosure (9)
#print axioms partners_six_ten
#print axioms reach_even
#print axioms six_even
#print axioms ten_even
#print axioms seven_not_reachable
#print axioms nine_not_reachable
#print axioms four_reachable
#print axioms sixteen_reachable
#print axioms odd_seeds_reach_odd

-- PolarPolygonCommonRefinement (7)
#print axioms periodic_sub
#print axioms periodic_one_const
#print axioms hex_and_dec_forces_constant
#print axioms constant_is_bisymmetric
#print axioms sawtooth_periodic_five
#print axioms sawtooth_not_constant
#print axioms sixfold_alone_permits_structure

-- ChladniPolygon (4)
#print axioms chladni6_sixfold_sym
#print axioms hexagon_nodes_are_zeros
#print axioms chladni10_tenfold_sym
#print axioms decagon_nodes_are_zeros
