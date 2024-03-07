import multiprocessing as mp
import time, random
import ctypes
CLEARSCR="\x1B[2J\x1B[;H" 

def effacer_ecran() : 
    print(CLEARSCR,end='')


def temperature(T): #Fonction qui lit la valeur du thermocouple et les envoie au chauffage
    while True:
        time.sleep(10) #La température change naturellement toutes les 5 secondes
        T = 21 + 2*random.random()
        temp.value = T


def pression(P): #Fonction qui lit la valeur de la pression et les envoie à l'écran
    while True:
        time.sleep(10)
        P = random.randint(980, 1020)
        press.value = P

def pompe(seuil_P): #Fonction qui rétablie une bonne valeur de pression
    dfw_pompe.close()
    while True:
        
        go_pomper = dfr_pompe.recv()
        pompeur = int.from_bytes(go_pomper,'big')
        P = press.value
        if pompeur:
            P = P-0.5*(P-seuil_P)
        press.value = P
        


def ecran(): #Affiche les valeurs pression/température et les consignes à respecter
    while True:
        time.sleep(2) 
        T = temp.value
        P = press.value
        
        print("Température désirée : ", 22, "°C")
        print("Pression désirée : ", 1000, "Pa")
        print()
        print("Température: %.2f"% T, "°C")
        print("Pression: %.1f"% P, "Pa")

        effacer_ecran()
  

def chauffage(seuil_T): #Met en route le chauffage ou l'arrete
    dfw_chauffage.close()

    while True:
        go_chauffer = dfr_chauffage.recv()
        chauffeur = int.from_bytes(go_chauffer,'big')
        T = temp.value
        if chauffeur:
            T = T- 0.5*(T-seuil_T) #Rétablie une bonne valeur de température
        temp.value = T

    

def controleur(seuil_P, seuil_T):
    dfr_chauffage.close()
    dfr_pompe.close()
    while True:
        time.sleep(2)
        T = round(temp.value,2)
        P = round(press.value,2)

        if T > seuil_T:
            go_chauffer = 0
            if P > seuil_P:
                go_pomper = 1
            else:
                go_pomper = 0
        elif T < seuil_T:
            
            go_chauffer = 1
            if P > seuil_P:
                go_pomper = 1
            else:
                go_pomper = 0
        else:
            go_chauffer = 0
            if P > seuil_P:
                go_pomper = 1
            else: 
                go_pomper = 0


        dfw_chauffage.send(go_chauffer.to_bytes(4,'big'))
        dfw_pompe.send(go_pomper.to_bytes(4,'big'))

#3 process : pression température et écran
if __name__ == '__main__':
    go_chauffage = mp.Value('i', False)
    go_pompe = mp.Value(ctypes.c_bool, False)
    seuil_T = 22.0
    seuil_P = 1000
    temp= mp.Value('f',22.0)
    press = mp.Value('f',1000.0)

    (dfr_chauffage, dfw_chauffage) = mp.Pipe()
    (dfr_pompe, dfw_pompe) = mp.Pipe()

    Pression = mp.Process(target = pression, args=(press,))
    Temperature = mp.Process(target = temperature, args=(temp,))
    Ecran = mp.Process(target = ecran, args=())
    Chauffage = mp.Process(target = chauffage, args = (seuil_T,))
    Pompe = mp.Process(target = pompe, args = (seuil_P,))
    Controleur = mp.Process(target = controleur, args = (seuil_P, seuil_T,))

    Pression.start()
    Temperature.start()
    Ecran.start()
    Chauffage.start()
    Pompe.start()
    Controleur.start()

    Pression.join()
    Temperature.join()
    Ecran.join()
    Chauffage.join()
    Pompe.join()
    Controleur.join()

