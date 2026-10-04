# -*- coding: utf-8 -*-
"""Room 4: flash photolysis (and the sector method). Numbers are produced by book7/photochem-flash-photolysis-verify.py."""
ROOM = dict(
    slug="flash-photolysis", num=4,
    title=dict(en="Flash photolysis", pt="Fotólise por pulso (flash)"),
    tagline=dict(en="Catching what lives for microseconds", pt="Capturando o que vive por microssegundos"),
    sub=dict(
        en="Some of the most important species in a photochemical reaction exist for far too short a time to see in steady light. Flash photolysis makes a lot of them at once and watches them go.",
        pt="Algumas das espécies mais importantes de uma reação fotoquímica existem por tempo curto demais para serem vistas sob luz contínua. A fotólise por pulso produz muitas de uma vez e observa o seu desaparecimento."),
    concept=dict(
        A2="Some molecules live for a very short time after light hits a sample. They disappear before you can see them. In flash photolysis, we use one very strong flash of light. It makes many of these short-lived molecules at the same moment. Then a second, weaker light looks at them. We watch how fast they disappear. This tells us how fast they react.",
        B1="In steady light, short-lived intermediates never build up enough to detect. Flash photolysis fixes this: a very intense flash creates a large amount of the intermediate at once, and a weaker monitoring light measures its absorption afterwards. If the monitoring flash is fired after different delays, you get a spectrum at each delay. If a continuous monitoring beam is set at the intermediate's absorption maximum, an oscilloscope shows the decay directly.",
        B2="The stationary concentration of a reactive intermediate in steady illumination is far too small for ordinary spectroscopy. Flash photolysis is a relaxation method: an intense flash, delivering 20 to 2000 J in 1 to 100 microseconds from a discharged capacitor bank, produces a large transient concentration, and the system is then followed either by flash spectroscopy (a second flash at a preset delay, recorded on a spectrograph) or by flash kinetic spectrophotometry (a continuous beam at the transient's absorption maximum, displayed on an oscilloscope). The flash must be short compared with the lifetime to be measured.",
        C1="Flash photolysis converts a stationary-state problem into a relaxation problem: a photolysis flash lifts a macroscopic fraction of the sample into transients whose absorption can be recorded as a time-resolved spectrum (probe flash with variable delay) and then as a kinetic trace at the spectral maximum. Detectability follows from the Beer-Lambert law applied to the quanta delivered, and time resolution is bounded below by the width of the photolysis pulse, which is why Q-switched and mode-locked lasers extend the method from microseconds to nanoseconds and picoseconds. Where a transient can only be generated continuously, the rotating-sector method recovers its lifetime from the dependence of the reaction rate on chopping frequency, but only when termination is second order."),
    glossary=[
        ("transient species", "espécie transiente"), ("flash photolysis", "fotólise por pulso (flash)"), ("delay time", "tempo de atraso"),
        ("extinction coefficient", "coeficiente de extinção"), ("triplet state", "estado tripleto"), ("scavenger", "sequestrador (scavenger)"),
        ("free radical", "radical livre"), ("sector wheel", "disco setorado"), ("stationary state", "estado estacionário"),
        ("detection limit", "limite de detecção"), ("flash lamp", "lâmpada de flash"), ("spectrograph", "espectrógrafo"),
        ("oscilloscope", "osciloscópio")],
    chooser_head=dict(en="2 · Which method for which transient", pt="2 · Qual método para qual transiente"),
    chooser_pill=dict(en="use-it-when", pt="quando usar"),
    chooser=[
        dict(name="Scavengers", ans=dict(en="Is a given radical or species being formed at all?", pt="Um dado radical ou espécie está mesmo se formando?"),
             use=dict(en="Indirect evidence is enough. Iodine traps alkyl radicals, azide ion and N2O trap singlet oxygen, p-nitroso-N,N-dimethylaniline traps OH in alkaline water (book p.311).", pt="Evidência indireta basta. O iodo captura radicais alquila, o íon azida e o N2O capturam oxigênio singlete, a p-nitroso-N,N-dimetilanilina captura OH em água alcalina (livro p.311)."),
             no=dict(en="It does not give a decay rate; the scavenger changes the chemistry.", pt="Não dá taxa de decaimento; o sequestrador altera a química.")),
        dict(name="Sector (chopper) method", ans=dict(en="The lifetime of a radical in a steady-state, chain-type reaction.", pt="O tempo de vida de um radical numa reação estacionária de tipo cadeia."),
             use=dict(en="The reaction rate depends on the square root of the light intensity (book p.314).", pt="A velocidade da reação depende da raiz quadrada da intensidade da luz (livro p.314)."),
             no=dict(en="Only works with second-order termination, and the lifetime is not simply read at the inflection (derived below).", pt="Só funciona com terminação de segunda ordem, e o tempo de vida não se lê simplesmente na inflexão (derivado abaixo).")),
        dict(name="Flash spectroscopy", ans=dict(en="What does the transient look like? A spectrum at each delay time.", pt="Como é o transiente? Um espectro para cada tempo de atraso."),
             use=dict(en="You do not yet know where the transient absorbs. A probe flash goes at right angles to the photolysis flash, delayed by a preset time, into a spectrograph (book p.314).", pt="Você ainda não sabe onde o transiente absorve. Um flash de prova vai em ângulo reto com o flash de fotólise, atrasado por um tempo predefinido, até um espectrógrafo (livro p.314)."),
             no=dict(en="One delay per shot: a decay curve needs many shots.", pt="Um atraso por disparo: uma curva de decaimento exige muitos disparos.")),
        dict(name="Flash kinetic spectrophotometry", ans=dict(en="How fast does it decay at its absorption maximum?", pt="Com que rapidez decai no seu máximo de absorção?"),
             use=dict(en="You already know the wavelength; a continuous beam and an oscilloscope give the whole decay in one shot (book p.314-315).", pt="Você já conhece o comprimento de onda; um feixe contínuo e um osciloscópio dão todo o decaimento num disparo (livro p.314-315)."),
             no=dict(en="It tells you nothing about where else the transient absorbs.", pt="Nada diz sobre onde mais o transiente absorve.")),
        dict(name="Flash lamp (1 to 100 microseconds)", ans=dict(en="20 to 2000 J discharged from capacitors charged to 0.5 to 20 kV.", pt="20 a 2000 J descarregados de capacitores carregados de 0,5 a 20 kV."),
             use=dict(en="Lifetimes of tens of microseconds and longer (derived below).", pt="Tempos de vida de dezenas de microssegundos ou mais (derivado abaixo)."),
             no=dict(en="Shorter lifetimes are hidden under the flash.", pt="Tempos de vida mais curtos ficam escondidos sob o flash.")),
        dict(name="Q-switched laser flash", ans=dict(en="Nanosecond photolysis, with a pulse that can be delayed by distance (Porter and Topp, book p.319).", pt="Fotólise de nanossegundos, com pulso que pode ser atrasado por distância (Porter e Topp, livro p.319)."),
             use=dict(en="Transients of a few nanoseconds (book p.317).", pt="Transientes de poucos nanossegundos (livro p.317)."),
             no=dict(en="The laser line is one colour, so the photolyte must absorb there (or you double it first).", pt="A linha do laser é de uma só cor; o fotólito precisa absorver ali (ou você dobra a frequência antes).")),
    ],
    derive_head=dict(en="3 · Derived and checked", pt="3 · Derivado e verificado"),
    derive_pill=dict(en="our arithmetic and simulations", pt="nossa aritmética e simulações"),
    derive_html="""
<div class="deriv"><h3><span class="en">3.1 The book's detectability example, rechecked</span><span class="pt">3.1 O exemplo de detectabilidade do livro, reconferido</span></h3>
<div class="en"><p>Book pp.315&ndash;316 argue that a 100 J flash at a colour temperature of 6000 K puts 12 % of its energy in a 100 nm band centred on 400 nm, that this makes about 2.5e19 quanta, that 20 mL of solution then holds 2.1e-3 mol/L of intermediate, and that a transient with &epsilon; = 7e4 L/(mol cm) in a 20 cm cell is just detectable at 3 % change in transmitted light, at about 1e-8 mol/L. Rechecked with exact constants:</p>
<table class="cat"><tr><th>quantity</th><th>book</th><th>recomputed</th></tr>
<tr><td>energy share, 350&ndash;450 nm at 6000 K</td><td>12 %</td><td>12.2 %</td></tr>
<tr><td>quanta from 100 J</td><td>2.5e19</td><td>2.42e19 (the book's figure is +3.5 % high)</td></tr>
<tr><td>concentration in 20 mL</td><td>2.1e-3 mol/L</td><td>2.0e-3 mol/L</td></tr>
<tr><td>detection limit</td><td>about 1e-8 mol/L</td><td>9.4e-9 mol/L</td></tr></table>
<p class="result">The detection limit leaves a headroom of 2.2e5 against the book's 2.1e-3 (2.1e5 against the exact 2.0e-3), about five orders of magnitude. Turned round: the overall efficiency from lamp quanta to detected intermediate could fall as low as 4.5e-6 before the triplet slipped under the limit. The book's small rounding does not change the argument. Control: at 5000 K the in-band share would be only 7.7 %, and the book's 12 % is rejected there.</p></div>
<div class="pt"><p>O livro (pp.315&ndash;316) argumenta que um flash de 100 J a 6000 K põe 12 % da energia numa faixa de 100 nm centrada em 400 nm, o que dá cerca de 2.5e19 quanta, 2.1e-3 mol/L de intermediário em 20 mL, e que um transiente com &epsilon; = 7e4 numa cubeta de 20 cm é detectável com 3 % de variação, em torno de 1e-8 mol/L. Reconferido com constantes exatas: 12.2 %, 2.42e19 quanta (o valor do livro é +3.5 % alto), 2.0e-3 mol/L e 9.4e-9 mol/L.</p>
<p class="result">A folga é de 2.2e5, cerca de cinco ordens de grandeza; a eficiência global poderia cair até 4.5e-6 antes de o tripleto ficar abaixo do limite. O pequeno arredondamento do livro não altera o argumento. Controle: a 5000 K a fração na faixa seria só 7.7 %.</p></div></div>

<div class="deriv"><h3><span class="en">3.2 Flash length against lifetime: an apparent inversion on p.315</span><span class="pt">3.2 Duração do flash contra tempo de vida: uma aparente inversão na p.315</span></h3>
<div class="en"><p>Page 315 prints that the duration of the photolysing flash sets the <em>upper</em> limit to the lifetime of transients that can be detected, and then says the lamp sets a limit of 1 to 10 &micro;s. Our simulation says the opposite direction. Model the lamp as a box of width w that makes the transient at a constant rate while it burns, with the transient decaying with lifetime &tau;. The peak, as a fraction of what an instantaneous flash would give, is <code>(&tau;/w)(1 &minus; e<sup>&minus;w/&tau;</sup>)</code>.</p>
<table class="cat"><tr><th>flash width</th><th>lifetime</th><th>peak seen</th></tr>
<tr><td>10 &micro;s</td><td>1 &micro;s</td><td>0.100</td></tr>
<tr><td>10 &micro;s</td><td>2 &micro;s</td><td>0.199</td></tr>
<tr><td>10 &micro;s</td><td>10 &micro;s</td><td>0.632</td></tr>
<tr><td>10 &micro;s</td><td>100 &micro;s</td><td>0.952</td></tr>
<tr><td>100 &micro;s</td><td>1 &micro;s</td><td>0.010</td></tr></table>
<p class="result">It is the <em>short</em> lifetimes that a long flash loses, so the flash width sets a <em>lower</em> limit on what can be resolved. A 100 &micro;s transient is seen at 95 % with a 10 &micro;s flash, which is not what an upper limit would allow. What sets the <em>longest</em> measurable lifetime is not in the book and is not claimed here. The sentence is read from the page scan; this section stands as a statement about the physics whether or not the scan misleads. Control: the printed reading is rejected by the numbers above.</p></div>
<div class="pt"><p>A p.315 imprime que a duração do flash de fotólise fixa o limite <em>superior</em> do tempo de vida detectável, e depois diz que a lâmpada fixa um limite de 1 a 10 &micro;s. Nossa simulação aponta o sentido contrário. Modelando a lâmpada como uma caixa de largura w que produz o transiente a taxa constante, o pico, como fração do que um flash instantâneo daria, é <code>(&tau;/w)(1 &minus; e<sup>&minus;w/&tau;</sup>)</code>: com w = 10 &micro;s, 0.100 para 1 &micro;s, 0.199 para 2 &micro;s, 0.632 para 10 &micro;s e 0.952 para 100 &micro;s; com w = 100 &micro;s e 1 &micro;s, 0.010.</p>
<p class="result">São os tempos de vida <em>curtos</em> que um flash longo perde: a largura do flash fixa um limite <em>inferior</em> do que se resolve. O que limita o tempo de vida <em>mais longo</em> não está no livro e não é afirmado aqui. A frase foi lida da imagem da página.</p></div></div>

<div class="deriv"><h3><span class="en">3.3 The capacitor bank</span><span class="pt">3.3 O banco de capacitores</span></h3>
<div class="en"><p>The stored energy is <code>E = &frac12;CV&sup2;</code>. Fig. 10.10B shows 5 &micro;F at 20 kV, which stores 1000 J, inside the book's 20 to 2000 J. The low end, 20 J at 0.5 kV, needs 160 &micro;F.</p>
<p class="result">Control: read the 20 kV as 20 V and the same capacitor stores about a millijoule, which is rejected.</p></div>
<div class="pt"><p>A energia armazenada é <code>E = &frac12;CV&sup2;</code>. A Fig. 10.10B mostra 5 &micro;F a 20 kV, que armazenam 1000 J, dentro dos 20 a 2000 J do livro. O extremo baixo, 20 J a 0,5 kV, exige 160 &micro;F.</p></div></div>

<div class="deriv"><h3><span class="en">3.4 The sector method, and where 1/&radic;2 comes from</span><span class="pt">3.4 O método do setor e de onde vem 1/&radic;2</span></h3>
<div class="en"><p>The book (p.314) says that with equal light and dark periods the radical concentration at high sector speed is 1/&radic;2 of its continuous-light value, and that the change from the slow- to the fast-speed limit gives the radical's lifetime. Model (ours): <code>d[X]/dt = I<sub>a</sub>(t) &minus; k[X]&sup2;</code>, light on for half of each period. At high speed the radical sees half the intensity, so [X] falls to <code>&radic;(I<sub>a</sub>/2k)</code> and the relative rate is 0.7071. At low speed the radicals are built in the light and die in the dark.</p>
<p>The simulation gives 0.7071 at high speed and, at low speed, 0.533 at 200 radical lifetimes and 0.506 at 2000: it approaches 1/2 from above, and only slowly, because second-order decay in the dark is hyperbolic. The half-way point between the limits falls at a light period of 16.1 radical lifetimes (lifetime taken as 1/(2k[X]<sub>ss</sub>)). Growth from zero under light follows a tanh: 90 % of steady state after 2.9 lifetimes, 99 % after 5.3.</p>
<p class="result">So the book's picture is right in outline, and the inflection sits several times beyond the time to reach steady state. Reading a lifetime from it needs a model fit, not a ruler. Control: with first-order termination the fast and slow limits are both 0.5, there is no 1/&radic;2 step, and the method gives no lifetime.</p></div>
<div class="pt"><p>O livro (p.314) diz que, com períodos iguais de luz e escuro, a concentração de radicais em alta velocidade é 1/&radic;2 do valor sob luz contínua, e que a transição entre os limites lento e rápido dá o tempo de vida do radical. Modelo (nosso): <code>d[X]/dt = I<sub>a</sub>(t) &minus; k[X]&sup2;</code>. A simulação dá 0.7071 em alta velocidade e, em baixa, 0.533 a 200 tempos de vida e 0.506 a 2000: aproxima-se de 1/2 por cima, devagar, porque o decaimento de segunda ordem no escuro é hiperbólico. O ponto médio cai a um período de luz de 16.1 tempos de vida; o crescimento a partir de zero segue uma tanh: 90 % do estado estacionário após 2.9 tempos de vida, 99 % após 5.3.</p>
<p class="result">O quadro do livro está certo em linhas gerais, mas ler o tempo de vida na inflexão exige ajuste de modelo. Controle: com terminação de primeira ordem, os dois limites são 0.5 e o método não dá tempo de vida.</p></div></div>
""",
    calc=dict(
        head=dict(en="Try it: can the transient be seen?", pt="Experimente: dá para ver o transiente?"),
        html="""<div class="calc"><label>flash energy (J)<input id="c_E" type="number" value="100" step="10"></label>
<label>share in band<input id="c_f" type="number" value="0.12" step="0.01"></label>
<label>&lambda; (nm)<input id="c_nm" type="number" value="400" step="10"></label>
<label>volume (mL)<input id="c_V" type="number" value="20" step="1"></label>
<label>&epsilon; (L/(mol cm))<input id="c_e" type="text" value="7e4"></label>
<label>cell length (cm)<input id="c_l" type="number" value="20" step="1"></label>
<label>detectable change (%)<input id="c_d" type="number" value="3" step="0.5"></label>
<div class="out" id="c_out"></div></div>""",
        js="""
(function(){
 var h=6.62607015e-34,c=299792458,NA=6.02214076e23;
 function g(i){return parseFloat(document.getElementById(i).value);}
 function run(){
  var E=g('c_E'),f=g('c_f'),nm=g('c_nm'),V=g('c_V')/1000,e=g('c_e'),l=g('c_l'),d=g('c_d');
  var out=document.getElementById('c_out');
  if(!(E>0&&f>0&&nm>0&&V>0&&e>0&&l>0&&d>0&&d<100)){out.textContent='-';return;}
  var q=E*f/(h*c/(nm*1e-9)),C=q/NA/V,lim=Math.log10(100/(100-d))/(e*l);
  out.innerHTML='quanta = '+q.toExponential(2)+' &middot; max concentration = '+C.toExponential(1)+' mol/L &middot; detection limit = '+lim.toExponential(1)+' mol/L &middot; headroom = '+(C/lim).toExponential(1)+' &middot; '+(C>lim?'above the limit':'BELOW the limit');
 }
 ['c_E','c_f','c_nm','c_V','c_e','c_l','c_d'].forEach(function(i){document.getElementById(i).addEventListener('input',run);});run();
})();"""),
    quiz=dict(
        q=dict(en="A transient lives about 2 microseconds. You can use a flash lamp with a 10 microsecond flash, or a Q-switched laser with a nanosecond pulse. Which do you choose, and why?",
               pt="Um transiente vive cerca de 2 microssegundos. Você pode usar uma lâmpada de flash de 10 microssegundos ou um laser com chave Q de nanossegundos. Qual escolhe, e por quê?"),
        opts=[dict(en="The laser: the lamp's flash is longer than the lifetime", pt="O laser: o flash da lâmpada é mais longo que o tempo de vida"),
              dict(en="The lamp: longer flashes resolve longer lifetimes better", pt="A lâmpada: flashes mais longos resolvem melhor tempos de vida mais longos"),
              dict(en="Either; the lifetime does not depend on the flash", pt="Qualquer um; o tempo de vida não depende do flash"),
              dict(en="Neither; use scavengers only", pt="Nenhum; use apenas sequestradores")],
        correct=0,
        ok=dict(en="Correct. By our model, with a 10 microsecond flash a 2 microsecond transient reaches only about 0.199 of its instantaneous-flash peak, and what you see is largely the lamp's own shape. A nanosecond pulse is short against 2 microseconds.",
                pt="Correto. Pelo nosso modelo, com um flash de 10 microssegundos um transiente de 2 microssegundos atinge só cerca de 0.199 do pico de um flash instantâneo, e o que se vê é em boa parte a forma da própria lâmpada. Um pulso de nanossegundos é curto frente a 2 microssegundos."),
        no=dict(en="No. The flash width limits how short a lifetime can be resolved, not how long. With a 10 microsecond flash a 2 microsecond transient reaches only about 0.199 of its peak. Scavengers give indirect evidence but no decay rate.",
                pt="Não. A largura do flash limita quão curto um tempo de vida pode ser resolvido, não quão longo. Com flash de 10 microssegundos um transiente de 2 microssegundos atinge só cerca de 0.199 do pico. Sequestradores dão evidência indireta, mas não taxa de decaimento.")),
    notdo=dict(en="""<p>This room does not teach a laboratory procedure and recommends no instrument. Every <em>book</em> statement is cited by page, read from page scans of one textbook; every <em>number in the derivations</em> comes from the verify script. Five things are open:</p>
<p><strong>The detectability argument</strong> takes the book's premises: 100 J of lamp output as a 6000 K blackbody, fully absorbed in 20 mL. It does not model electrical-to-light efficiency, the intermediate's yield or the sample's own absorption.</p>
<p><strong>The p.315 sentence.</strong> We read it as an inversion and show a model that says otherwise. If the scan misleads the sentence, the model still stands as physics. What limits the longest measurable lifetime is not covered.</p>
<p><strong>Figure values.</strong> The 5 &micro;F and 20 kV in Fig. 10.10B are read from the page scan.</p>
<p><strong>The sector model</strong> uses equal light and dark periods and one termination order at a time; the book's general ratio is not explored.</p>
<p><strong>Portuguese.</strong> The Portuguese text was drafted by Claude and has not been reviewed by a native speaker.</p>""",
               pt="""<p>Esta sala não ensina procedimento de laboratório e não recomenda instrumento. Cada afirmação do <em>livro</em> é citada por página, de imagens de um único livro-texto; cada <em>número das derivações</em> vem do script. Cinco pontos em aberto: o argumento de detectabilidade adota as premissas do livro; a frase da p.315, que lemos como inversão, com um modelo que diz o contrário (o que limita o tempo de vida mais longo não é coberto); os valores da Fig. 10.10B, lidos da imagem; o modelo do setor, com períodos iguais; e o português, redigido por Claude, sem revisão de falante nativo.</p>"""),
    verify="photochem-flash-photolysis-verify.py",
    pages="book pp.311-317",
)
