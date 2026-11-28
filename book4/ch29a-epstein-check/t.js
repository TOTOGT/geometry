const {latticeSums,tail,eig2,Eval}=require('./core.js');
const ref=require('./ref.json');
for(const s of [2,3,5]){
 for(const [nm,x,y] of [['i',0,1],['rho',0.5,Math.sqrt(3)/2]]){
  const Rs=[10,20,40,80,160,320];
  const A=latticeSums(x,y,s,Rs);
  const r=ref[String(s)][nm];
  const a=A[5]; const ev=eig2(a[3],a[5],a[4]);
  console.log(s,nm,'f',(a[0]+tail(y,s,320)).toFixed(8),'ref',r.value.toFixed(8),'| ev',ev.map(v=>v.toFixed(5)).join(','),'ref',r.ev.map(v=>v.toFixed(5)).join(','),'| grad',a[1].toExponential(1),a[2].toExponential(1),'| trace',(y*y*(a[3]+a[4])).toFixed(5),(s*(s-1)*(a[0]+tail(y,s,320))).toFixed(5));
 }
}
// finite-diff check of derivative formulas at generic point
const s=2.7,x=0.23,y=1.17,R=60,h=1e-4;
const f=(X,Y)=>latticeSums(X,Y,s,[R])[0][0];
const a=latticeSums(x,y,s,[R])[0];
console.log('fx',a[1],(f(x+h,y)-f(x-h,y))/(2*h));
console.log('fy',a[2],(f(x,y+h)-f(x,y-h))/(2*h));
console.log('fxx',a[3],(f(x+h,y)-2*f(x,y)+f(x-h,y))/(h*h));
console.log('fyy',a[4],(f(x,y+h)-2*f(x,y)+f(x,y-h))/(h*h));
console.log('fxy',a[5],(f(x+h,y+h)-f(x+h,y-h)-f(x-h,y+h)+f(x-h,y-h))/(4*h*h));
// sign scan
let bad=[];
for(let s=1.5;s<=8.0001;s+=0.05){
  const ai=latticeSums(0,1,s,[300])[0], ar=latticeSums(0.5,Math.sqrt(3)/2,s,[300])[0];
  const evi=eig2(ai[3],ai[5],ai[4]), evr=eig2(ar[3],ar[5],ar[4]);
  if(!(evi[0]<0&&evi[1]>0&&evr[0]>0)) bad.push(s.toFixed(2));
}
console.log('scan violations',bad);
