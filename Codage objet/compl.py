import termios
import sys
import tty
import time
import os
import threading
import select


class Etat:
    VIDE = 0
    PERSONNAGENORMAL = 10
    PERSONNAGEINVERSE = 11
    PLEINHAUTGAUCHE = 20
    PLEINHORIZONTAL = 21
    PLEINHAUTDROITE = 22
    PLEINVERTICAL = 23
    PLEINBASGAUCHE = 24
    PLEINBASDROITE = 25
    PARTIELHAUTGAUCHE = 30
    PARTIELHORIZONTAL = 31
    PARTIELHAUTDROITE = 32
    PARTIELVERTICAL = 33
    PARTIELBASGAUCHE = 34
    PARTIELBASDROITE = 35
    ENNEMI = 4
    PORTECOIN = 50
    PORTEHAUT = 51
    PORTEGAUCHE = 52
    PORTEDROITE = 53
    PORTEBHAS = 54
    CLEF = 6
    PICHAUT = 70
    PICBAS = 71
    PICGAUCHE = 72
    PICDROITE = 73


class Case:
    def __init__(self, x: int, y: int, state: int):
        self.x = x
        self.y = y
        self.etat = state


def open_txt(text):
    txt = open(text, 'r')
    return txt


def min_len(l):
    b = 0
    c = 0
    t = 999
    for sub in l:
        if len(sub) < t:
            t = len(sub)
            c = b
        b += 1
    return c


def convert(lst):
    a = 0
    b = 0
    l = [[]]
    bl = {}
    for i in lst:
        if i == '┌':
            l[a].append(Case(b, a, Etat.PLEINHAUTGAUCHE))
        elif i == '─':
            l[a].append(Case(b, a, Etat.PLEINHORIZONTAL))
        elif i == '┐':
            l[a].append(Case(b, a, Etat.PLEINHAUTDROITE))
        elif i == '│':
            l[a].append(Case(b, a, Etat.PLEINVERTICAL))
        elif i == '└':
            l[a].append(Case(b, a, Etat.PLEINBASGAUCHE))
        elif i == '┘':
            l[a].append(Case(b, a, Etat.PLEINBASDROITE))
        elif i == "╔":
            l[a].append(Case(b, a, Etat.PARTIELHAUTGAUCHE))
        elif i == "═":
            l[a].append(Case(b, a, Etat.PARTIELHORIZONTAL))
        elif i == "╗":
            l[a].append(Case(b, a, Etat.PARTIELHAUTDROITE))
        elif i == "║":
            l[a].append(Case(b, a, Etat.PARTIELVERTICAL))
        elif i == "╚":
            l[a].append(Case(b, a, Etat.PARTIELBASGAUCHE))
        elif i == "╝":
            l[a].append(Case(b, a, Etat.PARTIELBASDROITE))
        elif i == "?":
            l[a].append(Case(b, a, Etat.PERSONNAGENORMAL))
        elif i == "¿":
            l[a].append(Case(b, a, Etat.PERSONNAGEINVERSE))
        elif i == "▲":
            l[a].append(Case(b, a, Etat.PICHAUT))
        elif i == "▼":
            l[a].append(Case(b, a, Etat.PICBAS))
        elif i == "◄":
            l[a].append(Case(b, a, Etat.PICGAUCHE))
        elif i == "►":
            l[a].append(Case(b, a, Etat.PICDROITE))
        elif i == "█":
            l[a].append(Case(b, a, Etat.PORTECOIN))
        elif i == "▀":
            l[a].append(Case(b, a, Etat.PORTEHAUT))
        elif i == "▌":
            l[a].append(Case(b, a, Etat.PORTEGAUCHE))
        elif i == "▐":
            l[a].append(Case(b, a, Etat.PORTEDROITE))
        elif i == "▄":
            l[a].append(Case(b, a, Etat.PORTEBHAS))
        elif i == "⤖":
            l[a].append(Case(b, a, Etat.CLEF))
        elif i == "Ω":
            l[a].append(Case(b, a, Etat.ENNEMI))
        elif i == " ":
            l[a].append(Case(b, a, Etat.VIDE))
        elif i == "\n":
            l.append([])
            bl.update({a: b})
            b = 0
            a += 1
        b += 1
    return l


def uniformise(l):
    mxl = 86
    mnl = min_len(l)
    while mxl != len(l[mnl]):
        mnl = min_len(l)
        l[mnl].append(Case(len(l[mnl]), mnl, Etat.VIDE))


