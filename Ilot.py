from tkinter import *

class Ilot :
    def __init__(self,position,hp,longueur,largeur,name):
        self.__position = position #une liste de la forme [coords en x, coords en y]
        self.__longueur = longueur
        self.__largeur = largeur
        self.__name=name
        self.__hp = hp #nombre entier qui représente le nombre de coup que peut subir l'ilôt de protection

    def __get_position__(self) :
        return self.__position

    def __get_largeur__(self) :
        return self.__largeur

    def __get_longueur__(self) :
        return self.__longueur

    def __get_hp__(self) :
        return self.__hp

    def construction(self,canevas):
        return canevas.create_rectangle(self.__get_position__()[0],self.__get_position__()[1],self.__get_position__()[0]+self.__get_longueur__(),self.__get_position__()[1]+self.__get_largeur__(),fill='black', tags = "ilot")

    def protection(self,canevas): # quand l'ilôt recoit un tir il doit le bloquer et perdre 1 hp   
        self.__hp -= 1
        if self.__hp ==1 :
            self.__largeur=self.__largeur/2
            self.__position[1]+=self.__largeur
        return self.__hp==1






