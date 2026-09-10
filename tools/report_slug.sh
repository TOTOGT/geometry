# report_slug.sh — ONE definition of how a gate report is named.
#
#   . tools/report_slug.sh ; slug=$(report_slug /abs/path/to/File.lean)
#
# Sourced by tools/leancheck.sh (which writes the report) and tools/overnight.sh
# (which checks whether one already exists). Two copies of this rule would be
# two naming schemes, and the second one to drift would silently stop finding
# yesterday's evidence.
#
# WHY A PATH AND NOT A BASENAME. Until 2026-09-10 the report was
# "$(basename file).axioms.txt". Measured on the 2026-09-09 run order: 280
# files, 70 colliding basenames, covering 187 of them. Six different
# lakefile.lean, five TribonacciDNLS.lean, five Chain.lean, four AXLE.lean.
# Every group wrote ONE report and the last writer won, so the evidence
# directory held a file named for a declaration set that belonged to a
# different file -- and the ledger then attributed those declarations to
# whichever path it matched first. book4/ZetaScratch.lean showing a kernel
# record sourced from ZetaReflection.axioms.txt is that bug, visible in the
# 2026-09-10 ledger.
report_slug() {
  printf '%s' "${1%.lean}" \
    | sed -e "s|^$HOME/Desktop/||" -e "s|^$HOME/||" -e 's|^/||' -e 's|/|__|g'
}
