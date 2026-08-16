const pptxgen = require('pptxgenjs');
const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';               // 13.3 x 7.5

const NAVY = '1A2744', DEEP = '111B2E', GOLD = 'C9A84C', CREAM = 'FAF7F0',
      MUTE = '8C93A3', GREEN = '7FB069', RED = 'C96A5A', RULE = '2E4070';
const H = 'Cambria', B = 'Calibri';

const W = 13.3, HT = 7.5, M = 0.7;

function base(dark){
  const s = p.addSlide();
  s.background = { color: dark ? DEEP : NAVY };
  return s;
}
function eyebrow(s, txt, color){
  s.addText(txt, { x:M, y:0.42, w:W-2*M, h:0.3, fontFace:B, fontSize:11,
    color: color||GOLD, charSpacing:3, bold:true, margin:0 });
}
function title(s, txt, y){
  s.addText(txt, { x:M, y:y||0.85, w:W-2*M, h:1.0, fontFace:H, fontSize:38,
    color:CREAM, bold:false, margin:0, valign:'top' });
}
function pill(s, x, y, txt, col){
  s.addText(txt, { x:x, y:y, w:1.5, h:0.3, fontFace:B, fontSize:10, bold:true,
    color:col, align:'center', valign:'middle', margin:0, charSpacing:2,
    fill:{ color:col, transparency:88 }, line:{ color:col, width:0.75 } });
}
function partBanner(s, txt, col){
  s.addText(txt, { x:M, y:HT-0.72, w:W-2*M, h:0.3, fontFace:B, fontSize:10,
    color:col, charSpacing:2, margin:0 });
}

/* ═══════════ SLIDE 1 — TITLE ═══════════ */
let s = base(true);
eyebrow(s, 'HIST 201 · WEEK 1 · THE ASCENT OF MAN');
s.addText('Kepler', { x:M, y:2.0, w:8.4, h:1.2, fontFace:H, fontSize:60, color:CREAM, margin:0 });
s.addText('The overreach, and what survived it', { x:M, y:3.15, w:8.4, h:0.6,
  fontFace:H, fontSize:22, color:GOLD, italic:true, margin:0 });
s.addText('Two models of the solar system, published by the same man, twenty-three years apart.\nOne of them is still in use. You are going to find out which — by checking.',
  { x:M, y:4.1, w:8.0, h:1.1, fontFace:B, fontSize:15, color:'C8CEDB', margin:0, lineSpacing:26 });
s.addShape(p.ShapeType.ellipse, { x:9.9, y:1.9, w:2.6, h:2.6,
  fill:{ color:GOLD, transparency:90 }, line:{ color:GOLD, width:1 } });
s.addShape(p.ShapeType.ellipse, { x:10.65, y:2.65, w:1.1, h:1.1, fill:{ color:GOLD } });
s.addText('PART ONE  ·  watch before you post your prediction', { x:M, y:HT-0.95, w:9, h:0.35,
  fontFace:B, fontSize:11, color:GOLD, charSpacing:2, margin:0 });
s.addNotes(
"Welcome to week one of HIST 201.\n\n" +
"This is the module the rest of the course is built on, so I want to be direct about what we are doing. " +
"You are not here to learn that Johannes Kepler discovered the laws of planetary motion. You probably already know that, and knowing it has never helped anybody do anything.\n\n" +
"You are here because Kepler published two different models of the solar system, twenty-three years apart, and he believed in both of them. One of those models is still used today to plan spacecraft trajectories. The other one is wrong. And here is the part that matters: at the time he published them, there was no obvious way to tell which was which. Both fit the data he had. Both were beautiful. He defended the wrong one for the rest of his life.\n\n" +
"This week you are going to do the arithmetic that separates them. It takes about ten minutes and a spreadsheet.\n\n" +
"This first video sets up the two models and stops. I am not going to tell you which one wins, because before you compute anything, you have to commit to a guess. That guess is graded on being posted on time and being specific. It is not graded on being right. I want to be very clear about that, because it changes how you should approach this: a confident wrong prediction earns full marks. Guessing safely earns you nothing.");

