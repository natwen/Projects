from tkinter import Tk, Label, Button, Frame, Canvas, messagebox, PhotoImage, StringVar
from Alien import Alien,Alien_Qui_Tire
from random import randint, random
from Ilot import Ilot
from Tir import Tir
from Vaisseau import Vaisseau

#Création de la fenêtre de jeu
jeu = Tk()
jeu.title("Space Invader")

#On prend les informations de l'écran
screen_width = jeu.winfo_screenwidth()
screen_height = jeu.winfo_screenheight()

score_height = screen_height//10
menu_width = screen_width//100

interface_jeu_width = screen_width - menu_width - 100
interface_jeu_height = screen_height - score_height

#Création des différentes Frame qu'on va placer dans la fenêtre Tkinter
Score_Frame = Frame(jeu, bg = 'blue', width = f'{screen_width}', height=f'{score_height}')
menu = Frame(jeu, bg = 'white', width = f'{menu_width}', height = f'{screen_height}')
interface_jeu = Frame(jeu, width = '1500', height = '1500') 

#Pack
Score_Frame.pack(side = 'top', padx = 0, pady = 0)
menu.pack(side = 'right', padx= menu_width, pady= 0)
interface_jeu.pack(side = 'left')
#Création du Canvas avec son background
canevas = Canvas(interface_jeu, width = 1500, height = 1500)

photo = PhotoImage(file = "wallpaper.png")
background = canevas.create_image(0, 0, image = photo, anchor = "nw")

#On rajoute le canvas dans l'interface du jeu + la taille de la fenetre
canevas.pack()
jeu.geometry(f'{screen_width}x{screen_height}')

#Création des objets dans l'interface graphique
Score = 0

#Création des images d'alien
basic_alien = PhotoImage(file = "basic_alien.png")
bonus_alien = PhotoImage(file = "bonus_alien.png")
tir_alien = PhotoImage(file = "tir_alien.png")

#Création des aliens
def creation_alien():
    global liste_alien_modele, interface_jeu_width
    x0 = interface_jeu_width//10

    for i in range(10):

        alien = canevas.create_image(x0 + i*100, 100, image = tir_alien, tags = "alien")
        alien_cree = Alien_Qui_Tire(50,67, [x0 + i*100, 100], 0)
        liste_alien_modele.append([alien_cree.__get_tir__(), alien, alien_cree.__get_sens__(), alien_cree.__get_bonus__()])
    for i in range(10): 
        alien = canevas.create_image(x0 + i*100, 200, image = basic_alien, tags = "alien")
        alien_cree = Alien(50,67, [x0 + i*100, 200], 0)
        liste_alien_modele.append([alien_cree.__get_tir__(), alien, alien_cree.__get_sens__(), alien_cree.__get_bonus__()])

def creation_alien_bonus():
    global liste_alien_modele, interface_jeu_width
    proba = random()
    x0 = interface_jeu_width//10

    if proba < 0.1:
        alien = canevas.create_image(interface_jeu_width/4, 100, image = bonus_alien, tags = "alien")
        alien_cree = Alien(50,67, [x0 + proba*100, 100], 1)
        liste_alien_modele.append([alien_cree.__get_tir__(), alien, alien_cree.__get_sens__(), alien_cree.__get_bonus__()])
    if len(liste_alien_modele) == 0:
        return
    canevas.after(1000, creation_alien_bonus)


#On crée les 3 ilôts de protection
x_1=15*interface_jeu_width//100-150
x_2= interface_jeu_width//2-150
x_3= 85*interface_jeu_width//100-150
y=interface_jeu_height-300

position1=[x_1,y]
position2=[x_2,y]
position3=[x_3,y]

ilot1=Ilot(position1,2,300,100,'ilot1')
ilot2=Ilot(position2,2,300,100,'ilot2')
ilot3=Ilot(position3,2,300,100,'ilot3')

ilot1_forme= ilot1.construction(canevas)
ilot2_forme= ilot2.construction(canevas)
ilot3_forme= ilot3.construction(canevas)

#Vaisseau 

x0_vaisseau = interface_jeu_width//2 - 100
x_vaisseau = interface_jeu_width//2 + 100
y0_vaisseau = interface_jeu_height -50
y_vaisseau = interface_jeu_height -100
vaisseau = canevas.create_rectangle(x0_vaisseau, y0_vaisseau, x_vaisseau, y_vaisseau, fill = 'white', tags = "vaisseau")
VAISSEAU = Vaisseau([x0_vaisseau,y0_vaisseau,x_vaisseau,y_vaisseau])

#Nombre de vie

vie_initiale = 5
liste_vie = []
photo_heart = PhotoImage(file = "heart2.png")
for i in range(vie_initiale):
    liste_vie.append(canevas.create_image(interface_jeu_width - 20*i - 20, 20, image = photo_heart,anchor = "ne", tags = "vie"))

