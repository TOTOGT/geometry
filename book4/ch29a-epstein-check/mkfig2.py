import sys;sys.path.insert(0,'.')
import numpy as np,math,json
from field import Egrad
from scipy.interpolate import RegularGridInterpolator as RGI
from contourpy import contour_generator
w=0.3;N=121
S=135/w;CX,CY=190,190
def X_(dx):return CX+S*dx
def Y_(dy):return CY-S*dy
centres={'i':(0.0,1.0),'rho':(0.5,math.sqrt(3)/2)}
ref=json.load(open('book4/ch29a-epstein-check/ref.json'))['2']
d={}
for k,(x0,y0) in centres.items():
    g=np.linspace(-w*1.15,w*1.15,N)  # a bit beyond the frame
    GX,GY=np.meshgrid(x0+g,y0+g,indexing='xy')
    E,Ex,Ey=Egrad(GX,GY)
    d[k]=(g,E,Ex,Ey,GY)
def fieldfun(k):
    g,E,Ex,Ey,GY=d[k];x0,y0=centres[k]
    fx=RGI((g,g),(-(y0+g)[:,None]**2*Ex.T*0+0)) if False else None
    # arrays indexed [ix,iy]
    Xv=-( (y0+g)[None,:]**2 )*Ex.T   # X_x at (ix,iy): E arrays are [iy,ix] -> transpose
    Yv=-( (y0+g)[None,:]**2 )*Ey.T
    fX=RGI((g,g),Xv,method='cubic');fY=RGI((g,g),Yv,method='cubic')
    return lambda dx,dy:(float(fX([[dx,dy]])[0]),float(fY([[dx,dy]])[0]))
def traj(f,p,dt=0.002,maxn=6000,lim=w*1.12):
    pts=[p];x,y=p
    for _ in range(maxn):
        k1=f(x,y);k2=f(x+dt/2*k1[0],y+dt/2*k1[1]);k3=f(x+dt/2*k2[0],y+dt/2*k2[1]);k4=f(x+dt*k3[0],y+dt*k3[1])
        x+=dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]);y+=dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        if abs(x)>lim or abs(y)>lim: break
        pts.append((x,y))
        if math.hypot(x,y)<0.012 and True and kind=='rho': break
    return pts
