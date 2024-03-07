import random, time, sys, math
import multiprocessing as mp
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration):
    nbre_hit = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
    # si le point est dans l’unit circle
        if x * x + y * y <= 1: 
            nbre_hit +=1
    mutex.acquire()
    count.value += nbre_hit
    mutex.release()
# Nombre d’essai pour l’estimation
if __name__ == '__main__':
    nb_total_iteration = 1000000
    mutex = mp.Lock()
    n = int(sys.argv[1])
    count = mp.Value('i',0)
    nbre_iteration= math.floor(nb_total_iteration/n)
    temps_debut = time.time()
    process = [mp.Process(target=frequence_de_hits_pour_n_essais,args=(nbre_iteration,)) for i in range(n)]
    for p in process:
        p.start()
    for p in process:
        p.join()

    temps_fin = time.time()
    duree_exec = temps_fin - temps_debut
    print("Valeur estimée Pi par la méthode Multi−Processus : ", 4 * count.value / nb_total_iteration)
    print("le programme s'est exécuté en",duree_exec, "secondes")
#TRACE :
# Calcul Mono−Processus : Valeur estimée Pi par la méthode Mono−Processus : 3.1412604