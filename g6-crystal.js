/* g6-crystal.js — Principia Orthogona Crystal Navigator
   Deploy to: /geometry/g6-crystal.js
   Version: 1.0.0 · G6 LLC · 2026
*/
(function(){
'use strict';

const BASE = '/geometry/';

const CHAPTERS = [
  {id:'overture',  short:'OV', label:'Overture',        url:'overture.html',              op:'G', desc:'JPM at 26. Newark at 46. The wrong fixed point.'},
  {id:'prelude',   short:'PR', label:'Prelude',          url:'prelude.html',               op:'C', desc:'The cajueiro principle. Generator before surface.'},
  {id:'ch1',       short:'C1', label:'Ch 1 · Cajueiro',  url:'ch1.html',                   op:'C', desc:'The nut hangs outside the apple.'},
  {id:'ch2',       short:'C2', label:'Ch 2 · Matrix',    url:'ch2.html',                   op:'C', desc:'Generative matrix. Compression begins.'},
  {id:'ch3',       short:'C3', label:'Ch 3 · Circadian', url:'ch3-circadian.html',         op:'K', desc:'Biological K-threshold. The circadian clock.'},
  {id:'ch3c',      short:'3C', label:'Ch 3c · Trader',   url:'ch3c-econophysics.html',     op:'K', desc:'Legendrian alignment. JOMO. Timezone independence.'},
  {id:'ch4',       short:'C4', label:'Ch 4 · Neural',    url:'ch4-neural.html',            op:'K', desc:'Neural oscillations. Theta-gamma coupling.'},
  {id:'ch5',       short:'C5', label:'Ch 5 · Immune',    url:'ch5-immune.html',            op:'K', desc:'Immune adaptation. Two-signal gate.'},
  {id:'ch6',       short:'C6', label:'Ch 6 · Resonance', url:'ch6-resonance.html',         op:'F', desc:'Chladni. Hypogeum 110 Hz. Schumann. Crystal math.'},
  {id:'ch7',       short:'C7', label:'Ch 7 · Crystal',   url:'ch7-crystalline.html',       op:'F', desc:'G6 Crystal. Monster threshold g₆=33.'},
   {id:'chT',        short:'TU', label:'Ch T · Tubulin', url:'chT-tubulin.html',       op:'F', desc:'One protein. Fifteen architectures. Biology solved Ulam.'},
  {id:'ch8',       short:'C8', label:'Ch 8 · Axiomatic', url:'ch8-axiomatic.html',         op:'F', desc:'dm³ axioms A1–A8. The fold is testable.'},
  {id:'ch9',       short:'C9', label:'Ch 9 · φ',         url:'ch9-phi.html',               op:'F', desc:'Golden ratio. τ×ε₀=2/3<1. Stability condition.'},
  {id:'ch10',      short:'10', label:'Ch 10 · Lyapunov', url:'ch10-lyapunov.html',         op:'U', desc:'V=(r-1)². Convergence before knowing the trajectory.'},
  {id:'ch11',      short:'11', label:'Ch 11 · Spectral', url:'ch11-spectral.html',         op:'U', desc:'Spectral radius. μ_max=−2. The canonical bound.'},
  {id:'ocio',      short:'OC', label:'Ch · Ocio',        url:'ch-ocio.html',               op:'U', desc:'Ocio as fixed point. Monster Law. Hyper-Mahlo.'},
  {id:'ch12',      short:'12', label:'Ch 12 · Fixed Pt', url:'ch12-conclusion.html',       op:'G', desc:'Banach fixed point. G(x*)=x*. You are the proof.'},
  {id:'chH',       short:'CZ', label:'Ch H · Collatz',   url:'chH-collatz.html',           op:'G', desc:'Collatz as dm³ corollary. Three gaps. AXLE T5.'},
  {id:'ch17',      short:'EP', label:'Ch 17 · Epilogue', url:'ch17-epilogue.html',         op:'G', desc:'The living book constellation. The fixed point.'},
  {id:'portal',    short:'SP', label:'Student Portal',   url:'Sportal.html',               op:'C', desc:'A1→D2 structured prompts. The full learning arc.'},
  {id:'impa',      short:'IM', label:'IMPA Portal',      url:'impa-portal.html',           op:'G', desc:'Brazil. Bilingual. XII Bienal SBM.'},
];

const OP_COL = {
  C:{fill:'#3B8BD4',stroke:'#185FA5'},
  K:{fill:'#D85A30',stroke:'#993C1D'},
  F:{fill:'#639922',stroke:'#3B6D11'},
  U:{fill:'#7F77DD',stroke:'#534AB7'},
  G:{fill:'#BA7517',stroke:'#854F0B'},
};

let cv, ctx, W, H, nodes=[], rotX=0.32, rotY=0.5, drag=false, lx, ly, hov=null, zoom=1, raf=null, lastAct=Date.now();

function init(){
  cv = document.getElementById('g6-cryst-cv');
  if(!cv) return;
  ctx = cv.getContext('2d');
  buildNodes();
  resize();
  cv.addEventListener('mousedown', e=>{drag=true;lx=e.clientX;ly=e.clientY;lastAct=Date.now();});
  cv.addEventListener('touchstart', e=>{drag=true;lx=e.touches[0].clientX;ly=e.touches[0].clientY;lastAct=Date.now();},{passive:true});
  window.addEventListener('mouseup', ()=>drag=false);
  window.addEventListener('touchend', ()=>drag=false);
  cv.addEventListener('mousemove', onMove);
  cv.addEventListener('touchmove', onTouch,{passive:true});
  cv.addEventListener('click', onClick);
  cv.addEventListener('wheel', e=>{e.preventDefault();zoom=Math.max(0.5,Math.min(2.2,zoom*(e.deltaY>0?0.93:1.08)));draw();lastAct=Date.now();},{passive:false});
  new ResizeObserver(resize).observe(cv);
  loop();
}

function buildNodes(){
  const ops=['C','K','F','U','G'];
  nodes = CHAPTERS.map((ch,i)=>{
    const opI = ops.indexOf(ch.op);
    const peers = CHAPTERS.filter(c=>c.op===ch.op);
    const pi = peers.indexOf(ch);
    const angle = (pi/peers.length)*Math.PI*2;
    const r = 72 + opI*36;
    const oy = (opI-2)*52;
    return {...ch, ox:Math.cos(angle)*r, oy, oz:Math.sin(angle)*r, r:15+(ch.op==='G'?4:0)};
  });
}

function proj(ox,oy,oz){
  const cX=Math.cos(rotX),sX=Math.sin(rotX),cY=Math.cos(rotY),sY=Math.sin(rotY);
  const x1=ox*cY+oz*sY, z1=-ox*sY+oz*cY;
  const y1=oy*cX-z1*sX, z2=oy*sX+z1*cX;
  const f=360*zoom/(360*zoom+z2+280);
  return {sx:W/2+x1*f, sy:H/2-35+y1*f, sc:f, z:z2};
}

function resize(){
  const rc=cv.getBoundingClientRect();
  W=cv.width=rc.width*devicePixelRatio;
  H=cv.height=rc.height*devicePixelRatio;
  ctx.scale(devicePixelRatio,devicePixelRatio);
  draw();
}

function draw(){
  const rW=W/devicePixelRatio, rH=H/devicePixelRatio;
  ctx.clearRect(0,0,W,H);

  const ps = nodes.map(n=>({...n,...proj(n.ox,n.oy,n.oz)})).sort((a,b)=>a.z-b.z);

  // Edges
  for(let i=0;i<ps.length;i++) for(let j=i+1;j<ps.length;j++){
    const a=ps[i],b=ps[j];
    const d=Math.hypot(a.ox-b.ox,a.oy-b.oy,a.oz-b.oz);
    if(d<110){
      const al=(1-d/110)*0.15;
      ctx.beginPath();ctx.moveTo(a.sx,a.sy);ctx.lineTo(b.sx,b.sy);
      ctx.strokeStyle=`rgba(201,168,76,${al})`;ctx.lineWidth=0.5;ctx.stroke();
    }
  }

  // Nodes
  for(const n of ps){
    const col=OP_COL[n.op];
    const r=n.r*n.sc*1.5;
    const isH=hov&&hov.id===n.id;
    if(isH){
      ctx.beginPath();ctx.arc(n.sx,n.sy,r*1.9,0,Math.PI*2);
      ctx.fillStyle='rgba(201,168,76,0.12)';ctx.fill();
    }
    ctx.beginPath();ctx.arc(n.sx,n.sy,r,0,Math.PI*2);
    ctx.fillStyle=col.fill+(isH?'ff':'bb');ctx.fill();
    ctx.strokeStyle=col.stroke;ctx.lineWidth=isH?1.5:0.5;ctx.stroke();
    if(r>7){
      ctx.fillStyle='#fff';
      ctx.font=`${Math.max(7,Math.round(r*0.62))}px "Courier New",monospace`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(n.short,n.sx,n.sy);
    }
  }

  // Legend
  ['C','K','F','U','G'].forEach((op,i)=>{
    const col=OP_COL[op];
    ctx.beginPath();ctx.arc(12,rH-80+i*16,5,0,Math.PI*2);
    ctx.fillStyle=col.fill;ctx.fill();
    ctx.font='9px "Courier New",monospace';ctx.textAlign='left';ctx.textBaseline='middle';
    ctx.fillStyle='rgba(201,168,76,0.45)';
    ctx.fillText(op,22,rH-80+i*16);
  });
}

function getHov(mx,my){
  let best=null,bd=Infinity;
  for(const n of nodes){
    const p=proj(n.ox,n.oy,n.oz);
    const r=(n.r+5)*p.sc*1.5;
    const d=Math.hypot(mx-p.sx,my-p.sy);
    if(d<r&&d<bd){bd=d;best=n;}
  }
  return best;
}

function setInfo(n){
  const t=document.getElementById('g6-ci-title');
  const d=document.getElementById('g6-ci-desc');
  if(!t||!d) return;
  if(!n){t.textContent='Book 3 · The Mini-Beast';d.textContent='Hover a node · click to open chapter';}
  else{t.textContent=n.label;d.textContent=n.desc;}
}

function onMove(e){
  const rc=cv.getBoundingClientRect();
  const mx=e.clientX-rc.left, my=e.clientY-rc.top;
  if(drag){rotY+=(e.clientX-lx)*0.009;rotX+=(e.clientY-ly)*0.007;rotX=Math.max(-1.2,Math.min(1.2,rotX));lx=e.clientX;ly=e.clientY;lastAct=Date.now();draw();}
  else{const h=getHov(mx,my);if(h!==hov){hov=h;setInfo(h);draw();}cv.style.cursor=h?'pointer':'crosshair';}
}

function onTouch(e){
  if(!drag)return;
  rotY+=(e.touches[0].clientX-lx)*0.009;rotX+=(e.touches[0].clientY-ly)*0.007;
  rotX=Math.max(-1.2,Math.min(1.2,rotX));lx=e.touches[0].clientX;ly=e.touches[0].clientY;lastAct=Date.now();draw();
}

function onClick(e){
  const rc=cv.getBoundingClientRect();
  const n=getHov(e.clientX-rc.left,e.clientY-rc.top);
  if(n) window.location.href=BASE+n.url;
}

function loop(){
  if(Date.now()-lastAct>2500&&!drag){rotY+=0.005;draw();}
  raf=requestAnimationFrame(loop);
}

// Init when panel first opens
const panel=document.getElementById('g6-cryst-panel');
if(panel){
  const obs=new MutationObserver(()=>{if(panel.classList.contains('g6-open')&&!ctx)init();});
  obs.observe(panel,{attributes:true,attributeFilter:['class']});
}

// Also init immediately if panel is already open
if(panel&&panel.classList.contains('g6-open')) init();

setInfo(null);

})();
