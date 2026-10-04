#!/usr/bin/env python3
"""tools/build_photochem.py -- writes the Book 7 photochemistry branch (index + four rooms) from tools/photochem_content/.

    python3 tools/build_photochem.py            write book7/photochem-*.html
    python3 tools/build_photochem.py --check    exit 1 if a file on disk differs from what this script would write
                                                (generated blocks <!--po-*--> are ignored in the comparison)

The pages are authored here (text in tools/photochem_content/room*.py); the generated blocks that other tools insert
(subject tag, Gold Standard Science stamp, Across the series, Run it yourself) are NOT written by this script and are
preserved if a page is rebuilt over an existing one (R8).
Textbook: K. K. Rohatgi-Mukherjee, Fundamentals of Photochemistry (revised ed.), cited by page, paraphrased only.
"""
import html as H, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from photochem_content import room1, room2, room3, room4

ROOMS = [room1.ROOM, room2.ROOM, room3.ROOM, room4.ROOM]
OUT = os.path.join(ROOT, 'book7')

UI = dict(
    en=dict(
        s1="1 · The concept, at your level", s1pill="re-levels to your English",
        s1hint="Pick a CEFR level. The same content is rewritten at that level of English.",
        target="Target language: English", diag="Not sure whether the gap is the science or the English?",
        gl_show="Show key terms in Português ↓", gl_hide="Hide Português ↑",
        glnote="If you know all these terms in Portuguese, the gap is the English, so drill the language. If the concepts are new, drill the science first. That routing is the point.",
        s4="4 · Scenario check", s4pill="comprehension", s5="5 · What this page does not do", s6="Sources",
        meta=dict(A2="Short sentences, everyday words.", B1="Adds the technical terms, passive voice, linked clauses.", B2="Technical register; the quantities and their relations.", C1="Dense, publication-level; the assumptions are in the sentence."),
        room="Room", of="of 4", idx="Photochemistry branch", gal="Scientist Gallery", prev="Previous room", next="Next room",
        lang_note="Portuguese text drafted by Claude; not yet reviewed by a native speaker.",
        src=("Source: K. K. Rohatgi-Mukherjee, <em>Fundamentals of Photochemistry</em> (revised edition), Chapter 10, {pages}, cited by page and paraphrased; no passages are reproduced. "
             "The book was read from page scans: an automatic text layer with recognition errors, with key lines and every figure value checked against page images. Page numbers are the book's. "
             "Checks: <code>book7/{verify}</code>. Where this page says <em>ours</em>, the statement is a derivation or simulation made here, not the book's."),
    ),
    pt=dict(
        s1="1 · O conceito, no seu nível", s1pill="ajusta ao seu inglês",
        s1hint="Escolha um nível CEFR. O mesmo conteúdo é reescrito naquele nível de inglês.",
        target="Idioma-alvo: inglês", diag="Não sabe se a dificuldade é a ciência ou o inglês?",
        gl_show="Mostrar termos-chave em português ↓", gl_hide="Ocultar português ↑",
        glnote="Se você conhece todos esses termos em português, a dificuldade é o inglês: treine o idioma. Se os conceitos são novos, treine primeiro a ciência. Esse roteamento é o objetivo.",
        s4="4 · Verificação de cenário", s4pill="compreensão", s5="5 · O que esta página não faz", s6="Fontes",
        meta=dict(A2="Frases curtas, palavras do dia a dia.", B1="Acrescenta termos técnicos, voz passiva, orações ligadas.", B2="Registro técnico; as grandezas e suas relações.", C1="Denso, nível de publicação; as hipóteses estão na frase."),
        room="Sala", of="de 4", idx="Ramo de fotoquímica", gal="Galeria de Cientistas", prev="Sala anterior", next="Próxima sala",
        lang_note="Texto em português redigido por Claude; ainda sem revisão de falante nativo.",
        src=("Fonte: K. K. Rohatgi-Mukherjee, <em>Fundamentals of Photochemistry</em> (edição revista), Capítulo 10, {pages}, citado por página e parafraseado; nenhuma passagem é reproduzida. "
             "O livro foi lido de imagens de página: camada de texto automática com erros de reconhecimento, com linhas-chave e todos os valores de figuras conferidos nas imagens. Os números de página são os do livro. "
             "Verificações: <code>book7/{verify}</code>. Onde a página diz <em>nosso</em>, a afirmação é derivação ou simulação feita aqui, não do livro."),
    ),
)

