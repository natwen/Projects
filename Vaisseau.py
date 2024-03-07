class Vaisseau:
    def __init__(self,position, vie = 5):
        self.__position = position #une liste de 2 coordonnées : x0, x
        self.vie = vie

    def bloquer(self, interface_jeu):
        if self.__position[1] == interface_jeu:
            return False #à changer 
        if self.__position[0] == 0:
            return False #à changer
        
    def vie(self):
        self.vie -= 1