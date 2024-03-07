import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import multiprocessing as mp


def Game_of_life(Population,Population_suivante,id,qe1,qr1,qe2,qr2):
    L=[]
    cpt = 0
    while cpt != 500:
        for i in range(len(Population)):
            for j in range(len(Population[0])):

                nbr_vivant = 0
                if id == 1:
                    if i == 0 :
                        Liste_12 = qr1.get.list()
                        if j == 0 :
                            nbr_vivant = Population[i+1][j+1] + Population[i][j+1] + Population[i+1][j] 
                        elif j == len(Population[0]) - 1 :
                            nbr_vivant = Population[i+1][j-1] + Population[i][j-1] + Population[i+1][j]                     
                        else : 
                            nbr_vivant = Population[i][j-1] + Population[i+1][j-1] + Population[i+1][j] + Population[i+1][j+1] + Population[i][j+1]
                    elif i == len(Population) - 1 :
                        if j ==0 :
                            nbr_vivant = Population[i-1][j] + Population[i-1][j+1] + Population[i][j+1]
                        elif j == len(Population[0]) - 1:
                            nbr_vivant = Population[i][j-1] + Population[i-1][j-1] + Population[i-1][j]
                        else : 
                            nbr_vivant = Population[i][j-1] + Population[i-1][j-1] + Population[i-1][j] + Population[i-1][j+1] + Population[i][j+1]
                    else :
                        if j == 0 :
                            nbr_vivant = Population[i-1][j] + Population[i-1][j+1] + Population[i][j+1] + Population[i+1][j+1] + Population[i+1][j] 
                        elif j == len(Population[0]) - 1 :
                            nbr_vivant = Population[i-1][j] + Population[i-1][j-1] + Population[i][j-1] + Population[i+1][j-1] + Population[i+1][j]
                        else : 
                            nbr_vivant = Population[i+1][j] + Population[i+1][j-1] + Population[i][j-1] + Population[i-1][j-1] + Population[i-1][j] + Population[i-1][j+1] + Population[i][j+1] + Population[i+1][j+1]

                    if Population[i][j]: 
                        if nbr_vivant < 2 : 
                            Population_suivante[i][j] = 0
                        elif nbr_vivant == 2 or nbr_vivant == 3 :
                            Population_suivante[i][j] = 1
                        else :
                            Population_suivante[i][j] = 0
                    else : 
                        if nbr_vivant == 3:
                            Population_suivante[i][j] = 1
                        else : 
                            Population_suivante[i][j] = 0
        Population = np.copy(Population_suivante)
        L.append(Population)
        Population_suivante = np.zeros((30,30),'i')
        print(Population,type(Population))
        cpt += 1 
    return L



def generateur_matrices(Frame=0):
        return liste_matrice[Frame]


def maj(Frame):
    mat.set_data(generateur_matrices(Frame))
    return

if __name__ == '__main__':
    taille = 30
    Population = np.random.randint(2, size=(taille,taille))
    Population_suivante = np.zeros((taille,taille),'i')
    print(Population,type(Population))
    liste_matrice = Game_of_life(Population,Population_suivante)
    generateur_matrices(0)
    q12 = mp.Queue()
    q13 = mp.Queue()
    q34 = mp.Queue()
    q24 = mp.Queue()
    q21 = mp.Queue()
    q31 = mp.Queue()
    q43 = mp.Queue()
    q42 = mp.Queue()
    process1 = mp.Process(target=Game_of_life,args=(Population[:int(taille/2)][:int(taille/2)],Population_suivante[:int(taille/2)][:int(taille/2)],1,q12,q21,q13,q31,))
    process2 = mp.Process(target=Game_of_life,args=(Population[:int(taille/2)][int(taille/2)+1:],Population_suivante[:int(taille/2)][int(taille/2)+1:],2,q21,q12,q24,q42,))
    process3 = mp.Process(target=Game_of_life,args=(Population[int(taille/2)+1:][:int(taille/2)],Population_suivante[int(taille/2)+1:][:int(taille/2)],3,q31,q13,q34,q43,))
    process4 = mp.Process(target=Game_of_life,args=(Population[int(taille/2)+1:][int(taille/2)+1:],Population_suivante[int(taille/2)+1:][int(taille/2)+1:],4,q42,q24,q43,q34,))
    process = [process1,process2,process3,process4]
    for p in process:
        p.start()
    for p in process:
        p.join()

    fig, ax = plt.subplots()
    mat = ax.matshow(generateur_matrices())
    plt.style.use('seaborn-pastel')
    anim = ani.FuncAnimation(fig, maj, interval=100, frames=len(liste_matrice))
    plt.show()