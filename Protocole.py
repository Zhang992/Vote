import random
import math
import sys

class PrivateKey(object):
	def __init__(self, p=None, g=None, x=None):
		self.p = p
		self.g = g
		self.x = x
		

class PublicKey(object):
	def __init__(self, p=None, g=None, h=None):
		self.p = p
		self.g = g
		self.h = h

def generator(q):
	b=False
	while(not b):
		g=random.randint(2,(q-1)//2)
		if(math.gcd(g,q)==1):
			return g


def generateKey(tailleBit):
	p=2**(tailleBit)
	g=generator(p) #generateur de z/zp
	x = random.randint( 1, p - 1 )
	h = pow( g, x, p )
	publicKey = PublicKey(p, g, h)
	privateKey = PrivateKey(p, g, x)

	return {privateKey, publicKey}


def encrypt(publicK,message) :
	
	r = random.randint( 0, publicK.p )
				#c = g**r mod p
	c1 = pow( publicK.g, r, publicK.p )
	c2=pow(publicK.g,m,publicK.p)*pow(publicK.h,r,publicK.p)
	return (c1,c2)

def encryptBinary(publicK,message):
	binar=message.bin()
	binarEnc= []
	for i in binar:
		binarEnc.append(encrypt(publicK,binar[i]))

	return binarEnc


def decrypt(publicK,chiffre): #Comment on partage le secret?

def CGate(X,Y):

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
