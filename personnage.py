from decor import *


class Personnage:
    def __init__(self,grille:Grille):
        self.traction = True
        self.direction = 0
        self.clef = False
        self.grille=grille

        for i in range(len(self.grille.grille)):
            for case in self.grille.grille[i]:
                if case.etat == Etat.PERSONNAGENORMAL or case.etat == Etat.PERSONNAGEINVERSE:
                    print(case.x, case.y)
        self.x = 8
        self.y = 15
    def gauche(self):
        if self.direction==1:
            self.direction-=2
        else:
            self.direction-=1
    def droite(self):
        if self.direction==-1:
            self.direction+=2
        else:
            self.direction+=1
    def mouvement(self):
        if self.direction==1:
            self.grille.grille[self.y][self.x].x,self.grille.grille[self.y][self.x+1].x=self.grille.grille[self.y][self.x+1].x,self.grille.grille[self.y][self.x].x
        elif self.direction==-1:
            self.grille.grille[self.y][self.x].x,self.grille.grille[self.y][self.x-1].x=self.grille.grille[self.y][self.x-1].x,self.grille.grille[self.y][self.x].x
        if self.traction:
            if self.grille.grille[self.y-1][self.x].etat==Etat.VIDE:
                self.y-=1
        if not self.traction:
            if self.grille.grille[self.y+1][self.x].etat==Etat.VIDE:
                self.y+=1
    def change_gravite(self):
        self.traction=not self.traction
    def recup(self):
        if not self.clef:
            self.clef=True
    def porte(self):
        if test():
            self.grille.grille[self.y][self.x].etat=Etat.VIDE

def test(a:list):
    return a[self.y][self.x+1].etat in (50,51,52,53,54) or


if __name__ == '__main__':
    A=Grille()
    A.remplir(0,1)
    P=Personnage(A)
    print(A)
    print(P.x,P.y)