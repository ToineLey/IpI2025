#fonction de lecture de csv
import csv
f=open("niveau.csv")
niveau=list(csv.reader(f))
f.close()



class Grille:
    def __init__(self,niveau):
        pass
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
    PORTENESW=50
    PORTEHAUT=51
    PORTENWSE=52
    PORTEGAUCHE=53
    PORTEDROITE=54
    PORTEBHAS=55
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

