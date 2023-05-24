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


generateKey(1000)