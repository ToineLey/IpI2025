from case import Case, Etat


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
        Etat.PLEINBASDROIfrom case import Case, EtatTE: "┘",
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

def recreer(txt:str):
    text = txt+".txt"
    open_txt(text)
    text = open_txt(text).read()
    return text

if __name__ == "__main__":
    print(recreer("mort"))