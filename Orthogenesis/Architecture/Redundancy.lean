-- Orthogenesis/Architecture/Redundancy.lean
-- Partial, explicitly hypothesis-gated closure of S2 (hexgrid progressive
-- collapse resistance). Written 2026-09-28. Does NOT close S2: it converts
-- one piece of the physical claim into a counting theorem whose hypotheses
-- carry all the empirical content, and states plainly what it does not prove.
--
-- BACKGROUND. G6Crystal.lean §9 records that S2 ("hexagrid progressive
-- collapse resistance superior [to diagrid]") was deleted as a Lean theorem
-- on 2026-08-21 because it had stood as `theorem ... : True := trivial` --
-- vacuous, not a proof. The corrected position, unchanged here: "an empirical
-- result from the engineering literature is not a proof obligation." Nothing
-- below overturns that. What follows is a narrower, genuinely provable claim
-- that sits underneath the empirical one, not a replacement for it.
--
-- THE REAL MATHEMATICAL CONTENT. "Progressive collapse resistance" is a
-- nonlinear structural-mechanics property; Lean cannot hold it directly. But
-- one necessary ingredient of it is arithmetic: a frame's static
-- indeterminacy (Maxwell's rule), the count of load-bearing members beyond
-- the bare minimum needed for rigidity. More redundancy means more
-- alternative load paths, so losing one member is less likely to produce an
-- immediate mechanism. That is provable. It is NOT sufficient on its own:
-- unlike the plane (Laman's theorem gives an exact combinatorial
-- characterisation of generic rigidity in 2D), 3D generic rigidity has no
-- known combinatorial characterisation. A positive count here is necessary
-- for rigidity, not a proof of it, and says nothing about post-buckling
-- behaviour, material nonlinearity, or dynamic load redistribution -- the
-- actual subject of the cited FEM literature.
--
-- SOURCES CHECKED 2026-09-28 (WebSearch/WebFetch, this session):
--   Mashhadiali, N.; Kheyroddin, A. "Proposing the hexagrid system as a new
--   structural system for tall buildings." The Structural Design of Tall and
--   Special Buildings, 22(17), 1310-1329, 2013. Confirmed real. Summary
--   found: hexagrid "ductility and stiffness sensitivity... about three
--   times that of the diagrid system," evaluated at 30/50/70/90-story
--   heights. Exact member/joint counts were not recoverable -- full text is
--   paywalled (Wiley 403, ResearchGate 429, academia.edu robots-disallowed)
--   and no accessible mirror gave the tables.
--   Mashhadiali, N. "Progressive collapse assessment of new hexagrid
--   structural system for tall buildings." Structural Design of Tall and
--   Special Buildings, 2014. DOI 10.1002/tal.1097. Confirmed to exist
--   (Wiley); this is the paper G6Crystal.lean's citation actually needs for
--   the *collapse* claim specifically, and its full text was not reachable
--   this session either.
--   "Yildirim (2024)" as cited in G6Crystal.lean: NOT VERIFIED. Repeated
--   search found no 2024 hexagrid/diagrid/progressive-collapse paper by any
--   Yildirim. The only match is Sıla Yıldırım, a Gazi University researcher
--   with a 2021 paper ("Performance assessment of hexagrid structural
--   system") and related hexagrid work, no confirmed 2024 title. This
--   citation should be checked against whatever source it was originally
--   drawn from, or corrected/removed if it cannot be confirmed.
--   COMPLICATION, not previously recorded here: Lee, H.-U.; Kim, Y.-C.
--   "Preliminary Design of Tall Building Structures with a Hexagrid System."
--   Procedia Engineering 171, 1085-1091, 2017 -- a different, real,
--   peer-reviewed comparison -- found hexagrid systems "less efficient than
--   a diagrid system in terms of lateral resistance" for the 60-story models
--   it tested. This does not contradict Mashhadiali's ductility/collapse
--   finding (different metric: lateral stiffness vs. collapse robustness),
--   but it means "hexgrid beats diagrid," stated unqualified, overstates
--   what the literature agrees on. The two papers measure different things
--   and should be cited for the specific thing each one found.

import Mathlib.Tactic

namespace Orthogenesis.Architecture.Redundancy

/-- Static indeterminacy of a 3D pin-jointed frame (Maxwell's rule):
      DSI = bars + reactions - 3 * joints.
    DSI > 0: more members than the generic-rigidity minimum -- redundant
    load paths whose individual loss need not produce a mechanism.
    NECESSARY, not sufficient, for rigidity or for collapse resistance: see
    the file header. This function is pure counting; it makes no claim about
    material behaviour, connection type, or load history. -/
def staticIndeterminacy (bars reactions joints : ℤ) : ℤ :=
  bars + reactions - 3 * joints

/-- HYPOTHESIS, not derived: modelling a frame as effectively pin-jointed.
    Real space frames (including the Water Cube's, see nacg-unrelated notes)
    typically use semi-rigid or moment connections, which admit a different
    and more permissive counting rule. Any instantiation of the theorem below
    with real bar/joint counts must state which model it assumes. -/
structure PinJointedFrameModel where
  bars      : ℤ
  reactions : ℤ
  joints    : ℤ
  bars_nonneg      : 0 ≤ bars
  reactions_nonneg : 0 ≤ reactions
  joints_pos       : 0 < joints

/-- Comparative theorem, fully general and hypothesis-gated: if two
    pin-jointed frames share a joint count and reaction count, the one with
    more bars has strictly greater static indeterminacy. This is the entire
    provable content -- it is arithmetic once the hypotheses (bar counts, a
    shared joint count, a shared pin-jointed model) are granted. It does NOT
    by itself establish that either named frame (hexgrid, diagrid, Water
    Cube) satisfies those hypotheses: that requires sourcing real bar/joint
    counts and justifying the pin-jointed idealisation for the actual
    connection type used, which this session could not complete (see file
    header -- the cited papers' full text was not reachable). -/
theorem more_bars_implies_more_redundancy
    (F G : PinJointedFrameModel)
    (hJoints : F.joints = G.joints) (hReactions : F.reactions = G.reactions)
    (hBars : G.bars < F.bars) :
    staticIndeterminacy G.bars G.reactions G.joints <
    staticIndeterminacy F.bars F.reactions F.joints := by
  unfold staticIndeterminacy
  omega

-- STATUS: this theorem is proved, and it is not `hexagrid_collapse_
-- resistance_superior` under a new name -- it takes no position on which of
-- a real hexgrid or a real diagrid has more bars per joint at equal scale,
-- because that number was not obtained this session. Closing S2 further
-- would mean sourcing Mashhadiali (2014)'s or a comparable paper's actual
-- member/joint tables (an institutional-access or interlibrary request, not
-- a web search) and instantiating `PinJointedFrameModel` for both systems
-- with cited numbers -- at which point `more_bars_implies_more_redundancy`
-- applied to those two instances becomes a real, sourced, non-vacuous
-- result, still bounded by the necessary-not-sufficient caveat above.

end Orthogenesis.Architecture.Redundancy
