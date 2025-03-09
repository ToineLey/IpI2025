import os
from time import sleep
from decor import *
from personnage import Personnage
from touches import *
import threading


A = Grille()  # Crée la grille de jeu
P = Personnage(A)  # Initialise le personnage de jeu


A.remplir(0, 1)

key=""



def key_pressed(obj,l:Personnage):
    while not P.mort or key!="m":
        if obj=="d":
            l.droite()
            P.mouvement()
            print("hey")
        elif obj=="q":
            l.gauche()
            P.mouvement()
        elif obj==" ":
            l.change_gravite()
            P.mouvement()
        else:
            pass


key_thread = threading.Thread(target=key_pressed, args=(key,P))


def gameloop(key:str = ""):
    while not P.mort or key!="m":  # Boucle de jeu
        key = getch()  # Lire une touche avec la fonction modifiée
        os.system("clear")
        print(A)
          # Traite l'entrée utilisateur
          # Appelle le mouvement du personnage en jeu
        sleep(0.06)  # Pause dans le temps
        print(P)
        if P.mort:  # Si le personnage est mort, fin de la boucle
            os.system("clear")
            print(recreer("mort"))
            break

game_thread = threading.Thread(target=gameloop)
key_thread.start()
game_thread.start()
