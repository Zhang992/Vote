def AddBits(x,y):
    x0=x[0]
    y0=y[0]
    R=CSZ(x0,y0)
    z=[]
    z[0]=x0*y0/(R*R)
    for i in range(1,len(x)-1):
        xi=x[i]
        yi=y[i]
        A=xi*yi/(CSZ(xi,yi)**2)
        z[i]=A*R/(CSZ(A,R)**2)
        R=(xi*yi*R/z[i])**(1/2)
    return z

def SubLTBits(x,y):
    x0=x[0]
    y0=y[0]
    A=CSZ(x0,y0)
    z=[]
    z[0]=x0*y0/(A*A)
    R=y0/A
    for k in range(1, len(x)-1):
        xk=x[k]
        yk=y[k]
        A=CSZ(yk,R)
        B=yk*R/(A*A)
        C=CSZ(xk,B)
        z[k]=xk*B/(C*C)
        R=yk*R/(A*C)
    return (z,R)
