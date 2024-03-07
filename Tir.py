from tkinter import *

class Tir:
    def __init__(self,position,longueur,largeur,sens):
        self.__position=position #altitude de départ du tir 
        self.__longueur=longueur
        self.__largeur = largeur
        self.__sens=sens # détermine si le tir fait vaisseau--> alien ou alien-->vaisseau

    def deplacement(self): #faire déplacer le tir verticalement
        #dans la fonction principale ?
        return 1==1
    def collision(self):
        # doit supprimer le tir
        return 1==1
    def __get_position__(self) :
        return self.__position

    def __get_largeur__(self) :
        return self.__largeur

    def __get_longueur__(self) :
        return self.__longueur
        
    def construction(self,canevas):
        return canevas.create_rectangle(self.__position[0],self.__position[1],self.__position[0]+self.__longueur,self.__position[1]+self.__largeur,fill='black',tags='tir')