def vie_vaisseau(): #Fonction qui gère le nombre de vie de la liste et le nombre de vie en graphique
    global VAISSEAU, vie_initiale, liste_vie
    if VAISSEAU.vie != vie_initiale:
        vie_initiale -=1
        canevas.delete(liste_vie[-1])
        liste_vie.remove(liste_vie[-1])
    canevas.after(100, vie_vaisseau)


#Fonctions pour le fonctionnement du jeu

#Déplacement

def deplacement_gauche(event):#Déplace le vaisseau avec la touche gauche
    if canevas.coords("vaisseau")[0] < 0:
        canevas.move("vaisseau",0,0)
    else:
        canevas.move("vaisseau", -50, 0)


def deplacement_droite(event): #Déplace le vaisseau avec la touche droite
    if canevas.coords("vaisseau")[2] > interface_jeu_width:
        canevas.move("vaisseau", 0, 0)
    else:
        canevas.move("vaisseau", 50, 0)

def deplacement_tir(): #Déplace les tirs du vaisseau
    canevas.move("tir_vaisseau", 0, -20)
    canevas.after(100, deplacement_tir)

def deplacement(): #Déplace les tirs des aliens
    canevas.move("tir", 0, 10)
    canevas.after(50, deplacement)

def sens_deplacement_alien(): #Déplacement des aliens avec prise en compte du rebond sur le côté de la fenêtre du jeu
    global liste_alien_modele, interface_jeu_width,interface_jeu_height
    if len(liste_alien_modele) == 0:
        messagebox.showinfo("Résultat", "Vous avez gagné!")
        return
    for i in range(len(liste_alien_modele)):
        if canevas.coords(liste_alien_modele[i][1]) == []:
            liste_alien_modele.remove(liste_alien_modele[i])
            break
        if canevas.coords(liste_alien_modele[i][1])[0] > interface_jeu_width -200 :
            liste_alien_modele[i][2]= -1
            canevas.move(liste_alien_modele[i][1], 0, 50)
        elif canevas.coords(liste_alien_modele[i][1])[0] < 0 :
            liste_alien_modele[i][2]= 1
            canevas.move(liste_alien_modele[i][1], 0, 50)
        elif canevas.coords(liste_alien_modele[i][1])[1] >= interface_jeu_height or VAISSEAU.vie == 0:
            return perdu()
        canevas.move(liste_alien_modele[i][1], liste_alien_modele[i][2]*20, 0)
    canevas.after(100 ,sens_deplacement_alien)




#Gestion des collisions
def collision():
    global ilot1,ilot2,ilot3
    canevas.after(50,collision)
    collision1 =canevas.find_overlapping(ilot1.__get_position__()[0],ilot1.__get_position__()[1],ilot1.__get_position__()[0]+ilot1.__get_longueur__(),ilot1.__get_position__()[1]+ilot1.__get_largeur__())
    if len(collision1) > 2 and ilot1.__get_hp__()!=0 :
        for i in range(1,len(collision1)):
            canevas.delete(collision1[1])
        return enlevehp_1()
    
    collision2 =canevas.find_overlapping(ilot2.__get_position__()[0],ilot2.__get_position__()[1],ilot2.__get_position__()[0]+ilot2.__get_longueur__(),ilot2.__get_position__()[1]+ilot2.__get_largeur__())
    if len(collision2) > 2 and ilot2.__get_hp__()!=0 :
        for i in range(1,len(collision2)):
            canevas.delete(collision2[i])
        return enlevehp_2()

    collision3 =canevas.find_overlapping(ilot3.__get_position__()[0],ilot3.__get_position__()[1],ilot3.__get_position__()[0]+ilot3.__get_longueur__(),ilot3.__get_position__()[1]+ilot3.__get_largeur__())
    if len(collision3) > 2 and ilot3.__get_hp__()!=0 :
        for i in range(1,len(collision3)):
            canevas.delete(collision3[1])
        return enlevehp_3()

def enlevehp_1(): 
    global ilot1,ilot1_forme
    if ilot1.protection(canevas) and ilot1.__get_hp__!=0:
        canevas.delete(ilot1_forme)
        ilot1_forme= ilot1.construction(canevas)
    else:
        canevas.delete(ilot1_forme)     
    canevas.pack()

def enlevehp_2():
    global ilot2,ilot2_forme
    if ilot2.protection(canevas) and ilot2.__get_hp__!=0:
        canevas.delete(ilot2_forme)
        ilot2_forme= ilot2.construction(canevas)
    else:
        canevas.delete(ilot2_forme)     
    canevas.pack()

def enlevehp_3():
    global ilot3,ilot3_forme
    if ilot3.protection(canevas) and ilot3.__get_hp__!=0:
        canevas.delete(ilot3_forme)
        ilot3_forme= ilot3.construction(canevas)
    else:
        canevas.delete(ilot3_forme)     
    canevas.pack()