CSS = """
:root { --void:#04040a; --surface:#0c0d14; --card:#0f1019; --gold:#c9a84c; --teal:#0abab5; --amber:#f59e0b;
  --text:#e8e4d8; --dim:#8a8570; --rule:rgba(201,168,76,0.14); --good:#34d399; --bad:#f472b6; --blue:#60a5fa; }
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Georgia,serif;background:var(--void);color:var(--text);font-size:18px;line-height:1.75;-webkit-font-smoothing:antialiased}
nav.top{position:sticky;top:0;z-index:200;background:rgba(4,4,10,.96);backdrop-filter:blur(10px);border-bottom:1px solid var(--rule);
  padding:.55rem 1.4rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
nav.top a{font-family:'Courier New',monospace;font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);text-decoration:none}
nav.top a:hover,nav.top a.brand{color:var(--gold)}
.langtog{margin-left:auto;display:flex;gap:.2rem;background:rgba(255,255,255,.07);border-radius:20px;padding:.15rem}
.langtog button{background:none;border:none;color:#bbb;font-weight:700;font-size:.72rem;padding:.2rem .65rem;border-radius:16px;cursor:pointer;font-family:inherit}
.langtog button.on{background:var(--gold);color:#111}
.hero{padding:3.4rem 1.4rem 2.2rem;text-align:center;border-bottom:1px solid var(--rule);position:relative}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 50% 30%,rgba(201,168,76,.06),transparent 70%);pointer-events:none}
.eyebrow{font-family:'Courier New',monospace;font-size:.62rem;letter-spacing:.3em;text-transform:uppercase;color:var(--teal);border:1px solid currentColor;padding:.2rem .7rem;display:inline-block;margin-bottom:1.4rem}
.hero h1{font-size:clamp(2rem,5vw,3.2rem);font-weight:400;color:var(--gold);letter-spacing:.03em;line-height:1.15;margin-bottom:.5rem}
.hero .tag{font-style:italic;color:var(--teal);margin-bottom:.8rem}
.hero .sub{font-size:1.02rem;color:var(--dim);font-style:italic;max-width:660px;margin:0 auto}
.wrap{max-width:800px;margin:0 auto;padding:2rem 1.4rem 4rem}
.card{background:var(--card);border:1px solid var(--rule);border-radius:6px;padding:1.2rem 1.4rem;margin:1.4rem 0}
h2{font-size:1.18rem;font-weight:400;color:var(--gold);letter-spacing:.06em;margin-bottom:.6rem;display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}
h3{font-size:1.02rem;font-weight:600;color:var(--text);margin:1.4rem 0 .6rem}
p{margin-bottom:1rem}
code{font-family:'Courier New',monospace;font-size:.86em;color:var(--teal)}
strong{color:var(--gold);font-weight:600}
.pill{font-family:'Courier New',monospace;font-size:.55rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:rgba(10,186,181,.12);color:var(--teal);padding:.15rem .55rem;border-radius:20px}
.hint{font-size:.88rem;color:var(--dim);margin-bottom:.7rem}
.levels{display:flex;gap:.4rem;flex-wrap:wrap;margin:.3rem 0 .9rem}
.lvl{border:1.5px solid var(--rule);background:transparent;color:var(--dim);font-weight:600;font-size:.82rem;padding:.3rem .8rem;border-radius:20px;cursor:pointer;font-family:inherit}
.lvl.on{background:var(--teal);border-color:var(--teal);color:#04100f}
.tgt{font-size:.66rem;color:var(--teal);font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.3rem;font-family:'Courier New',monospace}
.explain{background:rgba(10,186,181,.07);border-left:3px solid var(--teal);padding:.9rem 1.1rem;font-size:1.02rem;min-height:5.5rem}
.explain .meta{font-size:.72rem;color:var(--dim);margin-top:.6rem;font-style:italic}
.diag{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;margin-top:.8rem;font-size:.86rem;color:var(--dim)}
.toggle{border:1.5px solid var(--teal);color:var(--teal);background:transparent;font-weight:600;font-size:.8rem;padding:.3rem .8rem;border-radius:20px;cursor:pointer;font-family:inherit}
.toggle.on{background:var(--teal);color:#04100f}
.gloss{display:none;margin-top:.7rem}.gloss.show{display:block}
.gterm{display:flex;justify-content:space-between;gap:1rem;padding:.3rem 0;border-bottom:1px dashed var(--rule);font-size:.92rem}
.gterm .ptw{color:var(--amber);font-style:italic;text-align:right}
.models{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:.8rem;margin-top:.4rem}
.model{border:1px solid var(--rule);border-radius:6px;padding:.8rem .9rem;background:var(--surface)}
.model .m{font-weight:700;color:var(--gold);margin-bottom:.2rem}
.model .d{font-size:.86rem;color:var(--text);margin-bottom:.4rem;line-height:1.55}
.model .sell{font-size:.8rem;color:var(--good);background:rgba(52,211,153,.08);border-radius:4px;padding:.3rem .5rem;margin-bottom:.35rem;line-height:1.5}
.model .nosay{font-size:.8rem;color:var(--amber);background:rgba(245,158,11,.08);border-radius:4px;padding:.3rem .5rem;line-height:1.5}
.q{font-weight:600;margin:.2rem 0 .4rem}
.opt{display:block;width:100%;text-align:left;border:1.5px solid var(--rule);background:var(--surface);color:var(--text);border-radius:6px;padding:.6rem .8rem;margin:.4rem 0;cursor:pointer;font-size:.92rem;font-family:inherit}
.opt:hover{border-color:var(--teal)}.opt.correct{border-color:var(--good);background:rgba(52,211,153,.1)}.opt.wrong{border-color:var(--bad);background:rgba(244,114,182,.08)}
.fb{font-size:.92rem;margin-top:.6rem;display:none}.fb.show{display:block}
.deriv{margin:1.2rem 0;padding:1rem 1.2rem;border-left:3px solid var(--gold);background:rgba(201,168,76,.05)}
.deriv h3{margin-top:0;color:var(--gold)}
.deriv .result{border-top:1px dashed var(--rule);padding-top:.7rem;margin-top:.8rem;color:var(--text)}
pre.blockmath{background:rgba(17,17,24,.9);border:1px solid rgba(201,168,76,.2);padding:.9rem 1rem;margin:1rem 0;font-family:'Courier New',monospace;font-size:.86rem;overflow-x:auto;white-space:pre}
table.cat{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem}
table.cat th{text-align:left;font-family:'Courier New',monospace;font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;color:var(--teal);padding:.45rem .6rem;border-bottom:1px solid var(--rule)}
table.cat td{padding:.5rem .6rem;border-bottom:1px solid rgba(255,255,255,.05);vertical-align:top}
table.cat td:first-child{color:var(--gold)}
.calc{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.7rem;align-items:end}
.calc label{display:flex;flex-direction:column;font-size:.76rem;color:var(--dim);font-family:'Courier New',monospace}
.calc input{margin-top:.2rem;background:var(--surface);color:var(--text);border:1px solid var(--rule);border-radius:4px;padding:.4rem .5rem;font-family:'Courier New',monospace;font-size:.9rem}
.calc .out{grid-column:1/-1;background:var(--surface);border:1px solid var(--rule);border-radius:4px;padding:.7rem .9rem;font-family:'Courier New',monospace;font-size:.84rem;line-height:1.7;color:var(--text)}
.pt{display:none}body.lang-pt .en{display:none}body.lang-pt div.pt{display:block}body.lang-pt span.pt{display:inline}
.roomnav{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin:2rem 0 0;font-family:'Courier New',monospace;font-size:.72rem}
.roomnav a{color:var(--gold);text-decoration:none;border:1px solid var(--rule);border-radius:4px;padding:.5rem .8rem}
.roomnav a:hover{border-color:var(--gold)}
.langnote{font-size:.78rem;color:var(--dim);font-style:italic;margin-top:.6rem}
.rooms{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1rem;margin:1.2rem 0}
.room-card{display:block;text-decoration:none;color:var(--text);background:var(--card);border:1px solid var(--rule);border-radius:6px;padding:1.2rem 1.3rem;transition:.2s}
.room-card:hover{border-color:rgba(201,168,76,.45);transform:translateY(-2px)}
.room-card .n{font-family:'Courier New',monospace;font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal)}
.room-card .t{font-size:1.15rem;color:var(--gold);margin:.2rem 0}
.room-card .g{font-style:italic;color:var(--dim);font-size:.9rem;margin-bottom:.4rem}
.room-card .s{font-size:.86rem;line-height:1.55}
footer.site{border-top:1px solid var(--rule);text-align:center;padding:2rem 1.2rem;font-family:'Courier New',monospace;font-size:.68rem;letter-spacing:.06em;color:var(--dim);line-height:1.9}
footer.site a{color:var(--gold);text-decoration:none}
"""

