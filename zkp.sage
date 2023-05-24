import hashlib

def proofZkp01(x,r,b):
    
    eb=encMyalea(0,w)
    sig1minb=randrange(1, ordQ, 1)
    rp1minb=randrange(1, ordQ, 1)
    e1minb=R(multChifre(encMyalea(0,rp1minb),powerChifre(divChifre(x,encrypt(1-b)),-(sig1minb))))
    d=str(x)+str(eb)+str(e1minb)
    d=hashlib.sha256(d.encode('utf-8')).hexdigest()
    sigb=d-sig1minb
    rob=R(w+r*sigb)
    if(1-b==0):return (e1minb,eb,sig1minb,rp1minb,sigb,rob)
    else : return(eb,e1minb,sigb,rob,sig1minb,rp1minb)


def verifZkp01(x,proof):
    d=str(x)+str(proof[0])+str(proof[1])
    d=hashlib.sha256(d.encode('utf-8')).hexdigest()
    test1= proof(2)+proof(4)
    test2=R(multChifre(encMyalea(0,proof(6)),powerChifre(divChifre(x,encrypt(1)),-(proof(4)))))
    test3=R(multChifre(encMyalea(0,proof(3)),powerChifre(divChifre(x,encrypt(1)),-(proof(2)))))
    if (test1==d and test2==proof(1) and test3==proof(0)) : return True 
    else :return False


        
    