/* ═══════════ SLIDE 2 — THE MAN ═══════════ */
s = base();
eyebrow(s, 'WHO WE ARE TALKING ABOUT');
title(s, 'A man who wanted the universe to be beautiful');
const facts = [
  ['1571–1630', 'Württemberg, Graz, Prague, Linz. Lutheran in a Catholic empire, repeatedly expelled.'],
  ['The day job', 'Imperial Mathematician — which mostly meant casting horoscopes for the Emperor.'],
  ['The data', 'Tycho Brahe’s observations. The most precise in Europe, and Kepler spent years fighting the family for access to them.'],
  ['The temperament', 'He believed God was a geometer, and that the solar system had to be built on shapes.']
];
let yy = 2.15;
facts.forEach(function(f){
  s.addShape(p.ShapeType.ellipse, { x:M, y:yy, w:0.34, h:0.34, fill:{ color:GOLD, transparency:80 }, line:{ color:GOLD, width:0.75 } });
  s.addText(f[0], { x:M+0.55, y:yy-0.04, w:2.3, h:0.35, fontFace:B, fontSize:13, bold:true, color:GOLD, margin:0 });
  s.addText(f[1], { x:M+2.95, y:yy-0.06, w:8.5, h:0.85, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0, lineSpacing:20 });
  yy += 1.08;
});
partBanner(s, 'PART ONE  ·  no result is given in this video', MUTE);
s.addNotes(
"A little about the man, because his temperament is the whole story.\n\n" +
"Kepler was born in 1571 in what is now Germany. He was a Lutheran living in a Catholic empire, and he was expelled from cities more than once for refusing to convert. His official position was Imperial Mathematician, which sounds impressive and mostly meant casting horoscopes for an emperor who wanted to know whether to go to war.\n\n" +
"The data he worked from was not his own. It belonged to Tycho Brahe, a Danish nobleman with a metal nose and the most precise naked-eye observations in Europe. When Tycho died, Kepler spent years fighting Tycho's family for access to those notebooks. He needed them because his own eyesight was poor — he had contracted smallpox as a child and could not observe reliably himself.\n\n" +
"Now the important part. Kepler believed that God was a geometer. He believed the solar system was not an accident, that it had been built to a plan, and that the plan would turn out to be made of shapes. That belief is not incidental to his work. It is what motivated him to look for structure at all, and it is also what produced his worst mistake. Hold both of those in mind. We are not going to end up with a simple moral about mysticism being bad.");

/* ═══════════ SLIDE 3 — MODEL A ═══════════ */
s = base();
eyebrow(s, 'MODEL A · MYSTERIUM COSMOGRAPHICUM · 1596');
title(s, 'The five solids');
s.addText('There are exactly five regular solids — cube, tetrahedron, octahedron, dodecahedron, icosahedron. Euclid proved the list complete. Kepler knew six planets, which leaves five gaps between them.',
  { x:M, y:2.0, w:7.1, h:1.3, fontFace:B, fontSize:15, color:'C8CEDB', margin:0, lineSpacing:24 });
s.addText('Five solids. Five gaps. He thought that could not be a coincidence.',
  { x:M, y:3.35, w:7.1, h:0.7, fontFace:H, fontSize:19, color:GOLD, italic:true, margin:0, lineSpacing:26 });
s.addText([
  { text:'Nest each solid between two planetary spheres', options:{ bullet:true, breakLine:true } },
  { text:'Each solid fixes a ratio of outer radius to inner radius', options:{ bullet:true, breakLine:true } },
  { text:'That ratio is pure geometry — no measurement, no fitting', options:{ bullet:true, breakLine:false } }
], { x:M, y:4.3, w:7.1, h:1.5, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0, paraSpaceAfter:8 });
const solids = ['octahedron','icosahedron','dodecahedron','tetrahedron','cube'];
const gapsA  = ['Mercury → Venus','Venus → Earth','Earth → Mars','Mars → Jupiter','Jupiter → Saturn'];
let ty = 2.05;
s.addText('THE NESTING, OUTWARD', { x:8.3, y:1.65, w:4.3, h:0.3, fontFace:B, fontSize:10,
  bold:true, color:GOLD, charSpacing:2, margin:0 });
for (let i=0;i<5;i++){
  s.addShape(p.ShapeType.roundRect, { x:8.3, y:ty, w:4.3, h:0.62, rectRadius:0.06,
    fill:{ color:RULE, transparency:35 }, line:{ color:GOLD, width:0.5, transparency:55 } });
  s.addText(solids[i], { x:8.5, y:ty+0.04, w:2.1, h:0.26, fontFace:B, fontSize:12, bold:true, color:GOLD, margin:0 });
  s.addText(gapsA[i], { x:8.5, y:ty+0.3, w:3.9, h:0.26, fontFace:B, fontSize:11, color:'C8CEDB', margin:0 });
  ty += 0.72;
}
partBanner(s, 'PART ONE  ·  no result is given in this video', MUTE);
s.addNotes(
"Here is the first model, published in 1596, when Kepler was twenty-four.\n\n" +
"Start with a fact from Greek mathematics. There are exactly five regular solids — the cube, the tetrahedron, the octahedron, the dodecahedron and the icosahedron. Not four, not six. Euclid proved the list is complete, and it is one of the oldest classification results we have.\n\n" +
"Kepler knew of six planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn. Six planets leave five gaps between them.\n\n" +
"Five solids. Five gaps. He did not think that could be a coincidence.\n\n" +
"So he proposed this. Imagine each planet moving on a sphere. Between Mercury's sphere and Venus's, fit an octahedron — snugly, so the inner sphere touches its faces and the outer sphere passes through its corners. Between Venus and Earth, an icosahedron. Between Earth and Mars, a dodecahedron. Between Mars and Jupiter, a tetrahedron. Between Jupiter and Saturn, a cube.\n\n" +
"Now here is why this model is worth taking seriously rather than laughing at. Each solid fixes a specific ratio between the outer radius and the inner radius. That ratio comes out of the geometry alone. Kepler is not fitting anything to the data — he is deriving five numbers from pure mathematics and then asking whether the solar system matches them. That is a real prediction. It can fail.\n\n" +
"He called this his greatest discovery and defended it for the next thirty-four years.");