JS = """
(function(){
var ROOM=__ROOM__, UI=__UI__;
var lang='en', level='A2', glossOpen=false;
function $(i){return document.getElementById(i);}
function esc(s){return s;}
function renderConcept(){ $('explain').innerHTML=ROOM.concept[level]+'<div class="meta">'+level+' — '+UI[lang].meta[level]+'</div>'; }
function renderGloss(){ $('gloss').innerHTML=ROOM.glossary.map(function(g){return '<div class="gterm"><span>'+g[0]+'</span><span class="ptw">'+g[1]+'</span></div>';}).join('')+'<p class="hint" style="margin-top:.6rem">'+UI[lang].glnote+'</p>'; }
function renderChooser(){ $('models').innerHTML=ROOM.chooser.map(function(m){return '<div class="model"><div class="m">'+m.name+'</div><div class="d">'+m.ans[lang]+'</div><div class="sell">'+m.use[lang]+'</div><div class="nosay">'+m.no[lang]+'</div></div>';}).join(''); }
function renderQuiz(){
  $('qtext').textContent=ROOM.quiz.q[lang];
  $('quiz').innerHTML=ROOM.quiz.opts.map(function(o,i){return '<button class="opt" data-c="'+(i===ROOM.quiz.correct?1:0)+'">'+o[lang]+'</button>';}).join('');
  var fb=$('fb'); fb.classList.remove('show');
  Array.prototype.forEach.call(document.querySelectorAll('.opt'),function(o){o.onclick=function(){
    var ok=this.dataset.c==='1';
    Array.prototype.forEach.call(document.querySelectorAll('.opt'),function(x){if(x.dataset.c==='1')x.classList.add('correct');});
    if(!ok)this.classList.add('wrong');
    fb.classList.add('show'); fb.style.color=ok?'var(--good)':'var(--amber)'; fb.textContent=ok?ROOM.quiz.ok[lang]:ROOM.quiz.no[lang];
  };});
}
function setLang(l){
  lang=l; document.documentElement.lang=l; document.body.classList.toggle('lang-pt',l==='pt');
  Array.prototype.forEach.call(document.querySelectorAll('.langtog button'),function(b){b.classList.toggle('on',b.dataset.lang===l);});
  Array.prototype.forEach.call(document.querySelectorAll('[data-i18n]'),function(el){var k=el.getAttribute('data-i18n');if(UI[l][k]!==undefined)el.innerHTML=UI[l][k];});
  $('l1btn').textContent=glossOpen?UI[l].gl_hide:UI[l].gl_show;
  renderConcept();renderGloss();renderChooser();renderQuiz();
}
Array.prototype.forEach.call(document.querySelectorAll('.langtog button'),function(b){b.onclick=function(){setLang(b.dataset.lang);};});
Array.prototype.forEach.call(document.querySelectorAll('.lvl'),function(b){b.onclick=function(){level=b.dataset.l;Array.prototype.forEach.call(document.querySelectorAll('.lvl'),function(x){x.classList.remove('on');});b.classList.add('on');renderConcept();};});
$('l1btn').onclick=function(){glossOpen=!glossOpen;$('gloss').classList.toggle('show',glossOpen);this.classList.toggle('on',glossOpen);this.textContent=glossOpen?UI[lang].gl_hide:UI[lang].gl_show;};
setLang('en');
})();
__CALC__
"""

