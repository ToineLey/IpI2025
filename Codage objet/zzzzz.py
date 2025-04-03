import os
from time import sleep
from decor import *
from personnage import Personnage
from touches import *
import threading

A = Grille()  # Crée la grille de jeu
P = Personnage(A)  # Initialise le personnage de jeu

A.remplir(0, 1)


def interact():
    # gestion des evenement clavier

    # si une touche est appuyee

        c = sys.stdin.read(1)
        if c == '\x1b':  # x1b is ESC
            P.mort=True
        elif c == 'd':
            P.droite()
            P.mouvement()
        elif c == 'q':
            P.gauche()
            P.mouvement()
        elif c == ' ':
            P.change_gravite()
P.mouvement()


def gameloop():
    key = ""
    while not P.mort or key != "m":  # Boucle de jeu
        key = getch()  # Lire une touche avec la fonction modifiée
        os.system("clear")
        print(A)
        interact()
        # Traite l'entrée utilisateur
        # Appelle le mouvement du personnage en jeu
        sleep(0.06)  # Pause dans le temps
        print(P)
        if P.mort:  # Si le personnage est mort, fin de la boucle
            os.system("clear")
            print(recreer("mort"))
            break


gameloop()
