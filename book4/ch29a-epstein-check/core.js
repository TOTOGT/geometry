/* CORE-BEGIN */
function latticeSums(x,y,s,Rs){
  // Rs ascending radii; returns cumulative sums for each R of f,fx,fy,fxx,fyy,fxy over lattice points (m,n)!=0 with |m+nz|<=R
  const K=Rs.length, Rmax=Rs[K-1], R2=Rs.map(r=>r*r);
  const acc=[]; for(let k=0;k<K;k++) acc.push([0,0,0,0,0,0]);
  const nmax=Math.floor(Rmax/y);
  const ys=Math.pow(y,s);
  for(let n=-nmax;n<=nmax;n++){
    const b=n*y, rem=Rmax*Rmax-b*b; if(rem<0) continue;
    const sq=Math.sqrt(rem);
    const m0=Math.ceil(-n*x-sq), m1=Math.floor(-n*x+sq);
    for(let m=m0;m<=m1;m++){
      if(m===0&&n===0) continue;
      const a=m+n*x, q=a*a+b*b;
      let k=0; while(q>R2[k]) k++;
      const g=ys*Math.exp(-s*Math.log(q)), q2=q*q;
      const A=acc[k];
      A[0]+=g;
      A[1]+=g*(-2*s*n*a/q);
      A[2]+=g*(s/y)*(a*a-b*b)/q;
      A[3]+=g*2*s*n*n*((2*s+1)*a*a-b*b)/q2;
      A[4]+=g*(s/(y*y*q2))*(-4*s*b*b*q+2*b*b*((2*s+1)*b*b-a*a)+(s-1)*q2);
      A[5]+=g*2*s*a*b*(2*b*b*(s+1)-s*q)/(y*y*q2);
    }
  }
  for(let k=1;k<K;k++) for(let j=0;j<6;j++) acc[k][j]+=acc[k-1][j];
  return acc;
}
function tail(y,s,R){ return Math.PI*Math.pow(y,s-1)*Math.pow(R,2-2*s)/(s-1); }
function eig2(a,b,d){ const t=(a+d)/2, r=Math.sqrt(((a-d)/2)**2+b*b); return [t-r,t+r]; }
function Eval(x,y,s,R){ const a=latticeSums(x,y,s,[R])[0]; return a[0]+tail(y,s,R); }
/* CORE-END */
if(typeof module!=='undefined') module.exports={latticeSums,tail,eig2,Eval};
