import convertisseur
from convertisseur import *

class Grille:
    def __init__(self):
        self.grille=[]
    def remplir(self,niveau:int,tableau:int):
        def open_txt(text):
            txt = open(text, 'r')
            return txt
        obj = open_txt(f"niveau-{niveau}.txt").read()
        self.grille = convertisseur.convert(obj)
        for i in range (len(self.grille)):
            self.grille[i]=self.grille[i][86*(tableau-1):86*tableau]
        convertisseur.uniformise(self.grille)
    def __str__(self):
        ban = convertisseur.inverse_convert(self.grille)
        return ban




class Etat:
    VIDE=0
    PERSONNAGENORMAL=10
    PERSONNAGEINVERSE=11
    PLEINHAUTGAUCHE=20
    PLEINHORIZONTAL=21
    PLEINHAUTDROITE = 22
    PLEINVERTICAL=23
    PLEINBASGAUCHE = 24
    PLEINBASDROITE = 25
    PARTIELHAUTGAUCHE = 30
    PARTIELHORIZONTAL = 31
    PARTIELHAUTDROITE = 32
    PARTIELVERTICAL = 33
    PARTIELBASGAUCHE = 34
    PARTIELBASDROITE = 35
    ENNEMI=4
    PORTECOIN=50
    PORTEHAUT=51
    PORTEGAUCHE=52
    PORTEDROITE=53
    PORTEBHAS=54
    CLEF=6
    PICHAUT = 70
    PICBAS = 71
    PICGAUCHE = 72
    PICDROITE = 73




class Case:
    def __init__(self,x:int,y:int,state:Etat):
        self.x=x
        self.y=y
        self.etat=state

if __name__ == '__main__':
    A=Grille()
    A.remplir(0,3)
    print(A)