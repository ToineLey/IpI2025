from decor import *


class Personnage:
    def __init__(self, grille: Grille):
        self.traction = True
        self.direction = 0
        self.clef = False
        self.grille = grille
        self.x = 8
        self.y = 15
        self.mort = False
        self.pic = (70,71,72,73)

    def gauche(self):
        self.direction = -1

    def droite(self):
        self.direction = 1

    def mouvement(self):
        if not self.mort:
            if self.direction == 1:
                if self.grille.grille[self.y][self.x + 1].etat == Etat.VIDE:
                    if self.grille.grille[self.y][self.x+1].etat in self.pic:
                        self.mort = True
                    if self.traction:
                        self.grille.grille[self.y][self.x].etat, self.grille.grille[self.y][
                            self.x + 1].etat = Etat.VIDE, Etat.PERSONNAGENORMAL
                    else:
                        self.grille.grille[self.y][self.x].etat, self.grille.grille[self.y][
                            self.x + 1].etat = Etat.VIDE, Etat.PERSONNAGEINVERSE
                    self.x += 1
            elif self.direction == -1:
                if self.grille.grille[self.y][self.x - 1].etat == Etat.VIDE:
                    if self.grille.grille[self.y][self.x-1].etat in self.pic:
                        self.mort = True
                    if self.traction:
                        self.grille.grille[self.y][self.x].etat, self.grille.grille[self.y][
                            self.x - 1].etat = Etat.VIDE, Etat.PERSONNAGENORMAL
                    else:
                        self.grille.grille[self.y][self.x].etat, self.grille.grille[self.y][
                            self.x - 1].etat = Etat.VIDE, Etat.PERSONNAGEINVERSE
                    self.x -= 1
            if not self.traction:
                if self.grille.grille[self.y - 1][self.x].etat in self.pic:
                    self.mort = True
                if self.grille.grille[self.y - 1][self.x].etat == Etat.VIDE:
                    self.grille.grille[self.y][self.x].etat, self.grille.grille[self.y - 1][self.x].etat = \
                        self.grille.grille[self.y - 1][self.x].etat, self.grille.grille[self.y][self.x].etat
                    self.y -= 1

            if self.traction:
                if self.grille.grille[self.y + 1][self.x].etat in self.pic:
                    self.mort = True
                if self.grille.grille[self.y + 1][self.x].etat == Etat.VIDE:
                    self.grille.grille[self.y][self.x].etat, self.grille.grille[self.y + 1][self.x].etat = \
                        self.grille.grille[self.y + 1][self.x].etat, self.grille.grille[self.y][self.x].etat
                    self.y += 1

            self.direction = 0

    def change_gravite(self):
        if not self.traction and self.grille.grille[self.y - 1][self.x].etat != Etat.VIDE:
            self.traction = not self.traction
        elif self.traction and self.grille.grille[self.y + 1][self.x].etat != Etat.VIDE:
            self.traction = not self.traction

    def recup(self):
        if not self.clef:
            self.clef = True
    def __str__(self):
        return f"Personnage: {self.x}, {self.y}"



if __name__ == '__main__':
    A = Grille()
    A.remplir(0, 1)
    P = Personnage(A)
    print(A)
    print(P.x, P.y)