/* ═══════════ SLIDE 4 — MODEL B ═══════════ */
s = base();
eyebrow(s, 'MODEL B · HARMONICES MUNDI · 1619');
title(s, 'The third law');
s.addShape(p.ShapeType.roundRect, { x:M, y:2.05, w:5.6, h:1.55, rectRadius:0.08,
  fill:{ color:RULE, transparency:30 }, line:{ color:GOLD, width:0.75, transparency:45 } });
s.addText('T ²  ∝  a ³', { x:M, y:2.25, w:5.6, h:0.7, fontFace:H, fontSize:40, color:GOLD, align:'center', margin:0 });
s.addText('period squared goes as distance cubed', { x:M, y:2.98, w:5.6, h:0.4,
  fontFace:B, fontSize:13, color:'C8CEDB', align:'center', margin:0 });
s.addText('Twenty-three years later, in a book mostly about musical harmony, Kepler stated a relationship between how long a planet takes to go round and how far out it sits.',
  { x:M, y:3.9, w:5.6, h:1.3, fontFace:B, fontSize:14, color:'C8CEDB', margin:0, lineSpacing:23 });
s.addText('He gave it four sentences.\nHe thought the solids were the important part.',
  { x:M, y:5.25, w:5.6, h:0.9, fontFace:H, fontSize:16, color:GOLD, italic:true, margin:0, lineSpacing:24 });
s.addShape(p.ShapeType.roundRect, { x:7.0, y:2.05, w:5.6, h:4.1, rectRadius:0.08,
  fill:{ color:'000000', transparency:70 }, line:{ color:RULE, width:1 } });
s.addText('WHAT MAKES THIS DIFFERENT', { x:7.3, y:2.3, w:5.0, h:0.3, fontFace:B, fontSize:10,
  bold:true, color:GOLD, charSpacing:2, margin:0 });
s.addText([
  { text:'It is not a shape. It is a proportion — it says nothing about why.', options:{ bullet:true, breakLine:true } },
  { text:'It was extracted from Tycho’s measurements, not derived from geometry.', options:{ bullet:true, breakLine:true } },
  { text:'Kepler considered it decidedly the lesser of his two results.', options:{ bullet:true, breakLine:false } }
], { x:7.3, y:2.8, w:5.0, h:2.0, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0, paraSpaceAfter:10 });
s.addText('Both models were built from the same six planets and the same observer’s data.',
  { x:7.3, y:5.2, w:5.0, h:0.8, fontFace:B, fontSize:13, color:GOLD, italic:true, margin:0, lineSpacing:21 });
partBanner(s, 'PART ONE  ·  no result is given in this video', MUTE);
s.addNotes(
"Twenty-three years later, Kepler published a book called The Harmony of the World. Most of it is about musical harmony — he assigned tunes to the planets. Buried inside it is the second model.\n\n" +
"It says: take how long a planet takes to complete one orbit, and square it. Take how far out the planet sits, and cube it. Those two numbers track each other.\n\n" +
"That is it. That is the whole claim. Kepler gave it about four sentences.\n\n" +
"I want you to notice three things about how different this is from the solids.\n\n" +
"First, it is not a shape. It is a proportion. It offers no picture of the solar system and no explanation of why the relationship should hold. Kepler had no idea why it was true. Newton would supply that reason seventy years later.\n\n" +
"Second, it did not come from pure geometry. He pulled it out of Tycho's measurements by trying combinations until something matched. In modern language: it is a fit.\n\n" +
"Third, and this is the one that should bother you: Kepler thought this was the minor result. The solids were his masterpiece. This was a footnote in a book about music.\n\n" +
"So both models come from the same six planets and the same observer's notebooks. One is derived from mathematics and one is fitted to data — and if your instinct is that the derived one sounds more rigorous, hold on to that instinct. Write it down. You are about to test it.");

