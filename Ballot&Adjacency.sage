load("MPC_arithmetic.sage")
load("zkp.sage")
def classer_candidats(nb_candidats):
    
    tot=factorial(nb_candidats)
    s=randrange(0,tot-1,1)
    a=CyclicPermutations(range(nb_candidats+1)).list()
    candidats=a[s][1:] 
    print(candidats)
   
    
    # Créer la matrice de préférences avec des chiffrés de 0
    matrice = [[bitwise(0)] * nb_candidats for _ in range(nb_candidats)]
    
    # Remplir et chiffrer la matrice selon les préférences déduites du classement
    for i in range(nb_candidats):
        for j in range(i+1, nb_candidats):
                x=bitwise(1)
                p1=proofZkp01(candidats[i][j][0],r,0)
                if(not(verifZkp01(candidats[i][j][0]),p1)) : print("non valide")
                matrice[candidats[i]-1][candidats[j]-1] = x #bitwise encryption of 1
                p=proofZkp01(bitwise[0],r,1)
                if(not(verifZkp01(bitwise[0],p))): print("non valide")
                E1=bitwise(1)
                matrice[candidats[j]-1][candidats[i]-1] = Neg(E1) #bitwise encryption of  0              
    

    return matrice


def classer_candidatsAll(nb_candidats,nb_voters):
    matALL=[]
    for i in range(nb_voters):
        matALL.append(classer_candidats(nb_candidats))
     
    return matALL

def matAdja(matALL):
    matrice_sortie= matrice_sortie = [[0] * len(matALL[0][0]) for _ in range(len(matALL[0]))]

    for matrice in matALL:
        for i in range(len(matrice)):
            for j in range(len(matrice[0])):
                Addbits( matrice_sortie[i][j] , matrice[i][j])

    return matrice_sortie
 

