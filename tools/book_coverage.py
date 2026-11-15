"""Verification coverage for every book folder (2026-11-14; replaces book4_coverage.py's single-book scope).
Per page in bookN/: claims in docs/claims.tsv, checkable claims (labelled proved/established/measured/empirical/
machine-checked/kernel-checked), those with a warrant other than '-', and same-stem .py/.lean tools in the folder.
Books are folders that keep receiving chapters, so rerun after adding one. Writes docs/book-verification-coverage.tsv
(sorted by book, then largest gap) and prints a per-book summary."""
import csv,glob,os,re,collections
rows=list(csv.reader(open('docs/claims.tsv',encoding='utf-8'),delimiter='\t'))[1:]
CHECK={'proved','established','measured','empirical','machine-checked','kernel-checked'}
by=collections.defaultdict(lambda:[0,0,0])
for r in rows:
    if len(r)<6: continue
    b=by[r[0]]; b[0]+=1
    if r[3] in CHECK or r[4] in CHECK:
        b[1]+=1
        if r[5] not in ('-',''): b[2]+=1
book_rows=collections.Counter()
for r in rows:
    if len(r)>6: book_rows[r[0].split('/')[0]]+=1
runs={}
if os.path.exists('docs/script-runs-2026-11-14.tsv'):
    for r in csv.reader(open('docs/script-runs-2026-11-14.tsv',encoding='utf-8'),delimiter='\t'):
        if r and r[0]!='script': runs[r[0].rsplit('.',1)[0]]=r[1]
out=[]
def booknum(p): m=re.match(r'book(\d+)',p); return int(m.group(1)) if m else 999
for d in sorted(glob.glob('book[0-9]*'),key=booknum):
    if not os.path.isdir(d): continue
    files=set(os.listdir(d))
    for p in sorted(glob.glob(d+'/*.html')):
        stem=os.path.basename(p)[:-5]; key=re.split(r'[-_]',stem)[0]
        tools=[f for f in files if f.endswith(('.py','.lean')) and (f.startswith(stem) or f.startswith(key+'-') or f.startswith(key+'_'))]
        extracted = book_rows.get(d,0)>0
        if extracted:
            n,c,w=by.get(p,[0,0,0]); status='extracted' if n else 'extracted_no_rows_for_page'
            vals=(n,c,w,c-w)
        else:
            status='NOT_ASSESSED'; vals=('','','','')
        out.append((d,p,status)+vals+(';'.join(sorted(tools)),'unassessed',runs.get(os.path.basename(p)[:-5],'not_run')))
out.sort(key=lambda x:(booknum(x[0]),-(x[6] if x[6]!='' else -1)))
with open('docs/book-verification-coverage.tsv','w',encoding='utf-8') as f:
    f.write('book\tpage\textraction_status\tclaims\tcheckable\twarrant_present\tcheckable_without_warrant\tsame_stem_tools\twarrant_adequate\tscript_check_result\n')
    for o in out: f.write('\t'.join(map(str,o))+'\n')
agg=collections.OrderedDict()
for o in out:
    a=agg.setdefault(o[0],[0,0,0,0,'extracted' if o[2]!='NOT_ASSESSED' else 'NOT_ASSESSED']); a[0]+=1
    if o[3]!='': a[1]+=o[4]; a[2]+=o[5]
    a[3]+=(0 if o[7] else 1)
print("book pages checkable warrant_present pages_without_tool extraction")
for k,a in agg.items():
    print(f"{k:8s} {a[0]:4d} "+(f"{a[1]:5d} {a[2]:5d}" if a[4]!='NOT_ASSESSED' else "    -     -")+f" {a[3]:4d}  {a[4]}")
print("warrant_adequate is 'unassessed' until a human review records it; script_check_result says a script ran, not that it tests the claim.")
