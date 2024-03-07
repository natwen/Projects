import multiprocessing as mp
import sys, time,random

#les deux processus majeurs et leurs actions

def calculateur(q1,qr):
    while True:
        nombre_operateur = 0
        indice_operateur = 0
        [expression,id] = q1.get().split(',') #réception de la demande avec l'identifiant du demandeur
        id = int(id)
        for i in range(len(expression)):
            if expression[i] == '+' or expression[i] == '-' or expression[i] == '*' or expression[i] == '/' :  #Compte le nombre d'opérateurs dans la demande
                nombre_operateur += 1
                indice_operateur = i
        if nombre_operateur !=1 or indice_operateur == 0 or indice_operateur == len(expression)-1: #S'il n'y a pas le bon nombre d'opérateurs dans la demande, alors elle est considérée comme fausse
            qr[id].put("Opération non valide")
        else: #La demande est considérée comme valide 
            nombre1 = int(expression[:indice_operateur])
            nombre2 = int(expression[indice_operateur+1:])
            operateur = expression[indice_operateur]          
            if operateur == '+': #On calcule en fonction de l'opérateur qui a été donné dans l'expression
                qr[id].put(nombre1 + nombre2)
            if operateur == '-':
                qr[id].put(nombre1 - nombre2)
            if operateur == '*':
                qr[id].put(nombre1 * nombre2)
            if operateur == '/':
                qr[id].put(nombre1 / nombre2)

def demandeur(q1,qr,id):
    while True : 
        operateurs = ["+",'-','*','/'] #Choix entre différents opérateurs
        nombre1 = random.randint(1,100)
        nombre2 = random.randint(1,100)
        operation = operateurs[random.randint(0,3)]
        expression = ""
        if random.random() < 0.01: #Le système écrit une expression fausse pour une probabilité de 1%
            operation2 = operateurs[random.randint(0,3)]
            expression = operation2 + str(nombre1) + operation +str(nombre2)
        elif random.random() < 0.01:#Le système écrit une expression fausse pour une probabilité de 1%
            operation2 = operateurs[random.randint(0,3)]
            expression = str(nombre1) + operation +str(nombre2) + operation2
        elif random.random() < 0.01:#Le système écrit une expression fausse pour une probabilité de 1%
            expression = operation+ str(nombre1) +str(nombre2)  
        elif random.random() < 0.01:#Le système écrit une expression fausse pour une probabilité de 1%
            expression = str(nombre1) +str(nombre2) + operation
        else: #le système écrit correctement l'expression
            expression = str(nombre1) + operation + str(nombre2)
        expression_modifie = expression + "," + str(id) #Ajoute l'identifiant du demandeur pour que le calculateur lui réponde à lui
        q1.put(expression_modifie) 
        print('opération à faire :', expression ,' donné par le demandeur',id)
        resultat = qr[id].get()
        print(expression," = ",resultat,' reçu par le demandeur',id) 
        time.sleep(random.randint(1,5))   

        


if __name__ == '__main__':
    q1 = mp.Queue()
    q2 = mp.Queue()
    n = int(sys.argv[2])
    m = int(sys.argv[1])
    qr = [mp.Queue() for i in range(m)]
    demandeurs = [mp.Process(target=demandeur,args=(q1,qr,i,)) for i in range(m)] #i permet de donner un identifiant aux demandeurs
    calculateurs = [mp.Process(target = calculateur, args=(q1,qr,)) for i in range(n)]

    for c in calculateurs:
        c.start()

    for d in demandeurs:
        d.start()

    for c in calculateurs:
        c.join()

    for d in demandeurs:
        d.join()


    sys.exit(0)