def destruction_tir(): #Gestion de la destruction des tirs lorsqu'ils dépassent la fenêtre de jeu
    global liste_tir, liste_tir_alien
    for i in range(len(liste_tir)):
        coords = canevas.coords(liste_tir[i])
        if coords == []:
            liste_tir.remove(liste_tir[i])
            break

        if coords[3] < 0:
            canevas.delete(liste_tir[i])
    for j in range(len(liste_tir_alien)):
        coords = canevas.coords(liste_tir_alien[j])
        if coords == []:
            liste_tir_alien.remove(liste_tir_alien[j])
            break
        if coords[3] > interface_jeu_height:
            canevas.delete(liste_tir_alien[j])
    canevas.after(100,destruction_tir)

def collision_boum():
    """Gestion de toutes les autres collisions et de l'ajout du score en fonction du type d'ennemi abattu.
    On différencie les tirs des aliens et les tirs du vaisseau
    On enlève également des vies au vaisseau s'il est touché"""
    global liste_alien_modele, liste_tir, liste_tir_alien, vaisseau, Score
    for i in range(len(liste_tir)):
        coords = canevas.coords(liste_tir[i])
        if coords == []:
            liste_tir.remove(liste_tir[i])
            break
        impact = canevas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
        for id_canevas_overlapped in impact:
            for k in range(len(liste_alien_modele)):
                if liste_alien_modele[k][1] == id_canevas_overlapped:
                    if liste_alien_modele[k][3] == 1:
                        Score +=200
                        score_total.set("Score : "+str(Score))
                    if liste_alien_modele[k][0]:
                        Score += 50
                        score_total.set("Score : " + str(Score))
                    else:
                        Score += 10
                        score_total.set("Score : " + str(Score))
                    canevas.delete(liste_alien_modele[k][1])
                    canevas.delete(liste_tir[i])   
    for j in range(len(liste_tir_alien)):
        coords = canevas.coords(liste_tir_alien[j])
        if coords == []:
            liste_tir_alien.remove(liste_tir_alien[j])
            break
        impact = canevas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
        for id_canevas_overlapped in impact:
            if vaisseau == id_canevas_overlapped:
                canevas.delete(liste_tir_alien[j])
                VAISSEAU.vie -=1
    canevas.after(100,collision_boum)




#Création des tirs
def tir_vaisseau(event):
    global liste_tir
    position = canevas.coords("vaisseau")
    tir = Tir([(position[0]+position[2])/2, position[1]], 10, 50, 1)
    tir_liste = canevas.create_rectangle(tir.__get_position__()[0], tir.__get_position__()[1] - 40, tir.__get_position__()[0] + tir.__get_longueur__(), tir.__get_position__()[1] + tir.__get_largeur__() - 40, fill = "black", tags = "tir_vaisseau")
    liste_tir.append(tir_liste)

def tir_aliens():
    global liste_alien_modele, liste_tir_alien
    nombre_alien = len(liste_alien_modele)
    p = randint(1,nombre_alien)
    if nombre_alien == 0:
        return
    if liste_alien_modele[p-1][0]:
        position=canevas.coords(liste_alien_modele[p][1])
        tir_alien= Tir([(position[0])/2,position[1]],10,50,1)
        tir_forme= canevas.create_rectangle(tir_alien.__get_position__()[0] + 25,tir_alien.__get_position__()[1],tir_alien.__get_position__()[0]+tir_alien.__get_longueur__(),tir_alien.__get_position__()[1]+tir_alien.__get_largeur__(),fill='black', tags='tir')
        liste_tir_alien.append(tir_forme)
    canevas.after(1000,tir_aliens)





#Messages gagner ou perdre
def perdu():
    messagebox.showinfo('Résultat', 'Vous avez perdu !')  

def gagne():
    messagebox.showinfo("Résultat", "Vous avez gagné!")
    




#Nouvelle partie
def main(event):
    global liste_alien_modele, liste_tir, liste_tir_alien,Score
    liste_alien_modele = []
    liste_tir = []
    liste_tir_alien = []
    Score = 0
    score_total.set("Score : " + str(Score))

    creation_alien()
    creation_alien_bonus()
    tir_aliens()   
    deplacement()
    sens_deplacement_alien()
    collision()
    deplacement_tir()
    collision_boum()
    vie_vaisseau()
    destruction_tir()

def setting():
    main()
#Destruction
def destruction(event):
    return jeu.destroy()


jeu.bind("<Left>", deplacement_gauche)
jeu.bind("<Right>", deplacement_droite)
jeu.bind("<Up>", tir_vaisseau)
jeu.bind("<Return>", main)
jeu.bind("<Escape>", destruction)

canevas.pack()
debut_partie = Button(menu, text = "Nouvelle partie", command = setting).pack()
quitter = Button(menu, text = "Quitter", command = jeu.destroy).pack()

score_total = StringVar()
score_total.set("Score : " + str(Score))
scorelabel = Label(Score_Frame, textvariable = score_total).pack(padx = 700, pady = 20)

jeu.mainloop()