def path(pts):return 'M'+' L'.join(f'{X_(x):.1f},{Y_(y):.1f}' for x,y in pts)
def clip(pts):return [(x,y) for x,y in pts if abs(x)<=w and abs(y)<=w]
def contours(k,levels):
    g,E,Ex,Ey,GY=d[k];x0,y0=centres[k]
    Ec=E-E[N//2,N//2] if False else None
    return g,E
out={}
checks={}
for kind in ('i','rho'):
    f=fieldfun(kind);g,E,Ex,Ey,GY=d[kind];x0,y0=centres[kind]
    # centre energy from reference
    Ec=ref[kind]['value']
    Z=E-Ec  # indexed [iy,ix]
    gen=contour_generator(g,g,Z)
    levels=[-0.12,-0.06,0.0,0.15,0.35,0.65] if kind=='i' else [0.03,0.08,0.16,0.26,0.36]
    cont=[]
    for L in levels:
        for line in gen.lines(L if L!=0.0 else 1e-9):
            pts=[(x,y) for x,y in line]
            cont.append((L,pts))
    # arrows grid
    arrows=''
    n=7;L=0.05
    for i in range(n):
        for j in range(n):
            dx=-w*0.86+i*(w*1.72/(n-1));dy=-w*0.86+j*(w*1.72/(n-1))
            if abs(dx)<0.045 and abs(dy)<0.045: continue
            vx,vy=f(dx,dy);nn=math.hypot(vx,vy)
            if nn<1e-9: continue
            ux,uy=vx/nn,vy/nn
            arrows+=f'<line x1="{X_(dx-ux*L/2):.1f}" y1="{Y_(dy-uy*L/2):.1f}" x2="{X_(dx+ux*L/2):.1f}" y2="{Y_(dy+uy*L/2):.1f}" marker-end="url(#ah)"/>'
    # integral curves
    starts=[]
    if kind=='i':
        for sx in (-0.22,-0.12,-0.05,0.05,0.12,0.22):
            starts+= [(sx,w*1.08),(sx,-w*1.08)]
        # near-stable-manifold and near-unstable starts
        starts+=[(0.004,w*1.08),(-0.004,-w*1.08)]
    else:
        for kk in range(12):
            th=kk*math.pi/6+0.2;starts.append((0.285*math.cos(th),0.285*math.sin(th)))
    curves=[];heads=''
    maxdE=0;idcheck=[]
    for st in starts:
        pts=traj(f,st)
        cp=clip(pts)
        if len(cp)<4: continue
        curves.append(path(cp))
        m=len(cp)//3;(x1,y1),(x2,y2)=cp[m],cp[min(m+3,len(cp)-1)]
        ang=math.atan2(-(y2-y1),(x2-x1))  # svg angle
        px,py=X_(x1),Y_(y1);t=8
        heads+=f'<polygon points="{px+t*math.cos(ang):.1f},{py+t*math.sin(ang):.1f} {px+t*0.6*math.cos(ang+2.5):.1f},{py+t*0.6*math.sin(ang+2.5):.1f} {px+t*0.6*math.cos(ang-2.5):.1f},{py+t*0.6*math.sin(ang-2.5):.1f}"/>'
    # identity check along one trajectory: dE/dt vs -y^2|gradE|^2
    st=starts[0];pts=traj(f,st,maxn=150)[::1]
    xs=np.array([x0+p[0] for p in pts]);ys=np.array([y0+p[1] for p in pts])
    Ev,Exv,Eyv=Egrad(xs,ys)
    dt=0.002
    num=(Ev[2:]-Ev[:-2])/(2*dt);ana=-(ys[1:-1]**2)*(Exv[1:-1]**2+Eyv[1:-1]**2)
    checks[kind]=float(np.max(np.abs(num-ana)/np.abs(ana)))
    out[kind]=dict(cont=cont,arrows=arrows,curves=curves,heads=heads)
# separatrix check at i: unstable branch from near i along +x stays on |z|=1?
f=fieldfun('i');kind='i'
p=traj(f,(1e-3,0.0),dt=0.002,maxn=900)
dev=max(abs(math.hypot(x,1+y)-1) for x,y in p[100:])
checks['unit_circle_dev']=dev
# stable branch: start on imaginary axis above
p2=traj(f,(0.0,w*1.05),dt=0.002,maxn=3000)
checks['axis_dev']=max(abs(x) for x,y in p2)
print(checks,file=sys.stderr)
Rr=1;fr=f'<rect x="{X_(-w):.1f}" y="{Y_(w):.1f}" width="{2*S*w:.1f}" height="{2*S*w:.1f}" fill="none" stroke="var(--line)"/>'
def panel(kind,title,sub,aria,extra,tag):
    o=out[kind]
    cs=''
    for L,pts in o['cont']:
        cls='z' if abs(L)<1e-8 else ('lo' if L<0 else 'hi')
        cs+=f'<path class="{cls}" d="{path(pts)}"/>'
    cv=''.join(f'<path class="ic" d="{c}"/>' for c in o['curves'])
    svg=f'''<svg viewBox="0 0 360 400" role="img" aria-label="{aria}"><title>{aria}</title>
<defs><marker id="ah{tag}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker><clipPath id="cl{tag}"><rect x="{X_(-w):.1f}" y="{Y_(w):.1f}" width="{2*S*w:.1f}" height="{2*S*w:.1f}"/></clipPath></defs>
<text class="t" x="180" y="24" text-anchor="middle">{title}</text>
<g clip-path="url(#cl{tag})">{cs}<g class="ar fld">{o['arrows'].replace('#ah','#ah'+tag)}</g>{cv}<g class="hd">{o['heads']}</g>{extra}</g>{fr}
<line class="ax" x1="{X_(-w):.1f}" y1="{CY}" x2="{X_(w):.1f}" y2="{CY}"/><line class="ax" x1="{CX}" y1="{Y_(-w):.1f}" x2="{CX}" y2="{Y_(w):.1f}"/>
<circle class="dot" cx="{CX}" cy="{CY}" r="4.5"/>
<text class="s" x="{X_(w):.1f}" y="{Y_(-w)+20:.1f}" text-anchor="end">horizontal axis: shear (x) →</text><text class="s" transform="translate(30 {CY}) rotate(-90)" text-anchor="middle">vertical axis: stretch (y) →</text>
<text class="m" x="180" y="390" text-anchor="middle">{sub}</text></svg>'''
    return svg
# separatrix overlays at i: stable = imaginary axis, unstable = unit circle arc
arc=[(dx,math.sqrt(1-dx*dx)-1) for dx in np.linspace(-w*1.1,w*1.1,60)]
sep=f'<line class="sp-s" x1="{CX}" y1="{Y_(-w*1.1):.1f}" x2="{CX}" y2="{Y_(w*1.1):.1f}"/><path class="sp-u" d="{path(arc)}"/>'
lab_i=f'<text class="lb" x="{CX+8}" y="{Y_(w)+34:.1f}" fill="var(--ok)">stable manifold</text><text class="lb" x="{CX+8}" y="{Y_(w)+50:.1f}" fill="var(--ok)">(imaginary axis)</text><text class="lb" x="{X_(w)-6:.1f}" y="{CY+36}" text-anchor="end" fill="var(--bad)">unstable manifold</text><text class="lb" x="{X_(w)-6:.1f}" y="{CY+52}" text-anchor="end" fill="var(--bad)">(unit circle)</text>'
A=panel('i','At i (square lattice): saddle','DX(i) = diag(+3.43, −15.48)','Vector field of minus the hyperbolic gradient of the Epstein sum at s=2 near the square lattice, with contours, integral curves and the two separatrices','' ,'A')
A=A.replace('</g>{fr}','</g>',1) if False else A
A=A.replace('<g class="hd">','<g class="sep">'+sep+'</g><g class="hd">',1)
A=A.replace('<text class="m"',lab_i+'<text class="m"',1)
B=panel('rho','At ρ (triangular lattice): minimum','DX(ρ) = −E(ρ,2)·I ≈ −5.78·I','Vector field of minus the hyperbolic gradient of the Epstein sum at s=2 near the triangular lattice, with contours and integral curves converging to the minimum','','B')
css='''<style>
.qm svg{width:100%;height:auto;display:block;background:var(--card);border:1px solid var(--line);border-radius:6px}
.qm .t{font:600 15px system-ui,sans-serif;fill:var(--fg)} .qm .s{font:13.5px system-ui,sans-serif;fill:var(--mut)} .qm .m{font:13px ui-monospace,Menlo,monospace;fill:var(--fg)} .qm .lb{font:600 12.5px system-ui,sans-serif;paint-order:stroke;stroke:var(--card);stroke-width:4px;stroke-linejoin:round}
.qm .lo{fill:none;stroke:var(--acc);stroke-width:1.8} .qm .hi{fill:none;stroke:var(--acc2);stroke-width:1.8} .qm .z{fill:none;stroke:var(--mut);stroke-width:2.2;stroke-dasharray:7 5}
.qm .ic{fill:none;stroke:var(--fg);stroke-width:1.6;opacity:.9} .qm .hd polygon{fill:var(--fg)}
.qm .sp-s{stroke:var(--ok);stroke-width:4;opacity:.85} .qm .sp-u{fill:none;stroke:var(--bad);stroke-width:4;opacity:.85}
.qm .ax{stroke:var(--mut);stroke-width:1;fill:none} .qm .fld line{stroke:var(--mut);stroke-width:1.4;opacity:.8} .qm marker path{fill:var(--mut)} .qm .dot{fill:var(--fg)}
</style>'''
fig=f'''{css}
<figure class="box qm" id="fig-local-models" style="margin:14px 0">
<div class="cols">{A}{B}</div>
<figcaption class="sub" style="margin-top:8px"><b style="color:var(--fg)">Local vector fields at s = 2.</b> Near the square lattice, the Epstein sum decreases along shear and increases along stretch. Near the triangular lattice, it increases in every local direction. Arrows are sampled from the field $X(z)=-\\nabla_{{\\mathrm{{hyp}}}}E(z,2)=-y^2(E_x\\,\\partial_x+E_y\\,\\partial_y)$, computed from the full lattice sum (not a quadratic model). Thin grey arrows: the field on a grid, <i>normalized to equal length for readability, so lengths are schematic and only directions come from the field</i>. Black curves: integral curves of $X$ (forward in time, arrowheads show the direction). Blue/orange: contours of $E-E(\\text{{centre}})$ below/above the centre value; dashed grey: the level through the saddle. Green and red at $i$: the two separatrices.</figcaption></figure>
<div class="box lab" id="fig-local-text">
<p><b>Why the arrows point downhill.</b> Along any trajectory of $\\dot z = X(z)$, $\;dE/dt = dE(X) = -y^2(E_x^2+E_y^2) = -\\|\\nabla_{{\\mathrm{{hyp}}}}E\\|^2\\le 0$, with equality only at critical points. So every integral curve crosses every contour from higher to lower value. <span class="tag">NUMERICAL</span> check: on one integrated trajectory at each centre, a finite-difference $dE/dt$ matched $-y^2|\\nabla E|^2$ to relative error {checks['i']:.1e} (at $i$) and {checks['rho']:.1e} (at $\\rho$).</p>
<p><b>At the square lattice $i$.</b> The Euclidean Hessian is $\\mathrm{{diag}}(E_{{xx}},E_{{yy}})=\\mathrm{{diag}}(-3.4268,\\,15.4804)$ (reference table), and $y=1$ at $i$, so the linearization of $X$ is $-\\mathrm{{diag}}(E_{{xx}},E_{{yy}})=\\mathrm{{diag}}(+3.43,\\,-15.48)$: <b>unstable along shear</b> ($x$), <b>stable along stretch</b> ($y$). The two separatrices are exact, not numerical: $E$ is invariant under the reflection $z\\mapsto-\\bar z$ and under $z\\mapsto-1/z$, hence under $z\\mapsto 1/\\bar z$; these are hyperbolic isometries, and the fixed set of an isometry that preserves $E$ is invariant under the gradient flow. The fixed set of $z\\mapsto-\\bar z$ near $i$ is the imaginary axis (the stable manifold) and that of $z\\mapsto1/\\bar z$ is the unit circle (the unstable manifold). <span class="tag">NUMERICAL</span> confirmation: a trajectory started on the unstable direction stayed within {checks['unit_circle_dev']:.1e} of $|z|=1$, and one started on the axis stayed within {checks['axis_dev']:.1e} of $x=0$.</p>
<p><b>At the triangular lattice $\\rho$.</b> The stabilizer of $\\rho$ contains a rotation of order 3, which acts on the tangent plane as a $120^\\circ$ rotation; a symmetric $2\\times2$ form invariant under it is a multiple of the identity, so the linearization is <b>isotropic</b>: $DX(\\rho)=-y^2\\,\\mathrm{{Hess}}\\,E=-\\tfrac34(7.711)\\,I\\approx-5.783\\,I$. (This equals $-E(\\rho,2)$: for the eigenfunction $E$ with eigenvalue $s(s-1)=2$ and an isotropic Hessian, $y^2E_{{xx}}=y^2E_{{yy}}=E$.) The quadratic model therefore gives purely radial descent, and the integral curves converge to $\\rho$ from every direction.</p>
<p class="sub">Scope: the neighbourhoods drawn are $|\\delta x|,|\\delta y|\\le0.3$; nothing here is a global statement about the flow on the fundamental domain. Gradients are from the truncated lattice sum (cutoff $|m+nz|\\le80$) and the curves are numerical integrals (RK4 on an interpolated grid).</p></div>'''
open('/tmp/fig2.html','w',encoding='utf-8').write(fig)
print(len(fig))