/* ═══════════ SLIDE 5 — THE TASK ═══════════ */
s = base();
eyebrow(s, 'WHAT YOU DO THIS WEEK');
title(s, 'Two columns, ten minutes');
s.addShape(p.ShapeType.roundRect, { x:M, y:2.0, w:5.8, h:2.5, rectRadius:0.08,
  fill:{ color:RULE, transparency:35 }, line:{ color:GOLD, width:0.75, transparency:50 } });
s.addText('COLUMN 1', { x:M+0.3, y:2.25, w:5.2, h:0.3, fontFace:B, fontSize:10, bold:true, color:GOLD, charSpacing:2, margin:0 });
s.addText('T ² ÷ a ³', { x:M+0.3, y:2.6, w:5.2, h:0.6, fontFace:H, fontSize:28, color:CREAM, margin:0 });
s.addText('For each of six planets. If the third law holds, this column does something recognisable. Six rows.',
  { x:M+0.3, y:3.3, w:5.2, h:1.0, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0, lineSpacing:22 });
s.addShape(p.ShapeType.roundRect, { x:6.9, y:2.0, w:5.7, h:2.5, rectRadius:0.08,
  fill:{ color:RULE, transparency:35 }, line:{ color:GOLD, width:0.75, transparency:50 } });
s.addText('COLUMN 2', { x:7.2, y:2.25, w:5.1, h:0.3, fontFace:B, fontSize:10, bold:true, color:GOLD, charSpacing:2, margin:0 });
s.addText('predicted ÷ actual', { x:7.2, y:2.6, w:5.1, h:0.6, fontFace:H, fontSize:26, color:CREAM, margin:0 });
s.addText('The five solid ratios are given to you. Compare each against the real spacing. Five rows.',
  { x:7.2, y:3.3, w:5.1, h:1.0, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0, lineSpacing:22 });
s.addText('Everything you need is in the spreadsheet. No algebra, no derivations — Tycho’s numbers are already typed in, and the solid ratios are already computed. You are doing division and comparing sizes.',
  { x:M, y:4.85, w:11.9, h:1.0, fontFace:B, fontSize:14, color:'C8CEDB', margin:0, lineSpacing:23 });
partBanner(s, 'PART ONE  ·  no result is given in this video', MUTE);
s.addNotes(
"Here is what you actually do, and I want to reassure you about the level. There is no algebra in this. There are no derivations. You will divide some numbers and compare the sizes of the results.\n\n" +
"The spreadsheet is in the module. Tycho's numbers are already typed in — orbital period and average distance for six planets, in units where the Earth is one. The five geometric ratios are already computed for you, so you do not need to know anything about solid geometry.\n\n" +
"Column one: for each of the six planets, divide the period squared by the distance cubed. Six rows. Look at what comes out. You are looking for whether the six numbers do anything recognisable.\n\n" +
"Column two: for each of the five gaps between planets, compare the ratio the solid predicts against the ratio the solar system actually has. Five rows. Look at how close they are.\n\n" +
"That is the entire task. If it takes you more than fifteen minutes, something has gone wrong with the spreadsheet and you should post in the help forum.\n\n" +
"One instruction that matters more than the arithmetic: do not open the spreadsheet yet.");

/* ═══════════ SLIDE 6 — THE GATE ═══════════ */
s = base(true);
eyebrow(s, 'BEFORE YOU OPEN THE SPREADSHEET');
s.addText('Post your prediction', { x:M, y:1.5, w:11.9, h:0.9, fontFace:H, fontSize:44, color:CREAM, margin:0 });
s.addText('Two sentences. Which model fits better, and roughly how much better?',
  { x:M, y:2.5, w:11.9, h:0.5, fontFace:H, fontSize:20, color:GOLD, italic:true, margin:0 });
const gate = [
  ['Graded on', 'Being posted on time, and being specific enough to be wrong.'],
  ['Not graded on', 'Being correct. A confident wrong answer earns full marks.'],
  ['Why it is locked', 'You cannot read anyone else’s post until you have written yours.'],
  ['Your tutor', 'Kepler is in the tutor deck. In "before" mode he will not give you the answer — he does not have it.']
];
let gy = 3.35;
gate.forEach(function(g, i){
  s.addShape(p.ShapeType.roundRect, { x:M, y:gy, w:11.9, h:0.72, rectRadius:0.06,
    fill:{ color: i===1 ? GREEN : RULE, transparency: i===1 ? 88 : 40 },
    line:{ color: i===1 ? GREEN : RULE, width:0.75 } });
  s.addText(g[0], { x:M+0.25, y:gy+0.2, w:2.5, h:0.32, fontFace:B, fontSize:12, bold:true,
    color: i===1 ? GREEN : GOLD, margin:0 });
  s.addText(g[1], { x:M+2.95, y:gy+0.18, w:8.7, h:0.4, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0 });
  gy += 0.84;
});
s.addText('End of Part One. Part Two unlocks after the computation deadline.',
  { x:M, y:HT-0.85, w:11.9, h:0.35, fontFace:B, fontSize:12, color:GOLD, charSpacing:1, margin:0 });
