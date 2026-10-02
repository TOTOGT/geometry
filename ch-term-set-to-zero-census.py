#!/usr/bin/env python3
"""ch-term-set-to-zero-census.py -- the census on the page 'The Term You Set to Zero', made repeatable.

Run from the repository root:   python3 ch-term-set-to-zero-census.py
Standard library only; needs git.

Counting basis (fixed here so the numbers can be regenerated):
  files    = every git-tracked file ending .html .md .lean .tex or .py,
             minus ch-term-set-to-zero.html itself and docs/audit-log.md
  match    = case-insensitive substring, one count per file (not per occurrence)
  'set to zero' is also reported after removing the chapter's own title, "The Term You Set to Zero",
             because most files that contain the phrase only link to this chapter.

History: the page's original counts (contact form 150, Reeb 143, entropy 60, adiabatic 4, Clausius 5,
neglect 7, set to zero 0) were taken over 685 files by a script that was not kept. They cannot be
regenerated, and this script does not claim to reproduce them: the corpus has grown and the basis
above is explicit. The 'set to zero = 0' result is the one that matters, and it can be rechecked.
"""
import subprocess, sys

EXT = ('.html', '.md', '.lean', '.tex', '.py')
SKIP = {'ch-term-set-to-zero.html', 'docs/audit-log.md'}
TERMS = ['contact form', 'Reeb', 'entropy', 'adiabatic', 'isentropic', 'Clausius',
         'set to zero', 'we assume', 'neglect']
TITLE = 'the term you set to zero'

def tracked():
    out = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True).stdout.splitlines()
    return [f for f in out if f.endswith(EXT) and f not in SKIP]

def main():
    files = tracked()
    texts = {}
    for f in files:
        try:
            texts[f] = open(f, encoding='utf-8', errors='ignore').read().lower()
        except OSError:
            pass
    print('files counted: %d (git-tracked .html .md .lean .tex .py, minus this chapter and docs/audit-log.md)' % len(texts))
    for t in TERMS:
        n = sum(1 for x in texts.values() if t.lower() in x)
        print('  %-14s %5d' % (t, n))
    own = [f for f, x in texts.items() if 'set to zero' in x.replace(TITLE, '')]
    print("  %-14s %5d   after removing the title 'The Term You Set to Zero':" % ('set to zero', len(own)))
    for f in sorted(own):
        print('      ' + f)
    print('Read each file listed above: a hit only counts against the page if it records that a term was dropped from a')
    print('contact form or other model. The count of such files is the number to compare with the page\'s "zero".')

if __name__ == '__main__':
    sys.exit(main())
