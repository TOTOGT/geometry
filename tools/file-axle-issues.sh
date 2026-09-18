#!/usr/bin/env bash
# file-axle-issues.sh — open the nine obligations that have no issue.
#
#   brew install gh && gh auth login        # once
#   bash tools/file-axle-issues.sh --dry    # show what would be filed
#   bash tools/file-axle-issues.sh          # file them
#
# WHY THESE NINE. The corpus cited ten AXLE numbers. Checked 2026-09-15, only
# #6, #12, #13 and #14 are obligation issues; #15 is an unrelated issue, #16 a
# discussion, and #17-#20 are pull requests. GitHub numbers issues and PRs in
# one sequence, so none of those numbers can be reused. The obligations below
# are real and have no home. See docs/axle-issue-map.md.
#
# After filing, write each number into docs/axle-issue-map.md and into the page
# listed as "cited in", which currently says the obligation is not yet filed.

set -euo pipefail
DRY=0; [ "${1:-}" = "--dry" ] && DRY=1
REPO="${AXLE_REPO:-$HOME/Desktop/AXLE}"
command -v gh >/dev/null || { echo "gh not installed: brew install gh && gh auth login"; exit 1; }
[ -d "$REPO/.git" ] || { echo "not a git repo: $REPO"; exit 1; }
cd "$REPO"

file_one () {  # title, body
  if [ $DRY -eq 1 ]; then
    printf '\n--- would file ---\n%s\n%s\n' "$1" "$2"; return
  fi
  local f; f=$(mktemp); printf '%s\n' "$2" > "$f"
  gh issue create --title "$1" --body-file "$f" --label "obligation" 2>/dev/null \
    || gh issue create --title "$1" --body-file "$f"
  rm -f "$f"
}

file_one "Regeneration loop invariant after g6 cycles — transfinite case" \
"Source: \`regeneration_loop_invariant.lean\`
Cited in: \`GameTheory_Full_Pack.html\` (geometry)

The invariant is proved for finite cycle counts. The transfinite case is open.

Acceptance: the statement holds for all limit ordinals, no \`sorry\`, axioms
limited to propext / Classical.choice / Quot.sound."

file_one "Floquet multipliers for the spiral return map" \
"Source: \`Main_v6.lean\`
Cited in: \`GameTheory_Full_Pack.html\` (geometry)

Multipliers of the return map on the spiral section, and the stability of the
closed orbit that follows from them.

Acceptance: multipliers defined in Lean and the stability conclusion proved from
them rather than asserted alongside them."

file_one "IPR_trib > IPR_fib — formal bound" \
"Source: \`SwarmSimulator.lean\`
Cited in: \`GameTheory_Full_Pack.html\` (geometry)

Inverse participation ratio, Tribonacci against Fibonacci. Numerics support the
inequality; no formal bound exists.

Acceptance: a proved inequality with its hypotheses stated, or a counterexample."

file_one "Spectral measure of the transfer operator at a Whitney fold" \
"Source: \`FoldEvents.lean\`
Cited in: \`GameTheory_Full_Pack.html\` (geometry)

Spectral measure theory for fold maps.

Acceptance: the measure constructed, not assumed, and the spectral statement
proved for the fold normal form."

file_one "LCH construction for Legendrian action positivity" \
"Source: \`MarketThreshold.lean\`
Cited in: \`GameTheory_Full_Pack.html\` (geometry)

Legendrian contact homology, and positivity of the action functional.

Acceptance: the construction carried far enough that the positivity statement is
well-typed, then proved."

file_one "Kernel dimension from contact topology" \
"Cited in: \`book8/ch6-quantum.html\` (geometry), which carries a proof outline
and marks the statement CONJECTURE.

Acceptance: the outline turned into a Lean statement with hypotheses, then
proved or refuted."

file_one "O7 — the asymmetric inner boundary against the symmetric Gronwall bound" \
"Cited in: \`ch-recurrence-ladder.html\` (geometry). Recorded as O7 in
\`PrincipiaOrthogona1/PrincipiaVol1.lean\`.

epsilon_0 = |mu_max| / (2 (1 + sup||Hess V||)) is the symmetric Gronwall bound.
The numerical inner boundary r* ~ 0.77594058 is asymmetric, and is numerical
input from the dm3 integration rather than a theorem.

The file states the three-way disagreement: the formula at H = 3 gives 1/4,
the printed arithmetic corresponds to H = 2, and \`epsilon0_of_eq_third_iff\`
proves 1/3 forces H = 2. Deciding it is a question about which Hessian bound
enters the estimate — V''(1) = 6 or |L2| = 3 — and that is physics, not Lean.

Acceptance: the Hessian bound settled with a stated reason, and the constant
either closed or withdrawn corpus-wide."

file_one "State the Global Positivity Theorem as a Lean proposition" \
"Cited in: \`book4/ch14.html\` (geometry).

Not a \`sorry\` and not an axiom: a precise \`theorem GPT : ...\` with its
hypotheses stated correctly. Once the statement is formalised, the gap between
what is proved and what is needed becomes a measurable distance.

The condition: d(alpha_arith) restricted to ker(alpha_arith) is positive-definite
for 0 < sigma < 1 with sigma != 1/2, and degenerates exactly on sigma = 1/2 —
equivalently a sign condition on the Wronskian W = c d_t g - g d_t c.

This is equivalent to the Riemann Hypothesis. Formalising the statement is the
obligation; proving it is not."

file_one "Non-integrability from Baker's theorem" \
"Cited in: \`book4/ch14.html\` (geometry), Ch 11 rung.

alpha_arith wedge d(alpha_arith) is non-vanishing on a dense set of t, via
Q-linear independence of { log p : p prime } (Baker, linear forms in logarithms).

Acceptance: the density statement proved in Lean, with the appeal to Baker
either discharged from Mathlib or carried as one clearly named hypothesis."

echo
echo "Done. Record the numbers in docs/axle-issue-map.md, then replace the"
echo "'not yet filed' wording on each page named above."