s.addNotes(
"Stop the video here and go and post your prediction.\n\n" +
"Two sentences is enough. Which of the two models do you expect to fit the real solar system better, and roughly how much better? You can say something like: I think the geometric one wins because it comes from mathematics rather than curve-fitting, and I expect it to be within a percent or two. Or the opposite. Either is a good answer.\n\n" +
"What makes it a good answer is that it is specific enough to be wrong. \"I think one of them will be better\" is not a prediction, and it will not get full marks. \"The solids will be within five percent and the third law will be worse\" is a real prediction. If it turns out to be badly wrong, you still get full marks, and you will remember this module for years.\n\n" +
"The forum is locked until you post. You will not be able to read what anyone else said until your own is in. That is deliberate, and it is not about catching anyone out — it is because a prediction you make after reading someone else's is not your prediction, and it will not teach you anything.\n\n" +
"Kepler himself is available in the tutor deck if you want to talk to him first. In before-mode he will not tell you the answer, and I want to be precise about why: it is not that he is refusing. The prompt that builds him does not contain the answer at all. He cannot leak what he was never given. He will ask you what you expect, and he will help you understand the two models, the units, and how to set up the sheet.\n\n" +
"Go and post. Then compute. Part two unlocks after the deadline.");

/* ═══════════ SLIDE 7 — PART TWO OPENER ═══════════ */
s = base(true);
eyebrow(s, 'PART TWO · AFTER THE DEADLINE');
s.addText('What the numbers did', { x:M, y:2.4, w:11.9, h:1.1, fontFace:H, fontSize:52, color:CREAM, margin:0 });
s.addText('You have the two columns in front of you. Let us read them together.',
  { x:M, y:3.6, w:11.9, h:0.6, fontFace:H, fontSize:20, color:GOLD, italic:true, margin:0 });
s.addShape(p.ShapeType.ellipse, { x:10.2, y:4.6, w:2.0, h:2.0, fill:{ color:GOLD, transparency:92 }, line:{ color:GOLD, width:1 } });
partBanner(s, 'PART TWO  ·  do not watch before you have computed', GOLD);
s.addNotes(
"Welcome back. You have posted a prediction and you have run the two columns. Now we read them.\n\n" +
"Before I show you anything, I want you to have your own numbers open in front of you. Not because I am going to test you on them, but because the point of the next five minutes is comparing what you got against what you expected, and that comparison only works if both are actually in front of you.\n\n" +
"If you have not computed yet, stop this video. Nothing here will make sense in the right order, and you will have spent the effort of the prediction for nothing.");

/* ═══════════ SLIDE 8 — COLUMN ONE ═══════════ */
s = base();
eyebrow(s, 'COLUMN ONE · THE THIRD LAW');
title(s, 'The fitted one held');
const rows = [
  ['Mercury','0.9996','0.04 %'],
  ['Venus','1.0002','0.02 %'],
  ['Earth','1.0000','0.00 %'],
  ['Mars','1.0000','0.00 %'],
  ['Jupiter','0.9985','0.15 %'],
  ['Saturn','0.9861','1.39 %']
];
s.addTable(
  [[{ text:'Planet', options:{ bold:true, color:GOLD, fontSize:12 } },
    { text:'T² ÷ a³', options:{ bold:true, color:GOLD, fontSize:12 } },
    { text:'off by', options:{ bold:true, color:GOLD, fontSize:12 } }]].concat(
    rows.map(function(r){ return [
      { text:r[0], options:{ color:'C8CEDB', fontSize:13 } },
      { text:r[1], options:{ color:CREAM, fontSize:13, bold:true } },
      { text:r[2], options:{ color:GREEN, fontSize:13 } } ]; })),
  { x:M, y:2.05, w:5.5, colW:[1.9,1.9,1.7], rowH:0.42, fontFace:B,
    border:{ type:'solid', color:RULE, pt:0.5 }, fill:{ color:NAVY }, valign:'middle', margin:4 });
s.addText('1.4 %', { x:7.2, y:2.2, w:5.4, h:1.2, fontFace:H, fontSize:72, color:GREEN, margin:0 });
s.addText('worst case, across the whole set', { x:7.2, y:3.35, w:5.4, h:0.4, fontFace:B, fontSize:14, color:'C8CEDB', margin:0 });
s.addText('Saturn sits forty times further out than Mercury. The ratio holds across that entire range, and the one visible drift — Saturn — is the planet Tycho had watched for the shortest fraction of an orbit.',
  { x:7.2, y:4.0, w:5.4, h:1.6, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0, lineSpacing:22 });