def fill(t, m):
    return re.sub(r'%\((\w+)\)s', lambda x: str(m[x.group(1)]), t)

def both(d):
    return '<span class="en">%s</span><span class="pt">%s</span>' % (d['en'], d['pt'])

def jsjson(o):
    return json.dumps(o, ensure_ascii=False).replace('</', '<\\/')

def page(title, desc, body, extra_js="", script_data=None, subject_meta=True):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>%s &middot; Principia Orthogona</title>\n'
            '<meta name="description" content="%s"/>\n<style>%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n'
            % (H.escape(title, quote=False), H.escape(desc, quote=True), CSS, body))

FOOT = """<footer class="site">
  &#9884; Principia Orthogona &middot; Book 7 &middot; The Scientist Gallery &middot;
  <a href="index.html">the gallery</a> &middot; <a href="photochem-index.html">photochemistry branch</a> &middot;
  <a href="../living-book.html">the living book</a><br>
  &copy; 2026 Pablo Nogueira Grossi &middot; G6 LLC &middot; Newark, NJ &middot; g6llc@proton.me
</footer>"""

def nav(home_label_en, home_label_pt):
    return ('<nav class="top"><a class="brand" href="../impa-portal.html">Principia Orthogona</a>'
            '<a href="index.html">&#9884; Scientist Gallery</a><a href="photochem-index.html">Photochemistry branch</a>'
            '<a href="ch-rohatgi-mukherjee.html">Rohatgi-Mukherjee</a>'
            '<div class="langtog"><button data-lang="en" class="on">EN</button><button data-lang="pt">PT</button></div></nav>')

