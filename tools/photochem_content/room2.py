# -*- coding: utf-8 -*-
"""Room 2: the spectrometer (emission, quantum yield, lifetime). Numbers are produced by book7/photochem-spectrometer-verify.py."""
ROOM = dict(
    slug="spectrometer", num=2,
    title=dict(en="The spectrometer", pt="O espectrômetro"),
    tagline=dict(en="Reading the light that comes back", pt="Lendo a luz que volta"),
    sub=dict(
        en="Absorb a photon, wait, emit another: what colour, how much, and how long after? This room covers the spectrofluorimeter and its relatives, from emission spectra to nanosecond lifetimes.",
        pt="Absorver um fóton, esperar, emitir outro: de que cor, quanto e quanto tempo depois? Esta sala cobre o espectrofluorímetro e seus parentes, de espectros de emissão a tempos de vida de nanossegundos."),
    concept=dict(
        A2="Some molecules send out light after they take in light. This is called fluorescence. A spectrofluorimeter has two colour selectors. One chooses the colour that goes in. The other chooses the colour that comes out. If you change one and keep the other fixed, you draw a curve. Other measurements tell you how bright the light is, and how long it lasts. It often lasts only a few billionths of a second.",
        B1="A spectrofluorimeter measures the light a molecule emits after absorbing light. It has two monochromators: one picks the exciting colour, the other analyses the emitted colour. Scanning the second gives the emission spectrum; scanning the first while watching one emission colour gives the excitation spectrum. Comparing the total emission with that of a standard under the same conditions gives the quantum yield, and observing how the emission dies away gives the lifetime.",
        B2="Emission characteristics are expressed in three kinds of measurement: spectra (emission and excitation), quantum yields, and decay constants. A true emission spectrum needs the detector-and-monochromator response corrected against a standard lamp or a standard emitter. Fluorescence quantum yield is obtained relative to a reference of known yield, with equal absorbance and geometry, by comparing integrated emission. Lifetimes come from pulse methods, which watch the decay directly, or from phase-shift methods, which excite with modulated light and measure how far the emission lags.",
        C1="The instrument couples an excitation monochromator and an emission monochromator to a detector whose spectral response must itself be calibrated (standard lamp of known colour temperature, a secondary standard emitter, or a quantum counter that flattens the response). Relative quantum yields follow from integrated, corrected spectra of sample and reference at matched absorbance and geometry, with dilute solutions chosen to avoid inner-filter distortion and re-absorption. Excited-state lifetimes, which turn quantum yields into rate constants, are measured either in the time domain (phosphoroscope, gated detection, single-photon counting) or the frequency domain, where the phase lag of the emission against modulated excitation satisfies tan&nbsp;&theta;&nbsp;=&nbsp;&omega;&tau;."),
    glossary=[
        ("fluorescence", "fluorescência"), ("phosphorescence", "fosforescência"), ("emission spectrum", "espectro de emissão"),
        ("excitation spectrum", "espectro de excitação"), ("monochromator", "monocromador"), ("quantum yield", "rendimento quântico"),
        ("excited-state lifetime", "tempo de vida do estado excitado"), ("phase shift", "defasagem"), ("modulated light", "luz modulada"),
        ("quantum counter", "contador quântico"), ("photon counting", "contagem de fótons"), ("chopper / rotating sector", "obturador rotativo (chopper)"),
        ("reference standard", "padrão de referência")],
    chooser_head=dict(en="2 · Which measurement for which question", pt="2 · Qual medição para qual pergunta"),
    chooser_pill=dict(en="use-it-when", pt="quando usar"),
    chooser=[
        dict(name="Emission spectrum", ans=dict(en="Which colours does the molecule give out, with the excitation colour held fixed?", pt="Que cores a molécula emite, com a cor de excitação fixa?"),
             use=dict(en="You want the shape and peak of the emission.", pt="Você quer a forma e o pico da emissão."),
             no=dict(en="It is not a true spectrum until the detector's wavelength response is corrected (book p.302).", pt="Não é um espectro verdadeiro até a resposta do detector ser corrigida (livro p.302).")),
        dict(name="Excitation spectrum", ans=dict(en="Which absorbed colours lead to this emission?", pt="Quais cores absorvidas levam a esta emissão?"),
             use=dict(en="You want to know which absorption bands feed the emitting state; the emission maximum is held and the exciting colour is scanned.", pt="Você quer saber quais bandas de absorção alimentam o estado emissor; fixa-se o máximo de emissão e varre-se a cor de excitação."),
             no=dict(en="It does not give the emission colour itself.", pt="Não dá a cor da emissão em si.")),
        dict(name="Relative quantum yield", ans=dict(en="What fraction of absorbed photons come back as fluorescence?", pt="Que fração dos fótons absorvidos volta como fluorescência?"),
             use=dict(en="You have a reference of known yield, the same absorbance and the same geometry (book Eq. 10.1).", pt="Você tem uma referência de rendimento conhecido, a mesma absorbância e a mesma geometria (livro Eq. 10.1)."),
             no=dict(en="It is only as good as the reference and the dilution; re-absorption must be corrected if the bands overlap (book p.304).", pt="Só é tão bom quanto a referência e a diluição; a reabsorção precisa ser corrigida se as bandas se sobrepõem (livro p.304).")),
        dict(name="Quantum counter", ans=dict(en="A screen that makes the detector respond to photons equally at every colour.", pt="Uma tela que faz o detector responder igualmente a fótons de qualquer cor."),
             use=dict(en="You want to flatten the detector's wavelength dependence; the book names rhodamine B in glycerol (3 g/L) and fluorescein in 0.01 N Na2CO3.", pt="Você quer achatar a dependência espectral do detector; o livro cita rodamina B em glicerol (3 g/L) e fluoresceína em Na2CO3 0,01 N."),
             no=dict(en="It assumes the dye's own yield does not change with exciting wavelength (book p.304).", pt="Supõe que o rendimento do próprio corante não muda com o comprimento de onda de excitação (livro p.304).")),
        dict(name="Phosphoroscope / chopper", ans=dict(en="Long-lived emission, with the short fluorescence cut off.", pt="Emissão de vida longa, com a fluorescência curta cortada."),
             use=dict(en="You want phosphorescence in the presence of fluorescence; rotating sectors block the instant emission.", pt="Você quer fosforescência na presença de fluorescência; setores rotativos bloqueiam a emissão instantânea."),
             no=dict(en="A mechanical shutter cannot reach nanoseconds; the book moves to Kerr cells and electronic gating for that (p.306).", pt="Um obturador mecânico não chega a nanossegundos; o livro passa a células de Kerr e a porteamento eletrônico (p.306).")),
        dict(name="Phase fluorimeter", ans=dict(en="Lifetime from the lag of the emission behind modulated excitation.", pt="Tempo de vida a partir do atraso da emissão em relação à excitação modulada."),
             use=dict(en="Lifetimes of order 1e-8 to 1e-10 s, with modulation at 2 to 20 MHz (book p.310).", pt="Tempos de vida da ordem de 1e-8 a 1e-10 s, com modulação de 2 a 20 MHz (livro p.310)."),
             no=dict(en="At the short end the phase is tiny (0.72 degrees at 20 MHz and 0.1 ns, derived below), so detection must be sensitive.", pt="No extremo curto a fase é minúscula (0.72 grau a 20 MHz e 0.1 ns, derivado abaixo); a detecção precisa ser sensível.")),
        dict(name="Single-photon counting", ans=dict(en="Decay curve from the arrival time of individual photons.", pt="Curva de decaimento a partir do tempo de chegada de fótons individuais."),
             use=dict(en="Very weak light; it removes noise and stray light by pulse-height discrimination (book p.308).", pt="Luz muito fraca; elimina ruído e luz parasita por discriminação de altura de pulso (livro p.308)."),
             no=dict(en="The count rate must stay low. Our derivation below shows why: at a detection probability p per flash the lifetime reads short by a factor 1/(1+p).", pt="A taxa de contagem precisa ser baixa. Nossa derivação abaixo mostra por quê: com probabilidade de detecção p por flash o tempo de vida sai curto por um fator 1/(1+p).")),
        dict(name="Right-angle, front-face, end-on", ans=dict(en="Where to put the detector relative to the exciting beam.", pt="Onde pôr o detector em relação ao feixe de excitação."),
             use=dict(en="Dilute solutions: observe at 90 degrees. Optically dense ones: 45 or 180 degrees (book p.302).", pt="Soluções diluídas: observar a 90 graus. Opticamente densas: 45 ou 180 graus (livro p.302)."),
             no=dict(en="Geometry errors do not vanish by themselves; use filters in the exciting and measuring beams.", pt="Erros de geometria não somem sozinhos; use filtros nos feixes de excitação e de medida.")),
    ],
    derive_head=dict(en="3 · Derived and checked", pt="3 · Derivado e verificado"),
    derive_pill=dict(en="our arithmetic, not the book's", pt="nossa aritmética, não a do livro"),
    derive_html="""
<div class="deriv"><h3><span class="en">3.1 Relative quantum yield and why the sample must be dilute</span><span class="pt">3.1 Rendimento quântico relativo e por que a amostra deve ser diluída</span></h3>
<div class="en"><p>The emission signal is <code>F = &phi; &middot; I<sub>a</sub> &middot; G</code>: yield times absorbed light times a geometry factor. For a sample and a reference with the same absorbed light and geometry the book (Eq. 10.1) gets <code>&phi;<sub>s</sub> / &phi;<sub>ref</sub> = F<sub>s</sub> / F<sub>ref</sub></code>. If the absorbances differ, the absorbed light is <code>f = 1 &minus; 10<sup>&minus;A</sup></code>, so</p>
<pre class="blockmath">&phi;_s = &phi;_ref &middot; (F_s / F_ref) &middot; (f_ref / f_s)</pre>
<p>Hypothetical example: &phi;<sub>ref</sub> = 0.50, F ratio 0.84, equal absorbance 0.030 gives &phi;<sub>s</sub> = 0.420.</p>
<p class="result">Why the book wants OD around 0.03: the shortcut of using A in place of f in the ratio is off by +1.7 % for absorbances 0.030 and 0.045, but by +16.0 % for 0.30 and 0.45. Dilution keeps the shortcut honest.</p></div>
<div class="pt"><p>O sinal de emissão é <code>F = &phi; I<sub>a</sub> G</code>. Com mesma luz absorvida e mesma geometria, o livro (Eq. 10.1) obtém <code>&phi;<sub>s</sub> / &phi;<sub>ref</sub> = F<sub>s</sub> / F<sub>ref</sub></code>. Se as absorbâncias diferem, usa-se <code>f = 1 &minus; 10<sup>&minus;A</sup></code>: <code>&phi;_s = &phi;_ref (F_s/F_ref)(f_ref/f_s)</code>. Exemplo hipotético: &phi;<sub>ref</sub> = 0.50, razão de F 0.84, absorbância 0.030 em ambos: &phi;<sub>s</sub> = 0.420.</p>
<p class="result">Por que o livro quer DO perto de 0.03: usar A no lugar de f erra +1.7 % para absorbâncias 0.030 e 0.045, mas +16.0 % para 0.30 e 0.45. A diluição mantém o atalho honesto.</p></div></div>

<div class="deriv"><h3><span class="en">3.2 The phase shift, by integrating the equation</span><span class="pt">3.2 A defasagem, integrando a equação</span></h3>
<div class="en"><p>The emission follows <code>dI/dt = &minus;kI + k J(t)</code> with <code>k = 1/&tau;</code> and sinusoidal excitation J (book Eqs. 10.4&ndash;10.11). The script integrates this numerically, waits until the start-up transient has died, then fits the steady response. It recovers the book's <code>tan &theta; = &omega;&tau; = 2&pi;&nu;&tau;</code> and, as the amplitude factor in Eq. 10.11 implies, a modulation depth of <code>1/&radic;(1 + &omega;&sup2;&tau;&sup2;) = cos &theta;</code>.</p>
<table class="cat"><tr><th>frequency</th><th>lifetime</th><th>phase lag</th></tr>
<tr><td>2 MHz</td><td>10 ns</td><td>7.16 degrees</td></tr>
<tr><td>20 MHz</td><td>10 ns</td><td>51.5 degrees</td></tr>
<tr><td>2 MHz</td><td>0.1 ns</td><td>0.072 degrees</td></tr>
<tr><td>20 MHz</td><td>0.1 ns</td><td>0.72 degrees</td></tr></table>
<p class="result">Control: the inverted relation tan &theta; = 1/(&omega;&tau;) is rejected by the same simulation. The table also shows that the book's range (2 to 20 MHz for 1e-8 to 1e-10 s) leaves angles below one degree at the short end; whether a detector can resolve them is not checked here.</p></div>
<div class="pt"><p>A emissão obedece a <code>dI/dt = &minus;kI + k J(t)</code>, com <code>k = 1/&tau;</code> e excitação senoidal. O script integra numericamente, espera o transiente inicial morrer e ajusta a resposta estacionária. Recupera <code>tan &theta; = &omega;&tau; = 2&pi;&nu;&tau;</code> do livro e uma profundidade de modulação <code>cos &theta;</code>. Fases: 7.16 graus (2 MHz, 10 ns), 51.5 graus (20 MHz, 10 ns), 0.072 graus (2 MHz, 0.1 ns) e 0.72 graus (20 MHz, 0.1 ns).</p>
<p class="result">Controle: a relação invertida tan &theta; = 1/(&omega;&tau;) é rejeitada pela mesma simulação. No extremo curto da faixa do livro os ângulos ficam abaixo de um grau; se um detector os resolve não é verificado aqui.</p></div></div>

<div class="deriv"><h3><span class="en">3.3 Distance as delay</span><span class="pt">3.3 Distância como atraso</span></h3>
<div class="en"><p>The Kerr-cell scheme (book p.306) and the Porter&ndash;Topp monitor (p.319) turn distance into time with <code>t = d/c</code>. Light covers 29.98 cm in 1 ns. In the Porter&ndash;Topp arrangement the beam goes to a mirror and back, so moving the mirror 15 cm farther adds a round-trip delay of 1.00 ns, not 0.50 ns.</p>
<p class="result">Control: forgetting the round trip gives 0.50 ns and is rejected.</p></div>
<div class="pt"><p>O esquema com células de Kerr (livro p.306) e o monitor de Porter&ndash;Topp (p.319) convertem distância em tempo com <code>t = d/c</code>. A luz percorre 29.98 cm em 1 ns. No arranjo de Porter&ndash;Topp o feixe vai ao espelho e volta; afastar o espelho 15 cm acrescenta 1.00 ns de atraso de ida e volta, não 0.50 ns.</p></div></div>

<div class="deriv"><h3><span class="en">3.4 Why the photon-counting rate must stay low</span><span class="pt">3.4 Por que a taxa de contagem de fótons deve ficar baixa</span></h3>
<div class="en"><p>The book says only that the count rate should not be too high (p.308). Here is the reason, our derivation. The converter records only the <em>first</em> photon after each flash. If the chance of detecting any photon on a flash is p, early photons crowd out later ones, and the recorded histogram is <code>h(t) = f(t)&middot;exp(&minus;p&middot;F(t))</code>, where f is the true decay and F its cumulative. At early times the log-slope is <code>&minus;(1+p)/&tau;</code>, so the lifetime reads short by the factor <code>1/(1+p)</code>.</p>
<p class="result">At p = 0.01 the lifetime reads 1.0 % short; at p = 0.05, 4.8 % short; at p = 0.5, a third short. Control: the claim of no distortion at p = 0.5 is rejected.</p></div>
<div class="pt"><p>O livro diz apenas que a taxa de contagem não deve ser alta (p.308). Eis o motivo, derivação nossa. O conversor registra apenas o <em>primeiro</em> fóton após cada flash. Se a chance de detectar algum fóton num flash é p, os fótons iniciais ocupam o lugar dos tardios e o histograma é <code>h(t) = f(t) exp(&minus;p F(t))</code>. No começo a inclinação logarítmica é <code>&minus;(1+p)/&tau;</code>: o tempo de vida sai curto por <code>1/(1+p)</code>.</p>
<p class="result">Com p = 0.01 sai 1.0 % curto; com p = 0.05, 4.8 % curto; com p = 0.5, um terço curto. Controle: a afirmação de nenhuma distorção em p = 0.5 é rejeitada.</p></div></div>

<div class="deriv"><h3><span class="en">3.5 From yield and lifetime to rate constants</span><span class="pt">3.5 De rendimento e tempo de vida a constantes de velocidade</span></h3>
<div class="en"><p>Book Eqs. 10.2 and 10.3: <code>k<sub>f</sub> = &phi;<sub>f</sub>/&tau;</code> and <code>1/&tau; = k<sub>f</sub> + &Sigma;k<sub>i</sub></code>. Hypothetical numbers: &phi; = 0.30 and &tau; = 5 ns give <code>k<sub>f</sub> = 6.0e7 /s</code>, the sum of the other rate constants 1.4e8 /s, and a radiative lifetime 1/k<sub>f</sub> = 16.7 ns, with &phi; = &tau;/&tau;<sub>rad</sub>.</p>
<p class="result">Control: a measured lifetime longer than the radiative lifetime would give &phi; &gt; 1 and is rejected.</p></div>
<div class="pt"><p>Eqs. 10.2 e 10.3 do livro: <code>k<sub>f</sub> = &phi;<sub>f</sub>/&tau;</code> e <code>1/&tau; = k<sub>f</sub> + &Sigma;k<sub>i</sub></code>. Números hipotéticos: &phi; = 0.30 e &tau; = 5 ns dão <code>k<sub>f</sub> = 6.0e7 /s</code>, soma das demais constantes 1.4e8 /s e tempo de vida radiativo 16.7 ns.</p></div></div>

<div class="deriv"><h3><span class="en">3.6 A spectrum per wavelength is not a spectrum per wavenumber</span><span class="pt">3.6 Um espectro por comprimento de onda não é um espectro por número de onda</span></h3>
<div class="en"><p>The book states emission spectra in relative quanta per unit wavenumber interval (p.302&ndash;303). Converting from per-nanometre data needs the Jacobian <code>n(&nu;) = n(&lambda;)&middot;&lambda;&sup2;/10<sup>7</sup></code> (&lambda; in nm, &nu; in cm<sup>-1</sup>). Counts are conserved, the shape is not: a Gaussian band centred at 450 nm per nanometre peaks at a wavelength +1.8 nm longer when plotted per wavenumber.</p>
<p class="result">Control: integrating the per-nm spectrum over wavenumber without the Jacobian gives a different area and is rejected. Quantum-yield ratios compare areas, so both spectra must be in the same variable.</p></div>
<div class="pt"><p>O livro expressa espectros de emissão em quanta relativos por intervalo de número de onda (p.302&ndash;303). Converter de dados por nanômetro exige o jacobiano <code>n(&nu;) = n(&lambda;) &lambda;&sup2;/10<sup>7</sup></code>. As contagens se conservam, a forma não: uma banda gaussiana centrada em 450 nm por nanômetro tem pico +1.8 nm mais longo quando traçada por número de onda.</p></div></div>
""",
    calc=dict(
        head=dict(en="Try it: phase lag and modulation for a lifetime", pt="Experimente: defasagem e modulação para um tempo de vida"),
        html="""<div class="calc"><label>modulation &nu; (MHz)<input id="c_nu" type="number" value="20" step="1"></label>
<label>lifetime &tau; (ns)<input id="c_tau" type="number" value="10" step="0.1"></label>
<div class="out" id="c_out"></div></div>""",
        js="""
(function(){
 function run(){
  var nu=parseFloat(document.getElementById('c_nu').value)*1e6,tau=parseFloat(document.getElementById('c_tau').value)*1e-9;
  var out=document.getElementById('c_out');
  if(!(nu>0&&tau>0)){out.textContent='-';return;}
  var wt=2*Math.PI*nu*tau,th=Math.atan(wt)*180/Math.PI;
  out.innerHTML='&omega;&tau; = '+wt.toPrecision(4)+' &middot; phase lag = '+th.toPrecision(4)+' degrees &middot; modulation depth = '+(1/Math.sqrt(1+wt*wt)).toFixed(5);
 }
 ['c_nu','c_tau'].forEach(function(i){document.getElementById(i).addEventListener('input',run);});run();
})();"""),
    quiz=dict(
        q=dict(en="A single-photon-counting run gives a lifetime about 5 % shorter than a phase-fluorimeter value for the same dye. Your detector registers a photon on roughly one flash in twenty. What do you check first?",
               pt="Uma corrida de contagem de fóton único dá um tempo de vida cerca de 5 % menor que o valor do fluorímetro de fase para o mesmo corante. Seu detector registra um fóton em cerca de um flash a cada vinte. O que você verifica primeiro?"),
        opts=[dict(en="Recalibrate the detector's wavelength response", pt="Recalibrar a resposta espectral do detector"),
              dict(en="Lower the count rate so that photons are detected on far fewer flashes", pt="Reduzir a taxa de contagem para que fótons sejam detectados em bem menos flashes"),
              dict(en="Add a quantum counter in front of the detector", pt="Pôr um contador quântico na frente do detector"),
              dict(en="Slow down the rotating sector", pt="Diminuir a velocidade do setor rotativo")],
        correct=1,
        ok=dict(en="Correct. One flash in twenty is p = 0.05, and the first-photon bias gives a lifetime short by 1/(1+p), about 4.8 %. The other fixes address wavelength response or phosphorescence, not this.",
                pt="Correto. Um flash em vinte é p = 0.05, e o viés do primeiro fóton encurta o tempo de vida por 1/(1+p), cerca de 4.8 %. As demais correções tratam de resposta espectral ou fosforescência, não disto."),
        no=dict(en="Not the first suspect. A response correction changes spectra, not decay times, and a rotating sector is for phosphorescence. One detected photon per twenty flashes is p = 0.05, and the first-photon bias alone shortens the lifetime by about 4.8 %.",
                pt="Não é o primeiro suspeito. Correção de resposta muda espectros, não tempos de decaimento, e o setor rotativo é para fosforescência. Um fóton por vinte flashes é p = 0.05, e o viés do primeiro fóton sozinho encurta o tempo de vida cerca de 4.8 %.")),
    notdo=dict(en="""<p>This room does not teach instrument operation and recommends no instrument. Every <em>book</em> statement is cited by page, from page scans of one textbook. Every <em>number in the derivations</em> comes from the verify script. Four things are open:</p>
<p><strong>The reference yield.</strong> The book names quinine sulphate in 0.1 N H<sub>2</sub>SO<sub>4</sub> and anthracene in benzene as common standards (p.303). The pages read do not state a yield for either, so none is used; the 0.50 in the example is hypothetical.</p>
<p><strong>Corrections left out.</strong> Eq. 10.1 as used here ignores the refractive-index factor between solvents and any re-absorption correction. The book flags re-absorption (p.304).</p>
<p><strong>Detectability.</strong> Section 3.2 shows the phase angles the book's frequency range implies, not whether a given detector can resolve 0.72 degrees.</p>
<p><strong>Portuguese.</strong> The Portuguese text was drafted by Claude and has not been reviewed by a native speaker.</p>""",
               pt="""<p>Esta sala não ensina a operar instrumentos nem recomenda nenhum. Cada afirmação do <em>livro</em> é citada por página, de imagens de um único livro-texto; cada <em>número das derivações</em> vem do script de verificação. Quatro pontos em aberto: o rendimento da referência (as páginas lidas não dão valor para o sulfato de quinina nem para o antraceno, então o 0.50 do exemplo é hipotético); correções omitidas (fator de índice de refração e reabsorção); detectabilidade (a seção 3.2 mostra os ângulos de fase, não se um detector os resolve); e o português, redigido por Claude e sem revisão de falante nativo.</p>"""),
    verify="photochem-spectrometer-verify.py",
    pages="book pp.302-311",
)