pill(s, 7.2, 5.7, 'VERIFIED', GREEN);
s.addText('arithmetic, reproducible from the sheet', { x:8.85, y:5.72, w:3.8, h:0.3, fontFace:B, fontSize:11, color:MUTE, margin:0 });
partBanner(s, 'PART TWO', GOLD);
s.addNotes(
"Column one. Period squared over distance cubed, for six planets.\n\n" +
"Mercury: nought point nine nine nine six. Venus: one point nought nought nought two. Earth: one, by construction, because we measured everything in Earth units. Mars: one. Jupiter: nought point nine nine eight five. Saturn: nought point nine eight six one.\n\n" +
"They are all one. The worst of them is off by one point four percent, and that is Saturn.\n\n" +
"Now, one point four percent might not sound remarkable until you look at what it is holding across. Saturn orbits about forty times further from the Sun than Mercury does, and takes a hundred and twenty times longer to get round. This is not a relationship that holds approximately in a narrow band. It holds across the entire solar system Kepler could see.\n\n" +
"And the one visible drift is worth a moment. Saturn is the outermost planet on the list and it takes twenty-nine years to complete an orbit. Tycho observed for roughly twenty. Saturn is the planet he had watched through the smallest fraction of a single circuit, so it is the one with the least constrained data. The largest error sits exactly where you would expect the measurement to be weakest — which is a good sign, not a bad one.\n\n" +
"I have tagged this VERIFIED, and I mean something narrow by that: it is arithmetic, and you can reproduce it from the sheet. That tag is not doing any work about whether the law is true in general. We will come back to that.");

/* ═══════════ SLIDE 9 — COLUMN TWO ═══════════ */
s = base();
eyebrow(s, 'COLUMN TWO · THE FIVE SOLIDS');
title(s, 'The derived one did not');
const rows2 = [
  ['Mercury → Venus','octahedron','1.732','1.869','+7.9 %'],
  ['Venus → Earth','icosahedron','1.258','1.383','+9.9 %'],
  ['Earth → Mars','dodecahedron','1.258','1.524','+21.1 %'],
  ['Mars → Jupiter','tetrahedron','3.000','3.415','+13.8 %'],
  ['Jupiter → Saturn','cube','1.732','1.841','+6.3 %']
];
s.addTable(
  [[{ text:'Gap', options:{ bold:true, color:GOLD, fontSize:11 } },
    { text:'Solid', options:{ bold:true, color:GOLD, fontSize:11 } },
    { text:'predicted', options:{ bold:true, color:GOLD, fontSize:11 } },
    { text:'actual', options:{ bold:true, color:GOLD, fontSize:11 } },
    { text:'off by', options:{ bold:true, color:GOLD, fontSize:11 } }]].concat(
    rows2.map(function(r){ return [
      { text:r[0], options:{ color:'C8CEDB', fontSize:12 } },
      { text:r[1], options:{ color:MUTE, fontSize:12 } },
      { text:r[2], options:{ color:CREAM, fontSize:12 } },
      { text:r[3], options:{ color:CREAM, fontSize:12 } },
      { text:r[4], options:{ color:RED, fontSize:12, bold:true } } ]; })),
  { x:M, y:2.05, w:8.5, colW:[2.2,1.8,1.5,1.4,1.6], rowH:0.44, fontFace:B,
    border:{ type:'solid', color:RULE, pt:0.5 }, fill:{ color:NAVY }, valign:'middle', margin:4 });
s.addText('6 – 21 %', { x:9.5, y:2.2, w:3.1, h:1.0, fontFace:H, fontSize:44, color:RED, margin:0 });
s.addText('every gap, all five wrong in the same direction', { x:9.5, y:3.2, w:3.1, h:0.9,
  fontFace:B, fontSize:13, color:'C8CEDB', margin:0, lineSpacing:20 });
s.addText('Not one of the five is close. And they all miss the same way — the real planets sit further apart than the solids allow.',
  { x:9.5, y:4.2, w:3.1, h:1.6, fontFace:B, fontSize:13, color:'C8CEDB', margin:0, lineSpacing:21 });
partBanner(s, 'PART TWO', GOLD);
s.addNotes(
"Column two. The five solids.\n\n" +
"Mercury to Venus, the octahedron: geometry says the ratio should be one point seven three two. The solar system says one point eight six nine. Off by about eight percent.\n\n" +
"Venus to Earth, the icosahedron: predicted one point two five eight, actual one point three eight three. Off by ten percent.\n\n" +
"Earth to Mars, the dodecahedron: predicted one point two five eight, actual one point five two four. That is off by twenty-one percent.\n\n" +
"Mars to Jupiter, the tetrahedron: predicted three, actual three point four two. Fourteen percent.\n\n" +
"Jupiter to Saturn, the cube: predicted one point seven three two, actual one point eight four. Six percent.\n\n" +
"Not one of the five is close. The best of them is off by six percent, which is more than four times worse than the worst error in column one.\n\n" +
"And notice one more thing, because it is the detail that makes this a genuine falsification rather than just poor agreement. Every single one misses in the same direction. The real planets always sit further apart than the solids allow. If the errors were scattered — some too big, some too small — you might argue for measurement noise. A consistent one-way bias across all five is the signature of a model that is simply not describing the thing.");

