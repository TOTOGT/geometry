# -*- coding: utf-8 -*-
"""Room 3: the laser. Numbers are produced by book7/photochem-laser-verify.py."""
ROOM = dict(
    slug="laser", num=3,
    title=dict(en="The laser", pt="O laser"),
    tagline=dict(en="Light that starts together", pt="Luz que começa junta"),
    sub=dict(
        en="A laser is a light source with one colour, one direction and a pulse as short as you can build. This room covers why inversion needs three or four levels, how a giant pulse is made, and what a laser can do that a flash lamp cannot.",
        pt="O laser é uma fonte de luz com uma só cor, uma só direção e um pulso tão curto quanto se consiga construir. Esta sala cobre por que a inversão exige três ou quatro níveis, como se faz um pulso gigante e o que um laser faz que uma lâmpada de flash não faz."),
    concept=dict(
        A2="A laser makes light in a special way. The light has one colour. It goes in one direction. All the light waves move together. To make a laser, you must put more molecules in the high-energy state than in the low-energy state. This is called population inversion. A system with only two energy levels can never do this. So lasers use three or four levels. Some lasers give a very short, very strong flash of light.",
        B1="In a laser, light stimulates molecules in an excited state to give out more light of exactly the same colour and phase. This only works if more molecules are in the upper state than in the lower one, which is called population inversion. With only two levels you can never get more than half the molecules into the upper state, so real lasers use three or four levels. A cavity with two mirrors makes the light pass through the material many times. A switch inside the cavity can hold the light back and then release it as one giant, very short pulse.",
        B2="Laser action needs population inversion between the emitting levels, which a two-level system cannot reach because at best half the molecules can be promoted. A three-level scheme such as ruby (Cr(III) in Al2O3) pumps the ground state to a short-lived upper level that relaxes quickly to a long-lived metastable level, which then lases back to the ground state. A four-level scheme lases into a level above the ground state and needs much less pump power. Q-switching blocks the cavity while the metastable level fills far beyond threshold, then opens it to release a nanosecond giant pulse; frequency doubling in a crystal such as KDP moves the ruby line from 694 to 347 nm for photochemistry.",
        C1="Inversion between a lasing pair requires a pumping scheme in which the lower laser level is depleted faster than the upper one is fed: two levels cannot do it, three levels need more than half the ground-state population promoted, and four levels, where the lower laser level lies above the ground state and empties quickly, lower the threshold to the thermal population of that level. An optical cavity supplies the feedback; Q-switching holds the cavity loss high while the inversion builds, then drops it to extract the stored energy as a nanosecond giant pulse, and mode-locking compresses the output into picosecond pulses of very high peak power. Harmonic generation in crystals such as KDP brings the fundamental into the ultraviolet, and tunable dye lasers or narrow-line sources permit state-selective, even isotope-selective, photochemistry that a broadband flash lamp cannot."),
    glossary=[
        ("laser", "laser"), ("population inversion", "inversão de população"), ("stimulated emission", "emissão estimulada"),
        ("pump", "bombeamento"), ("metastable state", "estado metaestável"), ("Q-switch", "chave Q (Q-switch)"),
        ("optical cavity", "cavidade óptica"), ("frequency doubling", "dobramento de frequência"), ("mode-locking", "travamento de modos"),
        ("coherent light", "luz coerente"), ("threshold", "limiar"), ("peak power", "potência de pico")],
    chooser_head=dict(en="2 · Which laser behaviour for which job", pt="2 · Qual comportamento de laser para qual tarefa"),
    chooser_pill=dict(en="use-it-when", pt="quando usar"),
    chooser=[
        dict(name="Continuous laser (He-Ne type)", ans=dict(en="A steady, narrow beam.", pt="Um feixe estável e estreito."),
             use=dict(en="Continuous pumping and a continuous output are what the job needs (book p.318).", pt="O trabalho precisa de bombeamento e saída contínuos (livro p.318)."),
             no=dict(en="It does not give the short, intense pulse of a Q-switched system.", pt="Não dá o pulso curto e intenso de um sistema com chave Q.")),
        dict(name="Q-switched pulsed laser", ans=dict(en="A giant nanosecond pulse of several joules.", pt="Um pulso gigante de nanossegundos com vários joules."),
             use=dict(en="You need to photolyse faster than a flash lamp allows (book p.317, 319).", pt="Você precisa fotolisar mais rápido do que uma lâmpada de flash permite (livro p.317, 319)."),
             no=dict(en="Ruby emits at 694 nm; for ultraviolet photochemistry you add frequency doubling.", pt="O rubi emite a 694 nm; para fotoquímica no ultravioleta você acrescenta dobramento de frequência.")),
        dict(name="Frequency doubling (KDP)", ans=dict(en="Half the wavelength: 694 to 347 nm. The book gives about 20 % efficiency.", pt="Metade do comprimento de onda: 694 para 347 nm. O livro dá cerca de 20 % de eficiência."),
             use=dict(en="The photochemistry sits in the ultraviolet and you have a red or near-infrared laser (book p.319).", pt="A fotoquímica está no ultravioleta e você tem um laser vermelho ou infravermelho próximo (livro p.319)."),
             no=dict(en="The book does not say whether 20 % means energy or photons; read as energy it is only 10 % of the photons (derived below).", pt="O livro não diz se 20 % é energia ou fótons; lido como energia, são só 10 % dos fótons (derivado abaixo).")),
        dict(name="Mode-locked laser", ans=dict(en="Picosecond pulses with peak power 1e6 to 1e13 W.", pt="Pulsos de picossegundos com potência de pico de 1e6 a 1e13 W."),
             use=dict(en="Vibrational relaxation and radiationless transitions in the 1e-12 to 1e-14 s region (book p.311, 320).", pt="Relaxação vibracional e transições não radiativas na região de 1e-12 a 1e-14 s (livro p.311, 320)."),
             no=dict(en="Not a general-purpose photolysis source: the pulse is built for time resolution, not for total energy.", pt="Não é fonte de fotólise de uso geral: o pulso é feito para resolução temporal, não para energia total.")),
        dict(name="Tunable dye laser", ans=dict(en="Any colour from about 400 to 700 nm, chosen with a grating and an etalon in the cavity.", pt="Qualquer cor de cerca de 400 a 700 nm, escolhida com grade e etalon dentro da cavidade."),
             use=dict(en="You want to excite one state or one isotopic species (book p.319-321).", pt="Você quer excitar um estado ou uma espécie isotópica (livro p.319-321)."),
             no=dict(en="It does not cover the ultraviolet by itself.", pt="Não cobre o ultravioleta sozinho.")),
        dict(name="Laser or flash lamp?", ans=dict(en="The laser gives one colour that excites defined states; a lamp gives a continuum that can drive several reactions at once.", pt="O laser dá uma cor que excita estados definidos; a lâmpada dá um contínuo que pode acionar várias reações ao mesmo tempo."),
             use=dict(en="Use the laser when you must keep the chemistry simple; use the lamp when you need broad coverage and energy cheaply.", pt="Use o laser quando for preciso manter a química simples; use a lâmpada quando precisar de cobertura ampla e energia a baixo custo."),
             no=dict(en="The book warns that a lamp's continuum can complicate the interpretation (p.319-320).", pt="O livro alerta que o contínuo de uma lâmpada pode complicar a interpretação (p.319-320).")),
    ],
    derive_head=dict(en="3 · Derived and checked", pt="3 · Derivado e verificado"),
    derive_pill=dict(en="our models, not the book's", pt="nossos modelos, não os do livro"),
    derive_html="""
<div class="deriv"><h3><span class="en">3.1 Two levels never invert</span><span class="pt">3.1 Dois níveis nunca invertem</span></h3>
<div class="en"><p>The book says at most 50 % of the molecules can be promoted in a two-level system (p.317). A balance of absorption, stimulated emission and spontaneous decay, <code>W&middot;N<sub>1</sub> &minus; W&middot;(g<sub>1</sub>/g<sub>2</sub>)&middot;N<sub>2</sub> &minus; A&middot;N<sub>2</sub> = 0</code>, shows why: as the pump rate W grows the upper fraction climbs towards <code>g<sub>2</sub>/(g<sub>1</sub>+g<sub>2</sub>)</code>, which is one half for equal degeneracies. The script reaches 0.499975 at the largest pump rate tried and never passes 0.5.</p>
<p class="result">With degeneracies 2 and 3 the upper fraction can pass one half (limit 3/5), but N<sub>2</sub>/g<sub>2</sub> never exceeds N<sub>1</sub>/g<sub>1</sub>, and that is the real condition for inversion. Control: the claim that high pump power inverts two levels is rejected.</p></div>
<div class="pt"><p>O livro diz que no máximo 50 % das moléculas podem ser promovidas num sistema de dois níveis (p.317). O balanço entre absorção, emissão estimulada e decaimento espontâneo mostra por quê: a fração superior tende a <code>g<sub>2</sub>/(g<sub>1</sub>+g<sub>2</sub>)</code>, metade para degenerescências iguais. O script chega a 0.499975 e nunca passa de 0.5.</p>
<p class="result">Com degenerescências 2 e 3 a fração superior pode passar de metade (limite 3/5), mas N<sub>2</sub>/g<sub>2</sub> nunca supera N<sub>1</sub>/g<sub>1</sub>, que é a condição real de inversão.</p></div></div>

<div class="deriv"><h3><span class="en">3.2 Three levels: the pump must beat the metastable decay</span><span class="pt">3.2 Três níveis: o bombeamento precisa vencer o decaimento metaestável</span></h3>
<div class="en"><p>Model (ours): ground level 1, metastable level 2 that decays to 1 at <code>k<sub>21</sub></code>, and a pumped level 3 that falls quickly to level 2. The steady state gives inversion (N<sub>2</sub> &gt; N<sub>1</sub>) when the pump rate per ion exceeds <code>W = k<sub>21</sub>k<sub>32</sub>/(k<sub>32</sub>&minus;k<sub>21</sub>) &asymp; k<sub>21</sub></code>. With the ruby value k<sub>21</sub> = 2e2 /s read from the book's Fig. 10.12 the threshold is 200 /s: one pump quantum per ion every 5 ms, which also means more than half the ions must be lifted.</p>
<p class="result">Control: a threshold ten times larger is rejected by the numerical solution.</p></div>
<div class="pt"><p>Modelo (nosso): nível fundamental 1, nível metaestável 2 que decai a 1 com <code>k<sub>21</sub></code> e um nível bombeado 3 que cai rápido para o 2. O estado estacionário dá inversão quando a taxa de bombeamento por íon passa de <code>W &asymp; k<sub>21</sub></code>. Com k<sub>21</sub> = 2e2 /s da Fig. 10.12 do livro, o limiar é 200 /s: um quantum de bombeamento por íon a cada 5 ms; mais da metade dos íons precisa ser erguida.</p></div></div>

<div class="deriv"><h3><span class="en">3.3 Four levels: the threshold is set by the lower level's thermal population</span><span class="pt">3.3 Quatro níveis: o limiar é fixado pela população térmica do nível inferior</span></h3>
<div class="en"><p>The book says a four-level scheme needs much less pump power (p.318) without a number. In our model the lower laser level empties at <code>k<sub>l</sub></code> and is refilled thermally from the ground state with detailed balance. Inversion needs <code>k<sub>l</sub> &gt; k<sub>u</sub></code> (the lower level must empty faster than the upper one decays, whatever the pump), and the threshold falls to roughly <code>W &asymp; k<sub>u</sub>e<sup>&minus;&Delta;E/kT</sup></code>. For an <strong>assumed</strong> lower-level gap of 0.2 eV at 300 K and the same upper-level decay as ruby (2e2 /s), the threshold is 0.087 /s.</p>
<p class="result">The ratio of the two thresholds is 2.3e3 for these assumptions (it is e<sup>&Delta;E/kT</sup>). Control: if the lower level empties more slowly than the upper decays, no pump rate inverts it.</p></div>
<div class="pt"><p>O livro diz que o esquema de quatro níveis precisa de muito menos potência de bombeamento (p.318), sem dar número. No nosso modelo o nível inferior esvazia a <code>k<sub>l</sub></code> e é reabastecido termicamente. A inversão exige <code>k<sub>l</sub> &gt; k<sub>u</sub></code> e o limiar cai para cerca de <code>k<sub>u</sub>e<sup>&minus;&Delta;E/kT</sup></code>. Com um intervalo <strong>assumido</strong> de 0.2 eV a 300 K e o mesmo decaimento superior do rubi (2e2 /s), o limiar é 0.087 /s, e a razão entre os dois limiares é 2.3e3.</p></div></div>

<div class="deriv"><h3><span class="en">3.4 Ruby, from the figure's numbers</span><span class="pt">3.4 O rubi, a partir dos números da figura</span></h3>
<div class="en"><p>The Fig. 10.12 caption gives 694.3 nm and the rate constants k<sub>f</sub> = 3e6 /s (fluorescence from the pumped level) and k<sub>e</sub> = 2e2 /s (the laser level). From them: the laser photon is 1.786 eV; the laser level lives 5.0 ms while fluorescence from the pumped level lasts 0.333 µs; after a 1 ms pump pulse 82 % of what reached the metastable level is still there; and the least energy stored to invert a mole of Cr(III) is half the ions at the photon energy, 86.1 kJ.</p>
<p class="result">Control: after a 50 ms pump pulse almost nothing would remain (e<sup>&minus;10</sup>), so a lamp slower than the metastable lifetime cannot build an inversion.</p></div>
<div class="pt"><p>A legenda da Fig. 10.12 dá 694.3 nm e as constantes k<sub>f</sub> = 3e6 /s e k<sub>e</sub> = 2e2 /s. Daí: o fóton do laser tem 1.786 eV; o nível do laser vive 5.0 ms e a fluorescência do nível bombeado dura 0.333 µs; após um pulso de bombeamento de 1 ms restam 82 % do que chegou ao nível metaestável; e a energia mínima armazenada para inverter um mol de Cr(III) é metade dos íons à energia do fóton, 86.1 kJ.</p></div></div>

<div class="deriv"><h3><span class="en">3.5 Doubling: wavelength, and what 20 % means</span><span class="pt">3.5 Dobramento: comprimento de onda e o que significam 20 %</span></h3>
<div class="en"><p>Doubling the frequency halves the wavelength: 694.3 nm becomes 347.15 nm (book p.319: 694 to 347 nm). The book gives "an efficiency of about 20 %" without saying energy or photons. Two fundamental photons make one doubled photon, so 20 % of the <em>energy</em> is only 10 % of the photons.</p>
<p>The book says a neodymium glass laser can be made to emit at 265 nm similarly. A fundamental near 1060 nm, which the pages read do not state, would give 265 nm after two doublings. One doubling would give 530 nm.</p>
<p class="result">Both figures are arithmetic on assumptions; the 1060 nm is from outside the book.</p></div>
<div class="pt"><p>Dobrar a frequência divide o comprimento de onda por dois: 694.3 nm vira 347.15 nm (livro p.319). O livro dá "cerca de 20 % de eficiência" sem dizer se é energia ou fótons. Dois fótons fundamentais fazem um fóton dobrado; 20 % da <em>energia</em> são só 10 % dos fótons. Um fundamental perto de 1060 nm, que as páginas lidas não informam, daria 265 nm após duas dobras.</p></div></div>

<div class="deriv"><h3><span class="en">3.6 Which pulse can reach the quoted power density?</span><span class="pt">3.6 Qual pulso alcança a densidade de potência citada?</span></h3>
<div class="en"><p>Page 317 says power densities as high as 1e19 W/cm&sup2; can be produced, in the paragraph that introduces Q-switched pulses. Page 319 gives the Q-switched pulse as several joules in nanoseconds, and page 320 gives mode-locked peak powers of 1e6 to 1e13 W. An order-of-magnitude check, taking a diffraction-limited spot of area about &lambda;&sup2; at 694.3 nm (4.82e-9 cm&sup2;):</p>
<p>A 1 J, 10 ns pulse is 1e8 W and reaches about 2e16 W/cm&sup2;. Getting 1e19 W/cm&sup2; at that spot needs 4.8e10 W, about 480 times more. The book's own mode-locked upper figure, 1e13 W, would reach about 2e21 W/cm&sup2;.</p>
<p class="result">So the quoted 1e19 is consistent with page 320's picosecond regime but not with a nanosecond Q-switched pulse. At an unfocused 1 mm&sup2; spot the same pulse gives only 1e10 W/cm&sup2;, which shows that the spot size is the assumption doing the work. This is a consistency check, not a laser design, and it does not say the book is wrong.</p></div>
<div class="pt"><p>A p.317 diz que densidades de potência de até 1e19 W/cm&sup2; podem ser produzidas, no parágrafo que introduz os pulsos com chave Q. A p.319 dá o pulso com chave Q como vários joules em nanossegundos, e a p.320 dá potências de pico de 1e6 a 1e13 W para travamento de modos. Com um ponto limitado por difração de área cerca de &lambda;&sup2; (4.82e-9 cm&sup2;): um pulso de 1 J e 10 ns é 1e8 W e alcança cerca de 2e16 W/cm&sup2;; chegar a 1e19 exige 4.8e10 W, cerca de 480 vezes mais; o limite de 1e13 W alcançaria 2e21 W/cm&sup2;.</p>
<p class="result">Logo, o 1e19 é coerente com o regime de picossegundos da p.320, não com um pulso de nanossegundos. Num ponto de 1 mm&sup2; sem foco, 1e10 W/cm&sup2;. É uma checagem de consistência, não um projeto, e não diz que o livro erra.</p></div></div>
""",
    calc=dict(
        head=dict(en="Try it: three-level and four-level pump thresholds", pt="Experimente: limiares de bombeamento de três e quatro níveis"),
        html="""<div class="calc"><label>upper-level decay k (1/s)<input id="c_k" type="number" value="200" step="10"></label>
<label>lower-level gap &Delta;E (eV)<input id="c_dE" type="number" value="0.2" step="0.01"></label>
<label>temperature T (K)<input id="c_T" type="number" value="300" step="10"></label>
<div class="out" id="c_out"></div></div>""",
        js="""
(function(){
 var kB=8.617333262e-5;
 function run(){
  var k=parseFloat(document.getElementById('c_k').value),dE=parseFloat(document.getElementById('c_dE').value),T=parseFloat(document.getElementById('c_T').value);
  var out=document.getElementById('c_out');
  if(!(k>0&&dE>=0&&T>0)){out.textContent='-';return;}
  var x=dE/(kB*T),W4=k*Math.exp(-x);
  out.innerHTML='three-level threshold &asymp; '+k.toPrecision(3)+' /s &middot; four-level threshold &asymp; '+W4.toPrecision(3)+' /s &middot; ratio = e<sup>&Delta;E/kT</sup> = '+Math.exp(x).toExponential(2)+' (formula approximations; see the verify script for the numerical solution)';
 }
 ['c_k','c_dE','c_T'].forEach(function(i){document.getElementById(i).addEventListener('input',run);});run();
})();"""),
    quiz=dict(
        q=dict(en="You want 347 nm light for flash photolysis and your only source is a Q-switched ruby laser. What do you add?",
               pt="Você quer luz de 347 nm para fotólise por pulso e sua única fonte é um laser de rubi com chave Q. O que você acrescenta?"),
        opts=[dict(en="A second ruby rod in series", pt="Uma segunda barra de rubi em série"),
              dict(en="A thermopile in the beam", pt="Uma termopilha no feixe"),
              dict(en="A sector wheel in the cavity", pt="Um disco setorado na cavidade"),
              dict(en="A frequency-doubling crystal such as KDP", pt="Um cristal dobrador de frequência como o KDP")],
        correct=3,
        ok=dict(en="Correct. Doubling halves the wavelength, 694.3 nm to 347.15 nm. Keep in mind the book's roughly 20 % efficiency, which is 10 % of the photons if it refers to energy.",
                pt="Correto. Dobrar reduz o comprimento de onda à metade, de 694.3 nm para 347.15 nm. Lembre da eficiência de cerca de 20 % do livro, que são 10 % dos fótons se for energia."),
        no=dict(en="No. A second rod gives more 694 nm, a thermopile only measures, and a sector wheel is a steady-state radical-lifetime tool. Halving the wavelength takes a frequency-doubling crystal.",
                pt="Não. Uma segunda barra dá mais 694 nm, a termopilha só mede, e o disco setorado é ferramenta de tempo de vida de radicais em estado estacionário. Reduzir o comprimento de onda à metade exige um cristal dobrador de frequência.")),
    notdo=dict(en="""<p>This room does not teach laser safety or design, and no laser is recommended. Every <em>book</em> statement is cited by page, from page scans of one textbook. Every <em>number in the derivations</em> comes from the verify script. Five things are open:</p>
<p><strong>The rate-equation models are ours.</strong> The book describes inversion in words. The thresholds depend on assumed values (a pumped level that decays at 1e9 /s, a lower laser level that empties at 1e9 /s, a 0.2 eV gap), not on the book.</p>
<p><strong>Figure values.</strong> The two rate constants come from the Fig. 10.12 caption on the page scan and are not independently confirmed.</p>
<p><strong>The 1060 nm fundamental</strong> is from outside the book. The book also labels the doubling crystal NH<sub>4</sub>H<sub>2</sub>PO<sub>4</sub> in Fig. 10.14 while the text says KDP; this page does not resolve that.</p>
<p><strong>The power-density check</strong> is an order-of-magnitude consistency argument.</p>
<p><strong>Portuguese.</strong> The Portuguese text was drafted by Claude and has not been reviewed by a native speaker.</p>""",
               pt="""<p>Esta sala não ensina segurança nem projeto de laser, e nenhum laser é recomendado. Cada afirmação do <em>livro</em> é citada por página; cada <em>número das derivações</em> vem do script. Cinco pontos em aberto: os modelos de taxa são nossos e dependem de valores assumidos; os valores da figura vêm da legenda da Fig. 10.12 e não foram confirmados de forma independente; o fundamental de 1060 nm é de fora do livro, e o livro rotula o cristal como NH<sub>4</sub>H<sub>2</sub>PO<sub>4</sub> na Fig. 10.14 e como KDP no texto; a checagem de densidade de potência é de ordem de grandeza; e o português foi redigido por Claude, sem revisão de falante nativo.</p>"""),
    verify="photochem-laser-verify.py",
    pages="book pp.317-321",
)