def inverse_convert(grille):
    # Dictionnaire de correspondance de chaque état vers son caractère
    mapping = {
        Etat.VIDE: " ",
        Etat.PERSONNAGENORMAL: "?",
        Etat.PERSONNAGEINVERSE: "¿",
        Etat.PLEINHAUTGAUCHE: "┌",
        Etat.PLEINHORIZONTAL: "─",
        Etat.PLEINHAUTDROITE: "┐",
        Etat.PLEINVERTICAL: "│",
        Etat.PLEINBASGAUCHE: "└",
        Etat.PLEINBASDROITE: "┘",
        Etat.PARTIELHAUTGAUCHE: "╔",
        Etat.PARTIELHORIZONTAL: "═",
        Etat.PARTIELHAUTDROITE: "╗",
        Etat.PARTIELVERTICAL: "║",
        Etat.PARTIELBASGAUCHE: "╚",
        Etat.PARTIELBASDROITE: "╝",
        Etat.ENNEMI: "Ω",
        Etat.PORTECOIN: "█",
        Etat.PORTEHAUT: "▀",
        Etat.PORTEGAUCHE: "▌",
        Etat.PORTEDROITE: "▐",
        Etat.PORTEBHAS: "▄",
        Etat.CLEF: "⤖",
        Etat.PICHAUT: "▲",
        Etat.PICBAS: "▼",
        Etat.PICGAUCHE: "◄",
        Etat.PICDROITE: "►"
    }

    lignes = []
    for ligne in grille:
        ligne_str = ""
        for case in ligne:
            # Récupère le caractère correspondant à l'état de la case
            # Par défaut, on affiche " ?" si l'état n'est pas trouvé
            ligne_str += mapping.get(case.etat, "#")
        lignes.append(ligne_str)

    # On retourne le résultat sous forme d'une chaîne multiligne
    return "\n".join(lignes)


def recreer(txt: str):
    text = txt + ".txt"
    open_txt(text)
    text = open_txt(text).read()
    return text


class Grille:
    def __init__(self):
        self.grille = []

    def remplir(self, niveau: int, tableau: int):
        if not self.grille:
            obj = open_txt(f"niveau-{niveau}.txt").read()
            self.grille = convert(obj)
            for i in range(len(self.grille)):
                self.grille[i] = self.grille[i][86 * (tableau - 1):86 * tableau]
            uniformise(self.grille)

    def __str__(self):
        ban = inverse_convert(self.grille)
        return ban


class Personnage:
    def __init__(self, grille: Grille):
        self.traction = True
        self.direction = 0
        self.clef = False
        self.grille = grille
        self.x = 8
        self.y = 15
        self.mort = False
        self.pic = (70, 71, 72, 73)

    def gauche(self):
        self.direction = -1

    def droite(self):
        self.direction = 1

    def mouvement(self):
        if not self.mort:
            if self.direction == 1:
                if self.grille.grille[self.y][self.x + 1].etat == Etat.VIDE:
                    if self.grille.grille[self.y][self.x + 1].etat in self.pic:
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
                    if self.grille.grille[self.y][self.x - 1].etat in self.pic:
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

def key_listener():
    """ Thread qui écoute en continu les entrées clavier """
    global pressed_keys

    # Configuration du mode non bloquant
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)

    try:
        while True:
            if select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)

                # Quitter avec Échap
                if key == '\x1b':
                    pressed_keys.add('quit')
                    break

                # Gestion des touches directionnelles
                elif key == 'd':
                    pressed_keys.add('d')
                    if 'q' in pressed_keys:  # Éviter les contraires simultanés
                        pressed_keys.remove('q')
                elif key == 'q':
                    pressed_keys.add('q')
                    if 'd' in pressed_keys:
                        pressed_keys.remove('d')

                # Touche espace pour changer la gravité
                elif key == ' ':
                    pressed_keys.add('space')

                # Simuler le relâchement des touches (ceci est une limitation)
                # En pratique, il faudrait une bibliothèque comme keyboard pour détecter le relâchement
                elif key in ('r'):  # 'r' pour reset/relâcher toutes les touches
                    pressed_keys.clear()

            time.sleep(0.01)
    finally:
        # Restaurer les paramètres du terminal
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# Remplacer la fonction gameloop par celle-ci
def gameloop():
    global pressed_keys
    last_update = time.time()
    frame_count = 0

    # Variables d'état pour gérer le changement de gravité
    gravite_cooldown = 0
    last_space_press = False

    while not P.mort and 'quit' not in pressed_keys:
        frame_count += 1
        os.system("clear")  # Efface l'écran

        # Affichage de l'état du jeu
        print(A)  # Affichage de la grille
        print(P)  # Affichage du personnage
        print("Touches: ", pressed_keys)  # Debug

        # Gestion des entrées
        if 'd' in pressed_keys:
            P.droite()
        elif 'q' in pressed_keys:
            P.gauche()
        else:
            P.neutre()  # Ralentissement naturel

        # Gestion du changement de gravité (avec cooldown)
        space_pressed = 'space' in pressed_keys
        if space_pressed and not last_space_press and gravite_cooldown <= 0:
            if P.change_gravite():  # Tente de changer la gravité
                gravite_cooldown = 15  # ~0.5 secondes
        last_space_press = space_pressed

        # Consommer l'événement espace pour éviter les répétitions
        if 'space' in pressed_keys:
            pressed_keys.remove('space')

        # Décrémentation du cooldown
        if gravite_cooldown > 0:
            gravite_cooldown -= 1

        # Mise à jour de la position
        P.mouvement()

        # Calcul du temps d'attente pour maintenir une fréquence constante
        now = time.time()
        elapsed = now - last_update
        frame_duration = 1 / 30  # 30 FPS

        if elapsed < frame_duration:
            time.sleep(frame_duration - elapsed)

        last_update = time.time()

    # Fin de partie
    os.system("clear")
    print(recreer("mort"))


# Initialisation du jeu reste identique
A = Grille()
P = Personnage(A)
A.remplir(0, 1)

# Lancer le jeu
keyboard_thread = threading.Thread(target=key_listener, daemon=True)
keyboard_thread.start()
gameloop()