/* ═══════════ SLIDE 10 — THE CHART ═══════════ */
s = base();
eyebrow(s, 'THE TWO COLUMNS, SIDE BY SIDE');
title(s, 'Same man. Same data. Same decade.');
s.addChart(p.ChartType.bar, [
  { name:'Platonic solids (derived)', labels:['Mer→Ven','Ven→Ear','Ear→Mar','Mar→Jup','Jup→Sat'],
    values:[7.9, 9.9, 21.1, 13.8, 6.3] },
  { name:'Third law (fitted)', labels:['Mer→Ven','Ven→Ear','Ear→Mar','Mar→Jup','Jup→Sat'],
    values:[0.02, 0.00, 0.00, 0.15, 1.39] }
], { x:M, y:1.95, w:11.9, h:4.3,
  barDir:'col', barGrouping:'clustered', barGapWidthPct:60,
  chartColors:[RED, GREEN],
  showTitle:true, title:'Percentage error against the real solar system', titleFontSize:13,
  titleColor:GOLD, titleFontFace:B,
  showValue:true, dataLabelPosition:'outEnd', dataLabelColor:CREAM,
  dataLabelFontSize:10, dataLabelFontFace:B, dataLabelFormatCode:'0.0"%"',
  showLegend:true, legendPos:'t', legendColor:'C8CEDB', legendFontSize:11, legendFontFace:B,
  catAxisLabelColor:'C8CEDB', catAxisLabelFontSize:11, catAxisLabelFontFace:B,
  valAxisLabelColor:'C8CEDB', valAxisLabelFontSize:10, valAxisLabelFontFace:B,
  valAxisMaxVal:24, valAxisMajorUnit:6,
  valGridLine:{ color:RULE, size:0.5 }, catGridLine:{ style:'none' },
  plotArea:{ fill:{ color:NAVY } }, chartArea:{ fill:{ color:NAVY } } });
partBanner(s, 'PART TWO', GOLD);
s.addNotes(
"Here they are together. Red is the model derived from pure geometry. Green is the model fitted to data.\n\n" +
"I want to let that sit for a second, because the shape of this chart is the entire week.\n\n" +
"The green bars are essentially invisible. The largest of them, Saturn, reaches one point four percent. The red bars run from six to twenty-one.\n\n" +
"Same man. Same six planets. Same observer's notebooks. Published twenty-three years apart by someone who was certain the red one was his masterpiece and the green one was a curiosity.\n\n" +
"Now — how many of you predicted this? Go and read the forum, which is unlocked now. In my experience most of a cohort predicts the opposite, and the reason is worth naming: the solids model sounds more rigorous. It comes from mathematics. It was not fitted to anything. That is a genuinely good instinct about what makes a claim strong, and this week it points the wrong way.\n\n" +
"If you predicted wrong, you have just learned something that people who predicted right did not. That is not a consolation prize. That is the mechanism.");

/* ═══════════ SLIDE 11 — WHAT IT ESTABLISHES ═══════════ */
s = base();
eyebrow(s, 'BE PRECISE ABOUT WHAT JUST HAPPENED');
title(s, 'What this establishes — and what it does not');
const cols = [
  ['What the computation shows', GREEN, [
    'The five solid ratios do not match the real spacings. All five miss, all in the same direction.',
    'T² ÷ a³ is constant across six planets to within 1.4%.'
  ]],
  ['What it does NOT show', RED, [
    'That the third law is true. Six planets is six data points — it is consistent with them, which is weaker.',
    'That deriving from mathematics is worse than fitting. That is not the lesson.'
  ]]
];
let cx = M;
cols.forEach(function(c){
  s.addShape(p.ShapeType.roundRect, { x:cx, y:2.0, w:5.8, h:3.15, rectRadius:0.08,
    fill:{ color:c[1], transparency:93 }, line:{ color:c[1], width:1 } });
  s.addText(c[0], { x:cx+0.3, y:2.25, w:5.2, h:0.35, fontFace:B, fontSize:13, bold:true, color:c[1], margin:0 });
  let iy = 2.75;
  c[2].forEach(function(t){
    s.addText(t, { x:cx+0.3, y:iy, w:5.2, h:1.05, fontFace:B, fontSize:13, color:'C8CEDB', margin:0, lineSpacing:21 });
    iy += 1.15;
  });
  cx += 6.1;
});
s.addText('The real difference is what happened next. The third law was later checked against planets Kepler never saw, against the moons of Jupiter, and against exoplanets found four centuries after his death. It kept holding. The solids were never checked against anything else, because there was nothing else to check them against — five gaps was all the model ever had.',
  { x:M, y:5.45, w:11.9, h:1.2, fontFace:B, fontSize:14, color:CREAM, margin:0, lineSpacing:23 });
