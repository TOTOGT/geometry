#!/usr/bin/env python3
"""The page and the PDF must be the same document.  Two checks:
 (1) both were built from the same source (sha256 of src/gcm-v2.md recorded at build time and re-computed now);
 (2) the prose of the finished HTML and the finished PDF is identical: all alphabetic words of length >= 4,
     in order, with math excluded from the HTML (MathML <math> removed) and ligatures/hyphenation normalised in the PDF.
Math notation itself is NOT compared word-for-word (PDF and MathML extract differently); it comes from the same source, check (1)."""
import re, subprocess, hashlib, sys, html
from pathlib import Path
here=Path(__file__).parent; ok=True
rec=(here/'out/source.sha256').read_text().split()[0]
now=hashlib.sha256((here/'src/gcm-v2.md').read_bytes()).hexdigest()
print(("PASS " if rec==now else "FAIL ")+"source unchanged since build", now[:12]); ok&=rec==now
h=(here/'out/gcm-framework.html').read_text()
h=re.sub(r'<math.*?</math>','',h,flags=re.S); h=re.sub(r'<(script|style).*?</\1>','',h,flags=re.S)
h=re.sub(r'<title>.*?</title>','',h,flags=re.S)
h=html.unescape(re.sub(r'<[^>]+>',' ',h))
pdf=subprocess.run(['pdftotext','-layout',str(here/'out/gcm-v2.pdf'),'-'],capture_output=True,text=True).stdout
for a,b in (('ﬁ','fi'),('ﬂ','fl'),('ﬀ','ff')): pdf=pdf.replace(a,b)
def words(t): return [w.lower() for w in re.findall(r"[A-Za-z]{4,}",t)]
# vocabulary of prose words in the source (math removed), built first so line-end hyphens can be resolved
src=(here/'src/gcm-v2.md').read_text()
prose=re.sub(r'\$\$.*?\$\$','',src,flags=re.S); prose=re.sub(r'\$[^$\n]*\$','',prose)
vocab=set(words(prose))
def fix(mo):                                  # 'dissipa-\ntion' -> joined if the joined word is in the source prose, else 'Euler-\nLagrange' -> two words
    a,b=mo.group(1),mo.group(2)
    return a+b if (a+b).lower() in vocab else a+' '+b
pdf=re.sub(r'([A-Za-z]+)-\n\s*([A-Za-z]+)',fix,pdf)
wh,wp=words(h),words(pdf)
wh=[w for w in wh if w in vocab]; wp=[w for w in wp if w in vocab]
same=wh==wp
print(("PASS " if same else "FAIL ")+f"prose words identical in HTML and PDF ({len(wh)} vs {len(wp)})")
if not same:
    import difflib
    d=[x for x in difflib.unified_diff(wh,wp,lineterm='',n=0)][:30]; print('\n'.join(d))
ok&=same
sys.exit(0 if ok else 1)
