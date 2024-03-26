"""
Ce programme génère des clauses CNF pour un problème de coloration de graphe,
en assurant qu'aucun couple de sommets adjacents ne partage la même couleur.
J'ai choisi de le modeliser en ayant 3 nombres par sommets:
1, 2 et 3 pour le sommet 1. 4, 5 et 6 pour le sommet 2 et ainsi de suite
chaque nombre représente une couleur :
3k=Bleu
3k+1=Rouge
3k+2=Vert
(x//3)+1 donne le sommet
et x%3 donne la couleur
"""


def voisins_differents(origine: int, arrivee: int):
    """
    Ajoute des clauses pour s'assurer que les sommets reliés par un arc ont
    des couleurs différentes.
    """
    with open("ex3.cnf", "a") as fichier:
        for i in range(3):
            fichier.write(
                f"-{3 * (origine -1 ) + i + 1} -{3 * (arrivee -1) + i + 1} 0\n"
            )


def au_moins_1_couleur(nombre_de_sommets: int):
    """
    Ajoute des clauses pour s'assurer qu'un sommet a au moins une couleur.
    """
    with open("ex3.cnf", "a") as fichier:
        for k in range(nombre_de_sommets):
            fichier.write(f"{3 * k + 1} {3 * k + 2} {3 * k + 3} 0\n")


def au_plus_1_couleur(nombre_de_sommets: int):
    """
    Ajoute des clauses pour s'assurer qu'un sommet a au plus une couleur.
    """
    with open("ex3.cnf", "a") as fichier:
        for i in range(nombre_de_sommets):
            fichier.write(f"-{3 * i + 1} -{3 * i + 2} 0\n")
            fichier.write(f"-{3 * i + 1} -{3 * i + 3} 0\n")
            fichier.write(f"-{3 * i + 3} -{3 * i + 2} 0\n")


def total():
    """
    Crée le fichier CNF pour le problème de coloration du graphe.
    """
    arcs = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 1],
        [1, 6],
        [2, 7],
        [3, 8],
        [4, 9],
        [5, 10],
        [6, 8],
        [7, 9],
        [8, 10],
        [9, 6],
        [10, 7],
    ]
    sommets = list(set(j for i in arcs for j in i))  # Utiliser la compréhension de set
    nb_sommets = len(sommets)
    nb_clause = nb_sommets * 4 + len(arcs) * 3

    with open("ex3.cnf", "a") as fichier:
        fichier.write("c tp2_ex3.cnf\n")
        fichier.write("c\n")
        fichier.write(f"p cnf {nb_sommets * 3} {nb_clause}\n")
        au_moins_1_couleur(nb_sommets)
        au_plus_1_couleur(nb_sommets)
        for lien in arcs:
            voisins_differents(lien[0], lien[1])


total()