partBanner(s, 'PART TWO', GOLD);
s.addNotes(
"Now I want to be careful, because it would be easy to walk away from this with the wrong lesson.\n\n" +
"Here is what your computation actually established. The five solid ratios do not match the real planetary spacings — all five miss, all in the same direction, by six to twenty-one percent. And the quantity T squared over a cubed is constant across six planets to within one point four percent.\n\n" +
"Here is what it did not establish.\n\n" +
"It did not show that the third law is true. Six planets is six data points. What you showed is that the law is consistent with them, and consistency is a much weaker claim than truth. A relationship can fit six points and fail on the seventh. This distinction — fits the data versus is true — is the one this whole course turns on, and if you take one thing from week one, take that.\n\n" +
"And it did not show that deriving things from mathematics is worse than fitting them to data. That would be a terrible lesson and it is not what happened.\n\n" +
"So what did happen? The real difference is what came afterwards. The third law was later tested against planets Kepler never knew existed — Uranus, Neptune. Against the moons of Jupiter, which are a completely separate system. Against exoplanets discovered four hundred years after he died. It kept holding, every time, in situations he could not have fitted it to.\n\n" +
"The solids were never tested against anything else. Not because nobody tried, but because there was nothing else to try. The model had exactly five gaps in it, and those five gaps were the same five it was built from. A model that can only ever be checked against the data that produced it is not a strong model, however elegant it looks. That is the actual lesson, and it applies to a great deal more than astronomy.");

/* ═══════════ SLIDE 12 — CARRY THIS ═══════════ */
s = base(true);
eyebrow(s, 'CARRY THIS OUT OF THE WEEK');
s.addText('A model that can only be checked\nagainst the data that made it\nhas not been checked.',
  { x:M, y:1.9, w:11.0, h:2.4, fontFace:H, fontSize:34, color:CREAM, margin:0, lineSpacing:52 });
s.addShape(p.ShapeType.roundRect, { x:M, y:4.6, w:11.9, h:1.5, rectRadius:0.08,
  fill:{ color:GOLD, transparency:92 }, line:{ color:GOLD, width:1 } });
s.addText('This week’s reading', { x:M+0.35, y:4.8, w:11.2, h:0.3, fontFace:B, fontSize:11,
  bold:true, color:GOLD, charSpacing:2, margin:0 });
s.addText('Kepler’s Other Correspondents  ·  book7/ch-keplers-correspondents.html  —  written above this level on purpose. Use the Kepler tutor to get through it, and remember the chapter outranks the tutor.',
  { x:M+0.35, y:5.2, w:11.2, h:0.8, fontFace:B, fontSize:13.5, color:'C8CEDB', margin:0, lineSpacing:22 });
s.addText('Reconcile post due Sunday  ·  read the forum, reply to two classmates on where their prediction and result diverged',
  { x:M, y:HT-0.8, w:11.9, h:0.35, fontFace:B, fontSize:12, color:GOLD, charSpacing:1, margin:0 });
s.addNotes(
"One sentence to carry out of this week.\n\n" +
"A model that can only be checked against the data that made it has not really been checked.\n\n" +
"That is Kepler's solids. It is also a great deal of what you will be handed at work for the rest of your life — a forecast tuned until it matches last year, a scoring model validated on the customers it was built from, a study whose hypothesis was chosen after the data came in. The shape of the error is identical, and now you have done the arithmetic that exposes it once, by hand, on a real historical case. You will recognise it again.\n\n" +
"Your reading this week is the chapter called Kepler's Other Correspondents. I will be honest with you: it is written above the level of this course, deliberately. It is a real research chapter and you are meant to reach for it, not absorb it in one pass. Use the Kepler tutor to work through the parts that are dense — that is exactly what it is for.\n\n" +
"And keep the rule in mind: the chapter outranks the tutor. If they disagree, the chapter is right and the tutor is wrong, and finding one of those disagreements is worth a post of its own.\n\n" +
"Reconcile post is due Sunday. The forum is open. Go and see how the rest of the cohort predicted, and reply to two people about where their expectation and their result came apart. See you next week.");

p.writeFile({ fileName: 'HIST201-Wk01-Kepler.pptx' }).then(function(f){ console.log('WROTE', f); });
