load("zkp.sage")


def cGate(x,y):
	

	eminus=encrypt( (-1)%ordQ)
	yy=multChifre(y,y)
	y0=multChifre(eminus,yy)
	res=decryptCgate(y0,publicK)
	#print("y0 "+str(res))
	x0=x
	for i in range (nbrDep):
		s=randrange(0,1,1)
		r1=randrange(1, ordQ, 1)
		r2=randrange(1, ordQ, 1)
		if(s==0):
			s=-1%ordQ
		else :
			s=1

		x0=powerChifre(x0,s)
		y0=powerChifre(y0,s)
		x0=reEnc(x0,r1 )
		y0=reEnc(y0,r2)
	
	
	res=decryptCgate(y0,publicK)
	
	
	pw=powerChifre(x0,res)
	ml=multChifre(x,pw)
	
	
	inv2 = pow(2,ordQ-2,ordQ)

	
	resf=powerChifre(ml,inv2)

	return resf

def Addbits(x,y):
	Z=[]
	
	r=cGate(x[0],y[0])
	xoyo=multChifre(x[0],y[0])
	r2=powerChifre(r ,2)
	z0=divChifre(xoyo,r2)
	Z.append(z0)
	for i in range(1,len(x)):
		xi=x[i]
		yi=y[i]
		xiyi=multChifre(xi,yi)
		cgxiyi=cGate(xi,yi)
		cg2=powerChifre(cgxiyi,2)
		A=divChifre(xiyi,cg2)
		cgar=cGate(A,r)
		zi=divChifre(multChifre(A,r),powerChifre(cgar,2))
		Z.append(zi)
		rentre1=multChifre(xiyi,r)
		rentre2=divChifre(rentre1,zi)
		inv2 = pow(2,ordQ-2,ordQ)
		r=powerChifre(rentre2,inv2)




	return Z


def SubLt(x,y):
	Z=[]
	A=cGate(x[0],y[0])
	z0=divChifre(multChifre(x[0],y[0]),powerChifre(A,2))
	r=divChifre(y[0],A)
	Z.append(z0)

	for i in range(1,len(x)):
		xi=x[i]
		yi=y[i]
		A=cGate(yi,r)
		B=divChifre(multChifre(yi,r),powerChifre(A,2))
		C=cGate(xi,B)
		zi=divChifre(multChifre(xi,B),powerChifre(C,2))
		r=divChifre(multChifre(yi,r),multChifre(A,C))
		Z.append(zi)


	return Z,r

def Not(x):
	e=encrypt(1)
	return divChifre(e,x)



def Neg(x):
	Z=[]
	Z.append(x[0])
	ri1=Not(x[0])
	for i in range (1,len (x)) :
		xi=x[i]
		ri=cGate(Not(xi),ri1)
		zi=divChifre(multChifre(Not(xi),ri1),powerChifre(ri,2))
		Z.append(zi)
		ri1=ri
	
	return Z

def Select(x,y,b):
	return multChifre(x,cGate(divChifre(y,x),b))

def selectWise(x,y,b):
	Z=[]
	for i in range (len(x)):
		Z.append(Select(x[i],y[i],b))
	return Z
