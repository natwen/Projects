import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as ani

n = 60
direction = [-1, 0]

mat= np.zeros((n,n))
liste_matrice=[]
def non_priorite(x):
    if(x==1):
        return 0
    elif(x==0):
        return 1
    return priorite
def bonne_direction(list):
    if list[0] != 0 :
        return 0
    return 1

def continue_sans_rien_faire():
    mat[coordonnees[0]][coordonnees[1]] = 0
    coordonnees[bonne_direction(direction)] += direction[bonne_direction(direction)]
    mat[coordonnees[0]][coordonnees[1]] = 1
    liste_matrice.append(np.reshape(np.copy(mat),(len(mat[0]),len(mat))))
    return

def dessine_mur(r1, r2, mat): #r1 et r2 sont des coordonnÃ©es dans la matrice
    for lignes in range(r1[0], r2[0]):
        for colonnes in range(r1[1], r2[1]):
            mat[lignes][colonnes] = 2

def mettre_direction(x, direction,bonne_direction):
    if(x==0 and bonne_direction==0):
       return  [0,1]
    if(x==1 and bonne_direction==0):
       return  [0,-1]
    if(x== 2 and bonne_direction ==0) :
       print([-direction[0],0])
       print("1")
       return [-direction[0],0]
    if(x==1 and bonne_direction==1):
       return  [1,0]
    if(x==0 and bonne_direction==1):
       return  [-1,0]
    if(x==2 and bonne_direction ==1) :
       print([0,-direction[1]])
       print("2")
       return [0,-direction[1]]

for colonnes in range(n):
    mat[0][colonnes]=2
    mat[1][colonnes]=2
    mat[n-1][colonnes]=2
    mat[n-2][colonnes]=2
for lignes in range(n):
    mat[lignes][0]=2
    mat[lignes][1]=2
    mat[lignes][n-1] = 2
    mat[lignes][n-2] = 2
mat[25][25] = 1 #Position initiale de la voiture
mat[2][2] = 3 # Sortie du labyrinthe

dessine_mur([2,10], [12, 20], mat)
dessine_mur([n-8, n-15],[n-3, n-13], mat)

priorite=0 # 1 = droite, -1 = gauche, 0 centre

coordonnees = [50, 50] #coordonnÃ©es de la position initiale de la voiture



possibilites = []

print(mat)
for i in range(600):
    print(possibilites)
    # print(priorite)
    print(direction)
    possibilites = []

    if bonne_direction(direction) == 0:
        if mat[coordonnees[0]+2*direction[bonne_direction(direction)]][coordonnees[1]] != 2: #Si on veut tester les coordonnÃ©es pour une direction montante ou descendante
            continue_sans_rien_faire()
        else: #Si les coordonnÃ©es montantes/descendantes sont Ã©gales Ã  2, on change les Ã©lÃ©ments de direction
            if mat[coordonnees[0]][coordonnees[1]+1] != 2 and mat[coordonnees[0]][coordonnees[1]+2] != 2:
                possibilites.append(0) #on rajoute la possibilitÃ© d'aller Ã  droite
            if mat[coordonnees[0]][coordonnees[1]-1] != 2 and mat[coordonnees[0]][coordonnees[1]-2] != 2:
                possibilites.append(1) #on rajoute la possibilitÃ© d'aller Ã  gauche
            elif (len(possibilites) ==0 ):
                possibilites.append(2) #on rajoute la possibilitÃ© de faire demi-tour
                #direction = [-direction[0], 0]

            if(len(possibilites)==1):
                if(direction[bonne_direction(direction)]==-1):
                    priorite = non_priorite(possibilites[0])
                direction=mettre_direction(possibilites[0],direction,bonne_direction(direction))

            else:
                if(direction[bonne_direction(direction)]==1):
                    direction=mettre_direction(non_priorite(priorite),direction,bonne_direction(direction))
                    priorite = non_priorite(priorite)
                elif(direction[bonne_direction(direction)]==-1):
                    direction=mettre_direction(priorite,direction,bonne_direction(direction))
                    priorite = non_priorite(priorite)
    elif bonne_direction(direction)==1:
        if mat[coordonnees[0]][coordonnees[1]+2*direction[bonne_direction(direction)]] != 2: #Si on veut tester les coordonnÃ©es pour une direction qui va Ã  gauche ou Ã  droite
            continue_sans_rien_faire()
        else: #Si les coordonnÃ©es colonnes sont Ã©gales Ã  2, on change les Ã©lÃ©ments de direction
            if mat[coordonnees[0]-1][coordonnees[1]] != 2 and mat[coordonnees[0]-2][coordonnees[1]] != 2:
                possibilites.append(0)
            if mat[coordonnees[0]+1][coordonnees[1]] != 2 and mat[coordonnees[0]+2][coordonnees[1]] != 2:
                possibilites.append(1)
            elif (len(possibilites) ==0 ):
                possibilites.append(2) #on rajoute la possibilitÃ© de faire demi-tour
                #direction = [-direction[0], 0]

            if(len(possibilites)==1):
                if(direction[bonne_direction(direction)]==-1):
                    priorite = non_priorite(possibilites[0])
                direction=mettre_direction(possibilites[0],direction,bonne_direction(direction))

            else:
                if(direction[bonne_direction(direction)]==1):
                    direction=mettre_direction(non_priorite(priorite),direction,bonne_direction(direction))
                    priorite = non_priorite(priorite)
                elif(direction[bonne_direction(direction)]==-1):
                    direction=mettre_direction(priorite,direction,bonne_direction(direction))
                    priorite = non_priorite(priorite)



#Variable direction ?

def generateur_matrices(Frame=0):
        return liste_matrice[Frame]

plt.style.use('default')
def maj(Frame):
    mat.set_data(generateur_matrices(Frame))
    return

fig, ax = plt.subplots()
mat = ax.matshow(generateur_matrices())
anim = ani.FuncAnimation(fig, maj, interval=10, frames=len(liste_matrice))
plt.show()