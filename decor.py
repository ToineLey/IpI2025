import convertisseur
from convertisseur import *
from case import *


class Grille:
    def __init__(self):
        self.grille = []

    def remplir(self, niveau: int, tableau: int):
        def open_txt(text):
            txt = open(text, 'r')
            return txt

        obj = open_txt(f"niveau-{niveau}.txt").read()
        self.grille = convertisseur.convert(obj)
        for i in range(len(self.grille)):
            self.grille[i] = self.grille[i][86 * (tableau - 1):86 * tableau]
        convertisseur.uniformise(self.grille)

    def __str__(self):
        ban = convertisseur.inverse_convert(self.grille)
        return ban


if __name__ == '__main__':
    A = Grille()
    A.remplir(0, 1)
    print(A)
    for i in range(len(A.grille)):
        for case in A.grille[i]:
            if case.etat == Etat.PERSONNAGENORMAL or case.etat == Etat.PERSONNAGEINVERSE:
                print(case.x, case.y)
