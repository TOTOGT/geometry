# -*- coding: utf-8 -*-
"""Room 1: light sources and actinometry. Numbers printed here are produced by book7/photochem-light-sources-verify.py."""
ROOM = dict(
    slug="light-sources", num=1,
    title=dict(en="Light sources and actinometry", pt="Fontes de luz e actinometria"),
    tagline=dict(en="Light you can count", pt="Luz que se pode contar"),
    sub=dict(
        en="Every photochemical result is a ratio against the photons that arrived. This room is about how those photons get counted: detectors, standard lamps, and chemical actinometers.",
        pt="Todo resultado fotoquímico é uma razão em relação aos fótons que chegaram. Esta sala trata de como esses fótons são contados: detectores, lâmpadas-padrão e actinômetros químicos."),
    concept=dict(
        A2="A photochemical reaction needs light. Each photon, a very small packet of light, can change one molecule. To study the reaction, we must know how many photons arrive each second. A lamp does not tell us this number. So we measure it. We can use a detector. Or we can use a special chemical that changes in a known way when light hits it. This chemical method is called actinometry.",
        B1="A photochemical reaction starts when a molecule absorbs a photon, so the first thing to know is how many photons reach the sample each second. A lamp does not come with this number. Actinometry measures it with a reaction whose quantum yield is already known: the number of molecules that change for each photon absorbed. If you measure how much product formed, and you know the yield and the fraction of light that was absorbed, you can calculate the photons that arrived.",
        B2="The absolute photon flux can be fixed in two ways: with a detector calibrated against a standard lamp (thermopile, photocell, photomultiplier), or chemically, by irradiating an actinometer whose quantum yield has been established against a standard source. Because the quantum yield is the rate of reaction divided by the rate of absorption, the incident flux follows from the amount of product, the yield, the exposure time and the fraction of light the solution absorbed. Each actinometer is only valid inside its stated wavelength range.",
        C1="Quantitative photochemistry reduces to knowing the rate of photon absorption. Detectors respond either to total energy (thermopile, bolometer) or to a photocurrent whose sensitivity depends on wavelength (photocell, photomultiplier), so each needs calibration against a standard lamp of known colour temperature. A chemical actinometer carries that calibration into the reaction cell itself, which removes the geometric error between lamp, detector and sample; the price is that it is trustworthy only inside its tabulated wavelength range and only when the absorbed fraction is measured or made close to one."),
    glossary=[
        ("photon", "fóton"), ("quantum yield", "rendimento quântico"), ("actinometry", "actinometria"),
        ("einstein (one mole of photons)", "einstein (um mol de fótons)"), ("absorbance", "absorbância"),
        ("thermopile", "termopilha"), ("photomultiplier", "fotomultiplicadora"),
        ("incident light flux", "fluxo de luz incidente"), ("colour temperature", "temperatura de cor"),
        ("cuvette", "cubeta"), ("ferrioxalate", "ferrioxalato")],
    chooser_head=dict(en="2 · Which tool for which question", pt="2 · Qual ferramenta para qual pergunta"),
    chooser_pill=dict(en="use-it-when", pt="quando usar"),
    chooser=[
        dict(name="Thermopile / bolometer", ans=dict(en="Total energy per second in the beam, whatever the colour.", pt="Energia total por segundo no feixe, seja qual for a cor."),
             use=dict(en="You need an absolute energy and the beam is one colour, set by a filter or monochromator.", pt="Você precisa de uma energia absoluta e o feixe tem uma só cor, definida por filtro ou monocromador."),
             no=dict(en="It cannot tell colours apart: it adds up everything that arrives (book p.299).", pt="Não distingue cores: soma tudo que chega (livro p.299).")),
        dict(name="Photocell / photomultiplier", ans=dict(en="Relative intensity, fast, and for very weak light.", pt="Intensidade relativa, rápida, e para luz muito fraca."),
             use=dict(en="Light is weak or changing quickly, and you can calibrate the detector against a thermopile or a secondary standard.", pt="A luz é fraca ou varia rápido, e você pode calibrar o detector contra uma termopilha ou um padrão secundário."),
             no=dict(en="Its sensitivity depends on wavelength, so on its own it gives no absolute count (book p.299).", pt="Sua sensibilidade depende do comprimento de onda; sozinho, não dá uma contagem absoluta (livro p.299).")),
        dict(name="Ferrioxalate", ans=dict(en="Absolute photon flux from 250 to 577 nm. Yield about 1.2 up to 365 nm, 1.1 at longer wavelengths.", pt="Fluxo absoluto de fótons de 250 a 577 nm. Rendimento cerca de 1,2 até 365 nm, 1,1 em comprimentos maiores."),
             use=dict(en="Ultraviolet to green, and you can read an absorbance at 510 nm after adding o-phenanthroline.", pt="Do ultravioleta ao verde, e você consegue ler uma absorbância a 510 nm após adicionar o-fenantrolina."),
             no=dict(en="Nothing beyond 577 nm or below 250 nm (book p.301).", pt="Nada além de 577 nm ou abaixo de 250 nm (livro p.301).")),
        dict(name="Reinecke's salt", ans=dict(en="Absolute photon flux from 316 to 735 nm, including the red. Yield 0.27 to 0.3.", pt="Fluxo absoluto de fótons de 316 a 735 nm, incluindo o vermelho. Rendimento 0,27 a 0,3."),
             use=dict(en="You work in the visible or red, and the solution can absorb nearly all of the light (about 99 %).", pt="Você trabalha no visível ou no vermelho, e a solução pode absorver quase toda a luz (cerca de 99 %)."),
             no=dict(en="Its yield is about a quarter of ferrioxalate's, so the same photon dose gives about a quarter of the product (arithmetic: 1.2 / 0.3 = 4).", pt="Seu rendimento é cerca de um quarto do ferrioxalato, então a mesma dose de fótons gera cerca de um quarto do produto (conta: 1,2 / 0,3 = 4).")),
        dict(name="Uranyl oxalate", ans=dict(en="Photon flux from 208 to 435 nm. Yield about 0.5.", pt="Fluxo de fótons de 208 a 435 nm. Rendimento cerca de 0,5."),
             use=dict(en="Mainly of historical interest; the book says it needs long exposures and careful oxalate titrations.", pt="Principalmente de interesse histórico; o livro diz que exige longas exposições e titulações cuidadosas de oxalato."),
             no=dict(en="Not for anything beyond 435 nm (book p.301).", pt="Não serve para nada além de 435 nm (livro p.301).")),
        dict(name="Malachite green leucocyanide", ans=dict(en="Strongest in the 220 to 300 nm range, yield 0.91; the product absorbs strongly at 662 nm.", pt="Mais útil na faixa de 220 a 300 nm, rendimento 0,91; o produto absorve fortemente a 662 nm."),
             use=dict(en="Deep ultraviolet, where the leuco compound itself absorbs strongly.", pt="Ultravioleta profundo, onde o próprio composto leuco absorve fortemente."),
             no=dict(en="The book gives no hard range for it, only where it is most useful (p.301-302).", pt="O livro não dá uma faixa rígida, só onde é mais útil (p.301-302).")),
    ],
    derive_head=dict(en="3 · Derived and checked", pt="3 · Derivado e verificado"),
    derive_pill=dict(en="our arithmetic, not the book's", pt="nossa aritmética, não a do livro"),
    derive_html="""
<div class="deriv"><h3><span class="en">3.1 What an einstein costs</span><span class="pt">3.1 Quanto custa um einstein</span></h3>
<div class="en"><p>A photon of wavelength &lambda; carries <code>E = hc/&lambda;</code>. Multiply by Avogadro's number and you get the energy of one einstein, a mole of photons. With the exact constants:</p>
<table class="cat"><tr><th>wavelength</th><th>kJ per einstein</th><th>where it comes from</th></tr>
<tr><td>253.7 nm</td><td>471.5</td><td>mercury resonance line (book p.298)</td></tr>
<tr><td>365 nm</td><td>327.7</td><td>mercury line used with filters (book p.298)</td></tr>
<tr><td>400 nm</td><td>299.1</td><td>wavelength of the flash example (book p.316)</td></tr>
<tr><td>577 nm</td><td>207.3</td><td>upper end of the ferrioxalate range (book p.301)</td></tr></table>
<p class="result">The book writes <code>hc</code> as 2e-16 J nm. The exact value is 1.986e-16 J nm, so the book's rounding is +0.68 %. That is harmless for a flux, and it is stated here so nobody has to wonder.</p></div>
<div class="pt"><p>Um fóton de comprimento de onda &lambda; carrega <code>E = hc/&lambda;</code>. Multiplicando pelo número de Avogadro obtém-se a energia de um einstein, um mol de fótons: 471.5 kJ a 253.7 nm, 327.7 kJ a 365 nm, 299.1 kJ a 400 nm e 207.3 kJ a 577 nm.</p>
<p class="result">O livro escreve <code>hc</code> como 2e-16 J nm. O valor exato é 1.986e-16 J nm; o arredondamento do livro é +0.68 %. Isso é inofensivo para um fluxo, e fica registrado aqui.</p></div></div>

<div class="deriv"><h3><span class="en">3.2 How much of the light is absorbed</span><span class="pt">3.2 Quanta luz é absorvida</span></h3>
<div class="en"><p>If the solution has absorbance A, it absorbs the fraction <code>f = 1 &minus; 10<sup>&minus;A</sup></code> of the light. The book asks the Reinecke solution to absorb nearly 99 % (p.302). That is exactly <code>A = 2</code>. An absorbance of 1 would absorb only 90 %, and A = 0.301 only half.</p>
<p class="result">Why it matters: the actinometer formula needs the absorbed fraction, not the incident light. Skip it and the flux is wrong by 1/f.</p></div>
<div class="pt"><p>Se a solução tem absorbância A, ela absorve a fração <code>f = 1 &minus; 10<sup>&minus;A</sup></code> da luz. O livro pede que a solução de Reinecke absorva quase 99 % (p.302): isso é exatamente <code>A = 2</code>. Absorbância 1 absorveria só 90 %, e A = 0.301 apenas metade.</p>
<p class="result">Por que importa: a fórmula do actinômetro precisa da fração absorvida, não da luz incidente. Sem ela, o fluxo erra por 1/f.</p></div></div>

<div class="deriv"><h3><span class="en">3.3 From product to photons, with a worked example</span><span class="pt">3.3 Do produto aos fótons, com um exemplo</span></h3>
<div class="en"><p>From the definition of quantum yield (book p.301), <code>&phi; = (molecules formed per second) / (photons absorbed per second)</code>. Solve for the incident flux over an exposure t:</p>
<pre class="blockmath">I0 = n / (&phi; &middot; f &middot; t)        n = moles of product, f = 1 - 10^-A</pre>
<p>Worked example, with a <strong>hypothetical</strong> reading (not a measurement): 3.0e-8 mol of product in 60 s at 366 nm, &phi; = 1.2 (the book's value for 254&ndash;365 nm), A = 2 so f = 0.99.</p>
<pre class="blockmath">I0 = 4.21e-10 einstein/s = 2.54e14 photons/s = 0.138 mW</pre>
<p class="result">What each shortcut costs: forgetting the absorbed fraction changes the answer by -1.0 % here; using &phi; = 1 instead of 1.2 changes it by +20.0 %. If the solution had absorbed only half the light (A = 0.301), forgetting f would be a factor of 2.</p></div>
<div class="pt"><p>Da definição de rendimento quântico (livro p.301), <code>&phi; = (moléculas formadas por segundo) / (fótons absorvidos por segundo)</code>. Isolando o fluxo incidente numa exposição t: <code>I0 = n / (&phi; f t)</code>.</p>
<p>Exemplo com leitura <strong>hipotética</strong> (não é medição): 3.0e-8 mol de produto em 60 s a 366 nm, &phi; = 1.2, A = 2, f = 0.99: <code>I0 = 4.21e-10 einstein/s = 2.54e14 fótons/s = 0.138 mW</code>.</p>
<p class="result">O que cada atalho custa: esquecer a fração absorvida muda o resultado em -1.0 %; usar &phi; = 1 em vez de 1.2 muda em +20.0 %. Se a solução absorvesse só metade da luz (A = 0.301), esquecer f seria um erro de fator 2.</p></div></div>
""",
    calc=dict(
        head=dict(en="Try it: flux from an actinometer reading", pt="Experimente: fluxo a partir de uma leitura de actinômetro"),
        html="""<div class="calc"><label>&lambda; (nm)<input id="c_nm" type="number" value="366" step="1"></label>
<label>product n (mol)<input id="c_n" type="text" value="3.0e-8"></label>
<label>&phi;<input id="c_phi" type="number" value="1.2" step="0.01"></label>
<label>exposure t (s)<input id="c_t" type="number" value="60" step="1"></label>
<label>absorbance A<input id="c_A" type="number" value="2" step="0.1"></label>
<div class="out" id="c_out"></div></div>""",
        js="""
(function(){
 var h=6.62607015e-34,c=299792458,NA=6.02214076e23;
 function run(){
  var nm=parseFloat(document.getElementById('c_nm').value),n=parseFloat(document.getElementById('c_n').value),
      phi=parseFloat(document.getElementById('c_phi').value),t=parseFloat(document.getElementById('c_t').value),A=parseFloat(document.getElementById('c_A').value);
  var out=document.getElementById('c_out');
  if(!(nm>0&&n>0&&phi>0&&t>0&&A>=0)){out.textContent='-';return;}
  var f=1-Math.pow(10,-A),I0=n/(phi*f*t),ph=I0*NA,Eph=h*c/(nm*1e-9),P=ph*Eph;
  out.innerHTML='f = '+f.toFixed(4)+' &middot; I0 = '+I0.toExponential(2)+' einstein/s &middot; '+ph.toExponential(2)+' photons/s &middot; '+(P*1e3).toFixed(3)+' mW &middot; '+(NA*Eph/1e3).toFixed(1)+' kJ per einstein';
 }
 ['c_nm','c_n','c_phi','c_t','c_A'].forEach(function(i){document.getElementById(i).addEventListener('input',run);});run();
})();"""),
    quiz=dict(
        q=dict(en="Your experiment runs at 650 nm in the red and you want an absolute photon flux from a chemical actinometer. Which of the four in this room's table covers it?",
               pt="Seu experimento roda a 650 nm, no vermelho, e você quer um fluxo absoluto de fótons com um actinômetro químico. Qual dos quatro da tabela desta sala cobre essa faixa?"),
        opts=[dict(en="Ferrioxalate", pt="Ferrioxalato"), dict(en="Uranyl oxalate", pt="Oxalato de uranila"),
              dict(en="Reinecke's salt", pt="Sal de Reinecke"), dict(en="Malachite green leucocyanide", pt="Leucocianeto de verde de malaquita")],
        correct=2,
        ok=dict(en="Correct. Reinecke's salt is the one of the four with a printed range reaching 735 nm. Remember its yield is only about 0.3, so expect less product per photon, and make the solution absorb about 99 %.",
                pt="Correto. O sal de Reinecke é o único dos quatro com faixa impressa chegando a 735 nm. Lembre que seu rendimento é só cerca de 0,3, então haverá menos produto por fóton; faça a solução absorver cerca de 99 %."),
        no=dict(en="Not quite. Ferrioxalate stops at 577 nm, uranyl oxalate at 435 nm, and the leuco dye is a deep-ultraviolet tool. Only Reinecke's salt (316 to 735 nm) reaches 650 nm.",
                pt="Ainda não. O ferrioxalato para em 577 nm, o oxalato de uranila em 435 nm, e o corante leuco é para o ultravioleta profundo. Só o sal de Reinecke (316 a 735 nm) chega a 650 nm.")),
    notdo=dict(en="""<p>This room does not teach a laboratory procedure and is not a vendor guide. Every <em>book</em> statement is cited by page and was read from page scans of one textbook; every <em>number printed in the derivations</em> is produced by the verify script. Four things are open:</p>
<p><strong>Absorbance of the ferrioxalate solution.</strong> The book recommends 0.006 M for wavelengths up to 400 nm and 0.15 M for longer ones. It gives no extinction coefficient, so whether those solutions absorb enough at a particular wavelength is not checked here.</p>
<p><strong>The analysis step.</strong> The colour reaction with o-phenanthroline is mentioned by the book (an absorbance at 510 nm compared with a standard). Calibration of that step is not covered.</p>
<p><strong>Yields.</strong> The quantum yields and ranges in the table are the book's printed values, not re-measured, and later literature may differ.</p>
<p><strong>Portuguese.</strong> The Portuguese text was drafted by Claude and has not been reviewed by a native speaker.</p>""",
               pt="""<p>Esta sala não ensina procedimento de laboratório nem é guia de fabricante. Cada afirmação do <em>livro</em> é citada por página e foi lida de imagens de página de um único livro-texto; cada <em>número impresso nas derivações</em> é produzido pelo script de verificação. Quatro pontos ficam em aberto: a absorbância da solução de ferrioxalato (o livro não dá coeficiente de extinção); a etapa de análise com o-fenantrolina (calibração não coberta); os rendimentos, que são os valores impressos no livro, não remedidos; e o português, redigido por Claude e ainda sem revisão de falante nativo.</p>"""),
    verify="photochem-light-sources-verify.py",
    pages="book pp.298-302",
)
