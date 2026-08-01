#!/usr/bin/env bash
# Finish today's commits. Run:  bash ~/Desktop/geometry/finish-today.sh
#
# Situation: two clones of the same repo both hold today's changes.
#   ~/geometry          -> already committed (70d08d7, 06aff2e), needs push
#   ~/Desktop/geometry  -> same edits uncommitted, PLUS book4/PO_10_source
#
# Order matters: push the committed clone first, then sync this one and
# commit only what is unique to it.
set -e

echo "=== 1. push the clone that already has the commits ==="
cd ~/geometry
rm -f .git/*.lock 2>/dev/null || true
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null || true
git log --oneline -2
git push

echo
echo "=== 2. sync this clone, keeping only what is unique to it ==="
cd ~/Desktop/geometry
rm -f .git/*.lock 2>/dev/null || true
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null || true

# the rotor + site edits are byte-identical to what was just pushed,
# so drop the local copies and take them from origin
git checkout -- book4/rotor_geometry.py HVEH/rotor_geometry.py \
                index.html omega/index.html _cajueiro-index-misplaced.html 2>/dev/null || true
git pull --rebase origin main

echo
echo "=== 3. commit the P290 material (only in this clone) ==="
git add book4/PO_10_source book4/dm3_rstar_verify.py
git commit -F - <<'MSG'
P290: rebuild poster and long abstract from source, with corrections

The original PO_10 .tex existed in no repository -- only the built PDF.
Source reconstructed here so the document is editable again.

  - rstar 0.80 -> 0.77594059 (0.80 matches no lambda in the family)
  - the numerical section now DECLARES its section z(0) = 0; the theorem
    hypothesises z(0) >= log 2, and the two were silently different
  - scaling law lambda = eps*exp(-z0) added, which reconciles them:
    r*(lambda=1) = 0.572235, r*(lambda=2) = 0.775941
  - Table 1 recomputed; the caption's window t in [5,15] yields -2.00 flat
  - submission codes corrected to portal values: P290, and EXP13 /
    MC48 / CO144 / OF53 for the companion submissions
  - contact updated to pg6llc@gmail.com
  - book reference relabelled B3 . Vol III, ISBN 979-8-9954416-6-3
    (the previously cited 979-8-9954416-9-4 appears in no ISBN map)

Adds P290_poster.tex -- A0 portrait conference poster, figures generated
from the verified numerics by figs.py / figs2.py -- and
dm3_rstar_verify.py, an independent check of the scaling law.

KNOWN OPEN: the zdot(0.3) column of the original Table 1 does not
reproduce under any convention tried. Recomputed rather than carried.
MSG
git push

echo
echo "=== 4. AXLE: the EXP13 commit still needs a push ==="
cd ~/Desktop/AXLE
rm -f .git/*.lock 2>/dev/null || true
git log --oneline -1
git push origin aula/rag-course

echo
echo "Done. Everything from today is in the public record."
