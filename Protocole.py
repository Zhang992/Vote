import hashlib
import random
from testr import diviser_aleatoirement

depouilleur=[]
nbrDep=2
publicK=0
R=None
ordQ=0
nombreCand=4

class PrivateKey(object):
	def __init__(self, p=None, g=None, x=None):
		self.p = p
		self.g = g
		self.x = x
		

class PublicKey(object):
	def __init__(self, p=None, g=None, h=None,t=None):
		self.p = p
		self.g = g
		self.h = h
		self.tailleB=t
		




def generateKey(tailleBit):
	global R
	global depouilleur
	global ordQ
	p=random_prime(2^(tailleBit)-1,false,2^(tailleBit-1))
	R=IntegerModRing(p)

	 
	f=list(factor(p-1))
	q=f[len(f)-1][0]
	print(" q "+str(q))
	ordQ=q
	g1=R.unit_gens()[0]
	print("p "+str(p))
	
	g=R(pow(g1,(p-1)/q))

	x = randrange(1, q, 1)
 
	 
	depouilleur=diviser_aleatoirement(int(x),nbrDep)
	 
	h = R(g^x)
	publicKey = PublicKey(p, g, h,tailleBit)
	privateKey = PrivateKey(p, g, x)
	
	global publicK

	#print(depouilleur) 
	#print("x "+str(x))
	publicK=publicKey
	return (publicK,privateKey)


def multChifre(chif1,chif2):
	global publicK
	return(R(chif1[0]*chif2[0]),R(chif1[1]*chif2[1]) )
def powerChifre(chif,s):
	global publicK
	return(R(chif[0]^s),R(chif[1]^s))
def reEnc(cipher,newR ):
	global publicK
	return (R(cipher[0]*R(publicK.h^newR)),R(cipher[1]*R(publicK.g^newR)))
def divChifre(c1,c2):
	global publicK
	return (R(c1[0]/c2[0]),R(c1[1]/c2[1]))



def encrypt( message) :
	global publicK
	global ordQ
	r = randrange(1, ordQ, 1)
				#c = g**r mod p
	c2 = R( publicK.g^r)
	c1=(R(publicK.g^message)*R(publicK.h^r))
	return (R(c1),c2)

def bitwise(message):
	global publicK
	bitend=[encrypt(message)]
	for i in range(log(nombreCand,2)):
		bitend.append(encrypt(0))
	
	return bitend

def decrypt(chiffre):
	global publicK
	sum=1
	global depouilleur
	global nbrDep
	sum2=0
	
	
	for i in range(nbrDep):
		sum2=sum2+depouilleur[i]
		sum=sum*(R(chiffre[1]^depouilleur[i]))

	messG=R(chiffre[0] /sum) 
	
	test=publicK.p
	#print("ouais")
	for i in range (test):
		 
		if(messG==R(publicK.g^i) ):
			return i 

def decbitwise(tab):
	res=[]
	for i in range (len(tab)):
		res.append(decrypt(tab[i]))

	rev = list(reversed(res))
	print(rev)


def decryptCgate(chiffre,publicK):
	sum=1
	global depouilleur
	global nbrDep
	sum2=0
	
	
	for i in range(nbrDep):
		sum2=sum2+depouilleur[i]
		sum=sum*(R(chiffre[1]^depouilleur[i]))

	messG=R(chiffre[0] /sum) 
	minus=(-1)%ordQ
	if(messG==R(publicK.g^minus)) : return minus
	else :return 1

def encMyalea(message,r):
	global publicK
	 
	c2 = R( publicK.g^r)
	c1=(R(publicK.g^message)*R(publicK.h^r))
	return (R(c1),c2)

def ZkCgate(xi,xi1,yi,yi1,s,r1,r2):
	alpha = randrange(1, q, 1)
	beta=  randrange(1, q, 1)
	esx=encMyalea(0,alpha)
	esy=encMyalea(0,beta)
	sigmamins=randrange(1, q, 1)
	rominsX=randrange(1, q, 1)
	rominsY=randrange(1, q, 1)
	eminsX=multChifre(encMyalea(0,rominsX),powerChifre(multChifre(xi,powerChifre(xi1,s%ordQ)),(-sigmamins)%ordQ))
	eminsY=multChifre(encMyalea(0,rominsY),powerChifre(multChifre(yi,powerChifre(yi1,s%ordQ)),(-sigmamins)%ordQ))
	d=str(publicK.g)+str(publicK.h)+str(xi1)+str(yi1)+str(xi)+str(yi)+str()
	return 0




def cGate(x,y):
	global publicK
	global nbrDep
	global ordQ

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
	
	#res2=decrypt(ml,publicK)
	#print(res2)
	inv2 = pow(2,ordQ-2,ordQ)

	
	resf=powerChifre(ml,inv2)
	#print("CGate" +str(decrypt(resf)))
	return resf

def Addbits(x,y):
	Z=[]
	global ordQ
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

def FloydWarshall(P):
	n = len(P)
	S = copy(P)
	A = zero_matrix(n)
	B = zero_matrix(n)
	for k in range(n):
		for i in range(n):	
			for j in range(n):
				if i != j:
					t,comp=SubLt(S[i][k],S[k][j])
					A[i,j] = selectWise(S[k][j],S[i][k],comp)
					t,comp=SubLt(S[i][j],A[i][j])
					B[i,j] = selectWise(S[i][j],A[i][j],comp)
		for i in range(n):
			for j in range(n):
				if i != j:
					S[i][j] = B[i][j]
	return S








pb,ps=generateKey(50)
message=40
x1=encrypt( message)

y=encrypt( 1)
#cGate(x,y)
t=bitwise(0)
t2=bitwise(1)
 
decbitwise(t)
add,r=SubLt(t,t2)
decbitwise(add)
add2=Neg(t2)
decbitwise(add2)
add3=Addbits(add2,t2)
decbitwise(add3)
#print(str(y)+str(y))
#d=hashlib.sha256(b"Nobody inspects the spammish repetition").hexdigest()
#print(d)

#x=encrypt(message)
#r=-5
#print(powerChifre(x,r%ordQ))

#xmin=powerChifre(x,(-1)%ordQ) 
#print(powerChifre(xmin,5))


#print(c)
#print(decrypt(res[0]))
#print(decrypt(xxp,publicK))
#print(publicK.tailleB)
#print(hashlib.sha256(b"Nobody inspects the spammish repetition").hexdigest())
