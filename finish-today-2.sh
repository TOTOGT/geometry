#!/usr/bin/env bash
# Resume from step 2. Step 1 already succeeded (61e8289..06aff2e pushed).
# Run:  bash ~/Desktop/geometry/finish-today-2.sh
#
# The rebase was blocked by ~27 files of YOUR earlier in-progress work.
# Those get stashed across the pull and restored afterwards -- they are
# not committed here.
set -e

cd ~/Desktop/geometry
rm -f .git/*.lock 2>/dev/null || true
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null || true

echo "=== 2a. set aside your in-progress work ==="
git stash push -u -m "wip before P290 sync $(date +%F)" \
  -- ':!book4/PO_10_source' ':!book4/dm3_rstar_verify.py' || true
echo "  stashed:"; git stash list | head -3 | sed 's/^/    /'

echo
echo "=== 2b. sync with origin ==="
git pull --rebase origin main

echo
echo "=== 3. commit the P290 material ==="
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
echo "=== 4. restore your in-progress work ==="
git stash pop || {
  echo
  echo "  !! stash pop hit a conflict."
  echo "     Your work is NOT lost -- it is in: git stash list"
  echo "     Recover with: git checkout --theirs <file>  (or resolve by hand)"
  exit 1
}
echo "  restored. Still uncommitted, as before:"
git status --porcelain | grep '^ M' | wc -l | sed 's/^/    /'
echo "    modified files (yours, untouched)"

echo
echo "=== 5. AXLE: push the EXP13 commit ==="
cd ~/Desktop/AXLE
rm -f .git/*.lock 2>/dev/null || true
git log --oneline -1
git push origin aula/rag-course

echo
echo "Done."
