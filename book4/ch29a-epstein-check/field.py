import numpy as np,json
R=80;s=2.0
ms=np.arange(-R-2,R+3)
def Egrad(X,Y):
    X=np.asarray(X,float);Y=np.asarray(Y,float);sh=X.shape;X=X.ravel();Y=Y.ravel()
    E=np.zeros_like(X);Ex=np.zeros_like(X);Ey=np.zeros_like(X)
    for n in range(-R-2,R+3):
        a=ms[None,:]+n*X[:,None];b=n*Y[:,None]
        q=a*a+b*b
        mask=(q<=R*R)&(q>1e-12)
        qq=np.where(mask,q,1.0)
        g=np.where(mask,Y[:,None]**s*qq**(-s),0.0)
        E+=g.sum(1)
        Ex+=(g*(-2*s*n*a/qq)).sum(1)
        Ey+=(g*(s/Y[:,None])*(a*a-b*b)/qq).sum(1)
    # tail (disc outside R): value pi*y^(s-1)R^(2-2s)/(s-1)
    E+=np.pi*Y**(s-1)*R**(2-2*s)/(s-1)
    return E.reshape(sh),Ex.reshape(sh),Ey.reshape(sh)
if __name__=='__main__':
    ref=json.load(open('book4/ch29a-epstein-check/ref.json'))['2']
    for nm,(x,y) in {'i':(0,1),'rho':(.5,np.sqrt(3)/2)}.items():
        E,ex,ey=Egrad([x],[y]);print(nm,E[0],ref[nm]['value'],ex[0],ey[0])
    h=1e-4
    for nm,(x,y) in {'i':(0,1.0),'rho':(.5,np.sqrt(3)/2)}.items():
        fxx=(Egrad([x+h],[y])[1]-Egrad([x-h],[y])[1])/(2*h);fyy=(Egrad([x],[y+h])[2]-Egrad([x],[y-h])[2])/(2*h)
        print(nm,'fxx',fxx[0],ref[nm]['fxx'],'fyy',fyy[0],ref[nm]['fyy'])
    # FD check gradient generic
    x,y=.13,1.07;E0=Egrad([x],[y])
    print('gen',(Egrad([x+h],[y])[0]-Egrad([x-h],[y])[0])/(2*h),E0[1],(Egrad([x],[y+h])[0]-Egrad([x],[y-h])[0])/(2*h),E0[2])