def build_room(i, R):
    ui = UI
    prev_r = ROOMS[i - 1] if i > 0 else None
    next_r = ROOMS[i + 1] if i < len(ROOMS) - 1 else None
    pn = ('<a href="photochem-%s.html">&larr; %s</a>' % (prev_r['slug'], both(dict(en='Room %d &middot; %s' % (prev_r['num'], prev_r['title']['en']), pt='Sala %d &middot; %s' % (prev_r['num'], prev_r['title']['pt']))))) if prev_r else '<a href="photochem-index.html">&larr; %s</a>' % both(dict(en='Photochemistry branch', pt='Ramo de fotoquímica'))
    nn = ('<a href="photochem-%s.html">%s &rarr;</a>' % (next_r['slug'], both(dict(en='Room %d &middot; %s' % (next_r['num'], next_r['title']['en']), pt='Sala %d &middot; %s' % (next_r['num'], next_r['title']['pt']))))) if next_r else '<a href="ch-rohatgi-mukherjee.html">%s &rarr;</a>' % both(dict(en='Back to Rohatgi-Mukherjee', pt='Voltar a Rohatgi-Mukherjee'))
    sources = both(dict(en=ui['en']['src'].format(pages=R['pages'], verify=R['verify']), pt=ui['pt']['src'].format(pages=R['pages'].replace('book pp.', 'pp. do livro '), verify=R['verify'])))
    body = nav('', '') + """
<div class="hero">
<div class="eyebrow">G7 &middot; The Scientist Gallery &middot; %(branch)s &middot; %(room)s %(num)d %(of)s</div>
<h1>%(title)s</h1><div class="tag">%(tag)s</div>
<p class="sub">%(sub)s</p>
</div>
<div class="wrap">
<div class="card">
  <h2><span data-i18n="s1">%(s1)s</span> <span class="pill" data-i18n="s1pill">%(s1pill)s</span></h2>
  <div class="hint" data-i18n="s1hint">%(s1hint)s</div>
  <div class="levels"><button class="lvl on" data-l="A2">A2</button><button class="lvl" data-l="B1">B1</button><button class="lvl" data-l="B2">B2</button><button class="lvl" data-l="C1">C1</button></div>
  <div class="tgt" data-i18n="target">%(target)s</div>
  <div class="explain" id="explain"></div>
  <div class="diag"><span data-i18n="diag">%(diag)s</span><button class="toggle" id="l1btn"></button></div>
  <div class="gloss" id="gloss"></div>
</div>
<div class="card">
  <h2>%(chead)s <span class="pill">%(cpill)s</span></h2>
  <div class="models" id="models"></div>
</div>
<div class="card">
  <h2>%(dhead)s <span class="pill">%(dpill)s</span></h2>
  %(derive)s
  <h3>%(calchead)s</h3>
  %(calchtml)s
</div>
<div class="card">
  <h2><span data-i18n="s4">%(s4)s</span> <span class="pill" data-i18n="s4pill">%(s4pill)s</span></h2>
  <p class="q" id="qtext"></p><div id="quiz"></div><div class="fb" id="fb"></div>
</div>
<div class="card">
  <h2 data-i18n="s5">%(s5)s</h2>
  %(notdo)s
  <p class="langnote">%(langnote)s</p>
</div>
<div class="card">
  <h2 data-i18n="s6">%(s6)s</h2>
  <p style="font-size:.9rem">%(sources)s</p>
  <p style="font-size:.9rem">%(related)s</p>
</div>
<div class="roomnav">%(pn)s %(nn)s</div>
</div>
%(foot)s
<script>
%(js)s
</script>
""" % dict(
        branch=both(dict(en='Photochemistry branch', pt='Ramo de fotoquímica')),
        room='%s' % both(dict(en='Room', pt='Sala')), num=R['num'], of=both(dict(en='of 4', pt='de 4')),
        title=both(R['title']), tag=both(R['tagline']), sub=both(R['sub']),
        s1=ui['en']['s1'], s1pill=ui['en']['s1pill'], s1hint=ui['en']['s1hint'], target=ui['en']['target'], diag=ui['en']['diag'],
        chead=both(R['chooser_head']), cpill=both(R['chooser_pill']), dhead=both(R['derive_head']), dpill=both(R['derive_pill']),
        derive=R['derive_html'], calchead=both(R['calc']['head']), calchtml=R['calc']['html'],
        s4=ui['en']['s4'], s4pill=ui['en']['s4pill'], s5=ui['en']['s5'], s6=ui['en']['s6'],
        notdo=both(R['notdo']).replace('<span class="en">', '<div class="en">').replace('</span><span class="pt">', '</div><div class="pt">')[:-7] + '</div>',
        langnote=both(dict(en=ui['en']['lang_note'], pt=ui['pt']['lang_note'])),
        sources=sources,
        related=both(dict(
            en='Related: <a href="ch-rohatgi-mukherjee.html">Krishna Kamini Rohatgi-Mukherjee</a>, whose textbook this branch reads &middot; <a href="photochem-index.html">the branch index</a>.',
            pt='Relacionado: <a href="ch-rohatgi-mukherjee.html">Krishna Kamini Rohatgi-Mukherjee</a>, cujo livro-texto este ramo lê &middot; <a href="photochem-index.html">o índice do ramo</a>.')),
        pn=pn, nn=nn, foot=FOOT,
        js=JS.replace('__ROOM__', jsjson(dict(concept=R['concept'], glossary=R['glossary'], chooser=R['chooser'], quiz=R['quiz']))).replace('__UI__', jsjson({k: dict(meta=v['meta'], glnote=v['glnote'], gl_show=v['gl_show'], gl_hide=v['gl_hide'], **{x: v[x] for x in ('s1', 's1pill', 's1hint', 'target', 'diag', 's4', 's4pill', 's5', 's6')}) for k, v in ui.items()})).replace('__CALC__', R['calc']['js']),
    )
    title = 'Photochemistry, Room %d: %s' % (R['num'], R['title']['en'])
    desc = R['sub']['en']
    return page(title, desc, body)

