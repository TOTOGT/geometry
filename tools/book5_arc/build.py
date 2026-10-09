import re,html
exec(open('chapters.py',encoding='utf-8').read())
exec(open('patches.py',encoding='utf-8').read())
apply_en(CH)
apply_en2(CH)
PT={}
for _f in ['pt_a','pt_b','pt_c']:
    _ns={}; exec(open(_f+'.py',encoding='utf-8').read(),_ns); PT.update([v for k,v in _ns.items() if k.startswith('PT_')][0])
apply_pt(PT)
apply_pt2(PT)
D='/'.join([__import__('os').path.expanduser('~'),'mnt','geometry','book5'])
CSS="""
:root{--void:#04040a;--surface:#0c0d16;--card:#10111c;--gold:#c9a84c;--teal:#0ABAB5;--red:#e05a3a;--text:#e8e4d8;--muted:#8a8674;--dim:#2a2920;--rule:rgba(201,168,76,0.18);--serif:'Noto Serif',Georgia,serif;--mono:'JetBrains Mono','Courier New',monospace;}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--serif);background:var(--void);color:var(--text);font-size:18px;line-height:1.85;-webkit-font-smoothing:antialiased}
.hero{padding:4.5rem 1.5rem 3.5rem;text-align:center;border-bottom:1px solid var(--rule)}
.hero-tag{font-family:var(--mono);font-size:.6rem;letter-spacing:.32em;text-transform:uppercase;color:var(--gold);border:1px solid currentColor;padding:.2rem .65rem;display:inline-block;margin-bottom:1.8rem}
.hero h1{font-size:clamp(1.8rem,5vw,3rem);font-weight:400;letter-spacing:.03em;color:var(--gold);line-height:1.2}
.hero-sub{font-size:1rem;color:var(--muted);max-width:640px;margin:.9rem auto 0;font-style:italic;line-height:1.7}
.page{max-width:720px;margin:0 auto;padding:3rem 1.25rem 4rem}
.page h2{font-size:1.2rem;font-weight:400;color:var(--gold);margin:2.4rem 0 .8rem;letter-spacing:.03em}
.page p{margin-bottom:1.2rem}
.math{font-family:var(--mono);font-size:.92rem;color:var(--gold);background:var(--surface);border:1px solid var(--dim);padding:.8rem 1.2rem;margin:1.4rem 0;overflow-x:auto}
.status{border-left:2px solid var(--teal);padding:.9rem 1.2rem;margin:1.6rem 0;background:rgba(10,186,181,.04);font-size:.93rem;line-height:1.75}
.status .lab{font-family:var(--mono);font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:.4rem}
.pager{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--rule);font-family:var(--mono);font-size:.7rem}
.pager a{color:var(--gold);text-decoration:none}
footer.prov-foot{max-width:720px;margin:0 auto;padding:1.5rem 1.25rem 3rem;border-top:1px solid var(--rule);font-size:.78rem;color:var(--muted);line-height:1.7}
footer.prov-foot a{color:var(--gold)}
"""
def render(i,pt=False):
    f,short,title,sub,blocks=CH[i]
    if pt:
        short,title,sub,blocks=PT[f]
    sfx='-pt' if pt else ''
    def L(x): return x[:-5]+'-pt.html' if pt else x
    other=(f if pt else f[:-5]+'-pt.html')
    UI=dict(lang='pt-BR',tag='Vol V · Arco das dimensões',of='de',idx='índice do Vol V',foot='Rascunho em português (assistido por máquina, ainda sem revisão de falante nativo)',sw='English') if pt else dict(lang='en',tag='Vol V · Dimensions arc',of='of',idx='Vol V index',foot='Draft, English (PT edition: machine-assisted draft, unreviewed)',sw='Português')
    out=[]
    for b in blocks:
        if b[0]=='p': out.append('<p>%s</p>'%b[1])
        elif b[0]=='h': out.append('<h2>%s</h2>'%b[1])
        elif b[0]=='m': out.append('<div class="math">%s</div>'%b[1])
        elif b[0]=='st': out.append('<div class="status"><span class="lab">%s</span>%s</div>'%(b[1],b[2]))
    nm=lambda j:(PT[CH[j][0]][0] if pt else CH[j][1])
    prev=('<a href="%s">&larr; %s</a>'%(L(CH[i-1][0]),nm(i-1))) if i>0 else '<a href="index.html">&larr; %s</a>'%UI['idx']
    nxt=('<a href="%s">%s &rarr;</a>'%(L(CH[i+1][0]),nm(i+1))) if i<len(CH)-1 else '<a href="index.html">%s &rarr;</a>'%UI['idx']
    esc=html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="{UI['lang']}" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc} &middot; Vol V</title>
