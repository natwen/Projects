import multiprocessing as mp
import time, sys, random

#Controle de l'affichage
CLEARSCR="\x1B[2J\x1B[;H" 

def effacer_ecran() : 
    print(CLEARSCR,end='')

#Définitions des 3 processus et de leurs actions

def client(liste_alphabet, liste_client, q_in):
    while True:
        time.sleep(2) #Envoie d'une commande aléatoire toutes les 5 secondes
        commande = random.choice(liste_alphabet)
        identifiant = random.choice(liste_client)
        expression = commande + ',' + identifiant #Envoie une commande + le nom d'un client
        q_in.put(expression)

def serveur(q_in, q_out, id_serveur):
    while True:
        [commande,identifiant] = q_in.get().split(',') #Reçoit ce que le client a envoyé
        temps = random.randint(1,5) #Prépare la commande en un temps random
        time.sleep(temps)
        expression = commande +',' + identifiant +',' + str(temps) + ',' + str(id_serveur) #Envoie la commande, le nom du client,le temps pour la préparer et le serveur qui s'en occupe au major d'homme
        q_out.put(expression)

def affichage(q_out):
    while True:
        #C'est lui qui va lire q_out et afficher les valeurs dedans 
        [commande, identifiant, temps, id_serveur] = q_out.get().split(',') #Reçoie ce qui a été envoyé par le serveur
        print("Commande : ", commande)
        print("Client :", identifiant)
        print("Temps de service : ", temps)
        print("Réalisé par le serveur : ", id_serveur)
        effacer_ecran()


if __name__ == "__main__":
    
    liste_alphabet = [chr(i) for i in range(ord('A'),ord('Z')+1)] #Alphabet pour la commande
    liste_client = ["Catherine", "Nicolas", "Bertrand", "Hugo", "Annie", "Mathis", "Florence", "Cassandra", "Paul", "Gérard", "Victor"] #Ensemble de noms pour définir les clients

    q_in = mp.Queue()
    q_out = mp.Queue()

    s = int(sys.argv[1])

    #Trois processus majeurs

    serveurs = [mp.Process(target = serveur, args = (q_in,q_out,x,)) for x in range(s)]    
    clients = mp.Process(target = client, args = (liste_alphabet,liste_client,q_in,))
    major_dHomme = mp.Process(target = affichage, args =(q_out,))

    for i in range(s):
        serveurs[i].start()

    clients.start()
    major_dHomme.start()

    for i in range(s):
        serveurs[i].join()
    clients.join()
    major_dHomme.join()