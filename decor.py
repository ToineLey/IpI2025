#fonction de lecture de csv
import csv
f=open("niveau.csv")
niveau=list(csv.reader(f))
f.close()



class Grille:
    def __init__(self,niveau):
        pass


class Case:
    def __init__(self,x:int,y:int,etat:Etat):
        self.x=x
        self.y=y
        self.etat=etat

class Etat:
    VIDE=0
    PERSONNAGE=1
    PLEIN=2
    PARTIEL=3
    ENNEMI=4
    PORTE=5
    CLEF=6
    PIC=7