<link rel="alternate" hreflang="{'en' if pt else 'pt-BR'}" href="{other}">
<meta name="description" content="{html.escape(sub)} Principia Orthogona, Vol V, dimensions arc.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="hero"><span class="hero-tag">{UI['tag']} &middot; {i+1} {UI['of']} {len(CH)}</span><div style="margin-top:.8rem"><a href="{other}" style="font-family:var(--mono);font-size:.7rem;color:var(--gold)">{UI['sw']}</a></div><h1>{esc}</h1><p class="hero-sub">{html.escape(sub)}</p></div>
<div class="page">
{chr(10).join(out)}
<div class="pager">{prev}{nxt}</div>
</div>
<script src="nav.js"></script>
<footer class="prov-foot">
<strong>{esc}</strong><br>
Principia Orthogona &middot; Vol V &middot; {UI['foot']} &middot; G6 LLC &middot; Pablo Nogueira Grossi &middot; Newark NJ &middot; 2026<br>
Series <a href="https://zenodo.org/communities/principia-orthogona" target="_blank" rel="noopener">Principia Orthogona community</a> &middot; <a href="https://github.com/TOTOGT/geometry">GitHub</a><br>
&copy; 2026 Pablo Nogueira Grossi &mdash; G6 LLC &middot; Licence CC BY-NC-ND 4.0
</footer>
</body>
</html>
"""
tot=0
for i,c in enumerate(CH):
    h=render(i); open(D+'/'+c[0],'w',encoding='utf-8').write(h)
    open(D+'/'+c[0][:-5]+'-pt.html','w',encoding='utf-8').write(render(i,True))
    body=re.sub(r'<style.*?</style>|<script.*?</script>','',h,flags=re.S); body=re.sub(r'<[^>]+>',' ',body)
    w=len(body.split()); tot+=w; print(c[0],w)
print('total',tot)
# nav.js
import os
p=D+'/nav.js'; n=open(p,encoding='utf-8').read()
for c in CH:
    n=re.sub(r'\n  \{ href:"%s", label:"[^"]*" \},'%re.escape(c[0]),'',n)
anchor='  { href:"chV-erdos-machine.html", label:"Erdős" },'
assert anchor in n
add=''.join('\n  { href:"%s", label:"%s" },'%(c[0],c[1]) for c in CH)
n=n.replace(anchor,anchor+add,1); open(p,'w',encoding='utf-8').write(n)
p=D+'/index.html'; x=open(p,encoding='utf-8').read()
for c in CH:
    x=re.sub(r'\n    <a href="%s" class="ch-row">.*?</a>'%re.escape(c[0]),'',x,flags=re.S)
anchor='    </a>\n  </div>\n\n  <div style="margin-top:3rem;">'
assert anchor in x
rows=''.join(f'\n    <a href="{c[0]}" class="ch-row">\n      <span class="ch-n">Dim {k+1}</span>\n      <div class="ch-info"><strong>{html.escape(c[2])}</strong><span class="sub">{html.escape(c[3])}</span></div>\n      <span class="badge b-prose">{"Derivação · Derivation" if "contact" in c[0] else "Prosa"}</span>\n    </a>' for k,c in enumerate(CH))
x=x.replace(anchor,'    </a>'+rows+'\n  </div>\n\n  <div style="margin-top:3rem;">',1); open(p,'w',encoding='utf-8').write(x)
print('wired')