IDX = dict(
    title=dict(en="Photochemistry: the instrument rooms", pt="Fotoquímica: as salas de instrumentos"),
    sub=dict(
        en="A branch of the Scientist Gallery that reads one textbook's chapter on tools and techniques, one instrument at a time. Each room is a small tutor in English and Portuguese, with the arithmetic redone and checked by a script that can fail.",
        pt="Um ramo da Galeria de Cientistas que lê o capítulo de ferramentas e técnicas de um livro-texto, um instrumento por vez. Cada sala é um pequeno tutor em inglês e português, com a aritmética refeita e conferida por um script que pode falhar."),
)

def build_index():
    cards = ''.join(
        '<a class="room-card" href="photochem-%s.html"><div class="n">%s</div><div class="t">%s</div><div class="g">%s</div><div class="s">%s</div></a>'
        % (R['slug'], both(dict(en='Room %d' % R['num'], pt='Sala %d' % R['num'])), both(R['title']), both(R['tagline']), both(R['sub'])) for R in ROOMS)
    body = nav('', '') + fill("""
<div class="hero">
<div class="eyebrow">G7 &middot; The Scientist Gallery &middot; %(branch)s</div>
<h1>%(title)s</h1>
<p class="sub">%(sub)s</p>
</div>
<div class="wrap">
<div class="card">
<h2>%(h1)s</h2>
<div class="en">
<p>The source is Chapter 10, <em>Tools and Techniques</em>, of K. K. Rohatgi-Mukherjee's <em>Fundamentals of Photochemistry</em> (revised edition), pp.298&ndash;321, read from page scans. The chapter describes how photochemists count photons, read emission, catch short-lived species and use lasers. Each room takes one group of instruments, rewrites the idea at four levels of English, gives a Portuguese key-term list that tells you whether your gap is the science or the English, sets out which tool answers which question, and then <strong>redoes the book's arithmetic and adds derivations of our own</strong>, all checked by a script with controls that must fail.</p>
<p>The book is the textbook of the scientist profiled in <a href="ch-rohatgi-mukherjee.html">Krishna Kamini Rohatgi-Mukherjee</a>. That profile rests on a biographical memoir; this branch rests on her textbook. Neither reads her doctoral thesis, which was not available.</p>
</div>
<div class="pt">
<p>A fonte é o Capítulo 10, <em>Tools and Techniques</em>, do livro <em>Fundamentals of Photochemistry</em> (edição revista) de K. K. Rohatgi-Mukherjee, pp.298&ndash;321, lido de imagens de página. O capítulo descreve como fotoquímicos contam fótons, leem emissão, capturam espécies de vida curta e usam lasers. Cada sala trata de um grupo de instrumentos, reescreve a ideia em quatro níveis de inglês, traz uma lista de termos em português que mostra se a dificuldade é a ciência ou o inglês, indica qual ferramenta responde a qual pergunta e então <strong>refaz a aritmética do livro e acrescenta derivações próprias</strong>, tudo verificado por um script com controles que devem falhar.</p>
<p>O livro é o livro-texto da cientista do perfil <a href="ch-rohatgi-mukherjee.html">Krishna Kamini Rohatgi-Mukherjee</a>. Aquele perfil se apoia numa memória biográfica; este ramo se apoia no livro. Nenhum dos dois lê a tese de doutorado, que não estava disponível.</p>
</div>
</div>
<div class="rooms">%(cards)s</div>
<div class="card">
<h2>%(h2)s</h2>
<div class="en">
<p>Everything below is produced by the verify scripts, one per room, and the branch's own script runs all four.</p>
<p><strong>Differences between the book and our recheck.</strong> Page 315 prints that the flash duration sets the <em>upper</em> limit to the lifetime of detectable transients; a simulation says it sets the <em>lower</em> limit, so a long flash loses short lifetimes (Room 4, section 3.2). The power density of 1e19 W/cm&sup2; on page 317 is reachable at a diffraction-limited spot with the picosecond pulses of page 320, but not with a nanosecond Q-switched pulse of a few joules (Room 3, section 3.6). The sector method's inflection is real but sits several times beyond the time to reach steady state, so it needs a model fit (Room 4, section 3.4).</p>
<p><strong>Small roundings.</strong> The book's 2.5e19 quanta from a 100 J flash is 3.5 % above the exact 2.42e19; its <code>hc</code> is 0.68 % high; neither changes any conclusion. &quot;About 20 % efficiency&quot; for doubling does not say energy or photons, and as energy it is 10 % of the photons.</p>
<p><strong>Confirmed.</strong> The 12 % in-band share at 6000 K, the detection limit of about 1e-8 mol/L, 99 % absorption at absorbance 2, the phase relation <code>tan&thinsp;&theta; = 2&pi;&nu;&tau;</code>, the 1/&radic;2 at high sector speed, and 694 to 347 nm on doubling.</p>
</div>
<div class="pt">
<p>Tudo abaixo é produzido pelos scripts de verificação, um por sala; o script do ramo roda os quatro.</p>
<p><strong>Diferenças entre o livro e nossa reconferência.</strong> A p.315 imprime que a duração do flash fixa o limite <em>superior</em> do tempo de vida detectável; uma simulação diz que fixa o limite <em>inferior</em> (Sala 4, seção 3.2). A densidade de potência de 1e19 W/cm&sup2; da p.317 é alcançável num ponto limitado por difração com os pulsos de picossegundos da p.320, mas não com um pulso de nanossegundos com chave Q de poucos joules (Sala 3, seção 3.6). A inflexão do método do setor é real mas fica várias vezes além do tempo de chegada ao estado estacionário (Sala 4, seção 3.4).</p>
<p><strong>Pequenos arredondamentos.</strong> Os 2.5e19 quanta do livro estão 3.5 % acima do valor exato 2.42e19; seu <code>hc</code> está 0.68 % alto; nenhum altera conclusão. &quot;Cerca de 20 % de eficiência&quot; na dobra não diz se é energia ou fótons.</p>
<p><strong>Confirmado.</strong> Os 12 % na faixa a 6000 K, o limite de detecção de cerca de 1e-8 mol/L, 99 % de absorção em absorbância 2, a relação de fase <code>tan&thinsp;&theta; = 2&pi;&nu;&tau;</code>, o 1/&radic;2 em alta velocidade do setor e 694 para 347 nm na dobra.</p>
</div>
</div>
<div class="card">
<h2>%(h3)s</h2>
<div class="en">
<p>This is not a vendor guide, not a laboratory manual, and not a substitute for the textbook; the book is paraphrased and cited by page and none of its text is reproduced. The Portuguese was drafted by Claude and has not been reviewed by a native speaker. It extends no claim about any instrument's current specifications. Branch checks: <code>book7/photochem-index-verify.py</code>.</p>
</div>
<div class="pt">
<p>Este ramo não é guia de fabricante, nem manual de laboratório, nem substitui o livro-texto; o livro é parafraseado e citado por página, sem reproduzir seu texto. O português foi redigido por Claude e não foi revisado por falante nativo. Nada aqui afirma especificações atuais de instrumentos. Verificações do ramo: <code>book7/photochem-index-verify.py</code>.</p>
</div>
</div>
</div>
%(foot)s
<script>
(function(){
function setLang(l){document.documentElement.lang=l;document.body.classList.toggle('lang-pt',l==='pt');
 Array.prototype.forEach.call(document.querySelectorAll('.langtog button'),function(b){b.classList.toggle('on',b.dataset.lang===l);});}
Array.prototype.forEach.call(document.querySelectorAll('.langtog button'),function(b){b.onclick=function(){setLang(b.dataset.lang);};});
})();
</script>
""", dict(branch=both(dict(en='Photochemistry branch', pt='Ramo de fotoquímica')), title=both(IDX['title']), sub=both(IDX['sub']),
           h1=both(dict(en='What this branch is', pt='O que é este ramo')), cards=cards,
           h2=both(dict(en='What the rooms found', pt='O que as salas encontraram')),
           h3=both(dict(en='What it is not', pt='O que não é')), foot=FOOT))
    return page('Photochemistry: the instrument rooms', IDX['sub']['en'], body)

