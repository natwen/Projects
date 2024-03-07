class Alien:
    def __init__(self,longueur,largeur,position, bonus) :
        self.__longueur = longueur 
        self.__largeur = largeur
        self.__position = position  #position sous la forme d'une liste de la forme [position en x, position en y]
        self.__sens_deplacement = 1 # nous indique le sens de déplacement de l'alien :quand il vaut 1, déplacement vers les x positifs quand il vaut -1, déplacement vers les x négatifs
        self.__tir = False # tir est un booléen qui nous renseigne sur la capacité pour un alien de tirer ou non
        self.bonus = bonus

    def collision(self,largeur_fenetre) : # on change le sens de déplacement
        -1*self.__sens_deplacement
        return self.deplacer_x(largeur_fenetre)

    def deplacer_x(self,dx) : # objectif : déplacer l'alien horizontalement 
        self.__position[0] += dx*self.__sens_deplacement
        return self.__position

    def rebond(self):
        self.__position[1] = self.__position[1] -20

    def __get_position__(self) :
        return self.__position

    def __get_largeur__(self) :
        return self.__largeur

    def __get_longueur__(self) :
        return self.__longueur

    def __get_tir__(self) :
        return self.__tir

    def __get_sens__(self) :
        return self.__sens_deplacement
    def __get_bonus__(self):
        return self.bonus
        
    def deplacer_y(self,hauteur_fenetre): # objectif : déplacer l'alien verticalement 
        dy=hauteur_fenetre/100 # 100 = valeur à changer peut être
        if self.__position[1] < hauteur_fenetre: # correspond à un déplacement en bas
            self.__position[1] -= dy

        

class Alien_Qui_Tire(Alien):
    def __init__(self,longueur,largeur,position, bonus) :
        self.__longueur = longueur 
        self.__largeur = largeur
        self.__position = position  #position sous la forme d'une liste de la forme [position en x, position en y]
        self.__sens_deplacement = 1 # nous indique le sens de déplacement de l'alien :quand il vaut 1, déplacement vers les x positifs quand il vaut -1, déplacement vers les x négatifs
        self.__tir = True
        self.bonus = bonus
    def __get_tir__(self) :
        return self.__tir
    def __get_sens__(self) :
        return self.__sens_deplacement
    def __get_bonus__(self):
        return self.bonus
