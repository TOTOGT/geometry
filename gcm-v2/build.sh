#!/usr/bin/env bash
# One source -> two outputs.  src/gcm-v2.md -> out/gcm-v2.pdf and out/gcm-framework.html
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
pandoc src/gcm-v2.md -s --mathml -o out/gcm-framework.html \
  --metadata pagetitle="Generative Contact Mechanics, Version 2" \
  -V maxwidth=48em
pandoc src/gcm-v2.md -s --pdf-engine=xelatex -V geometry:margin=1in -V mainfont="DejaVu Serif" -V colorlinks=true -V linkcolor=blue -V urlcolor=blue -o out/gcm-v2.pdf
sha256sum src/gcm-v2.md | tee out/source.sha256
echo built