def outputs():
    out = {'photochem-index.html': build_index()}
    for i, R in enumerate(ROOMS):
        out['photochem-%s.html' % R['slug']] = build_room(i, R)
    return out

GEN = re.compile(r'<!--po-([a-z]+)-->.*?<!--/po-\1-->', re.S)

def main():
    outs = outputs()
    if '--check' in sys.argv:
        bad = 0
        for name, txt in outs.items():
            p = os.path.join(OUT, name)
            cur = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
            if _norm(cur) != _norm(txt):
                print('DIFFERS', name); bad += 1
        sys.exit(1 if bad else 0)
    for name, txt in outs.items():
        p = os.path.join(OUT, name)
        if os.path.exists(p):
            old = open(p, encoding='utf-8').read()
            blocks = {m.group(1): m.group(0) for m in GEN.finditer(old)}
            # re-insert the generated blocks where the generators put them: subject (head + hero), gss/run/related before the footer
            for k in ('gss', 'run', 'related'):
                if k in blocks:
                    txt = txt.replace('<footer class="site">', blocks[k] + '\n<footer class="site">', 1)
        open(p, 'w', encoding='utf-8').write(txt)
        print('wrote', os.path.relpath(p, ROOT))

def _norm(t):
    return [l.rstrip() for l in GEN.sub('', t).splitlines() if l.strip()]

if __name__ == '__main__':
    main()
