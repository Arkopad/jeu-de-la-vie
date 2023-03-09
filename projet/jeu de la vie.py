# importation des librairies
from random import randint
import copy
from tkinter import *
import time

def echap(event):
    """
    def: sur appui de la touche "échap", quitte la fenêtre
    in:
    out:
    """
    if event.keysym == "Escape":
        window.destroy()


def fullscreen(event):
    """
    def: sur appui de la touche "F11" active/désactive le plein écran
    in:
    out:
    """
    global is_fullscreen
    global taille_case
    if event.keysym == "F11":
        if is_fullscreen == True:
            for lignes in range(nombre_case_y):
                for colonnes in range(nombre_case_x):
                    cellule[lignes][colonnes].config(height="19", width="19")
                    taille_case = 19

            is_fullscreen = False
            window.attributes("-fullscreen", False)
        else:
            for lignes in range(nombre_case_y):
                for colonnes in range(nombre_case_x):
                    cellule[lignes][colonnes].config(height="30", width="30")
                    taille_case = 30

            window.attributes("-fullscreen", True)
            is_fullscreen = True

def speed(event):
    """
    def: sur appui de la touche "espace", change la vitesse de lecture de l'algorithme
    in:
    out:
    """
    global vitesse
    if event.keysym == "space":
        if vitesse == 0.05:
            vitesse = 0.001
            text_vitesse.config(text="Vitesse : x10")
        elif vitesse == 0.001:
            vitesse = 0.5
            text_vitesse.config(text="Vitesse : x1")
        elif vitesse == 0.5:
            vitesse = 0.05
            text_vitesse.config(text="Vitesse : x5")

def restart(event):
    """
    def: sur appui de la touche "entrée", relance le jeu de la vie
    in:
    out:
    """
    if event.keysym == "Return":
        jeu(plateau(nombre_case_x, nombre_case_y, "X"), nombre_vivant, nombre_tour)

def plateau(x, y, charactere):
    """
    def: crée le plateau console
    in:
    out:
    """

    plateau = []

    for i in range(y):
        lignes = []

        for j in range(x):
            lignes.append(charactere)

        plateau.append(lignes)

    return plateau


def cellule_autour(grilles, ligne, colonne):
    """
    def: Retourne le nombre de cellules vivantes parmi les 8 cellules entourant la cellule de coordonnées ligne, colonne
    in:
    out:
    """

    cellule_vivante = 0
    cellule_morte = 0

    for i in range(max(0, ligne - 1), min(len(grilles), ligne + 2)):
        for j in range(max(0, colonne - 1), min(len(grilles[0]), colonne + 2)):
            if i == ligne and j == colonne:
                continue
            if grilles[i][j] == "X":
                cellule_vivante += 1
            else:
                cellule_morte += 1

    return cellule_vivante


def jeu(grille, nbr_vivant, tour):
    """
    def: Lance le jeu
    in:
    out:
    """

    # place les cellules vivantes dans le plateau console et le plateau GUI
    for vivant in range(nbr_vivant):
        ligne = randint(0, len(grille) - 1)
        colonne = randint(0, len(grille[0]) - 1)
        if len(grille) * len(grille[0]) < nbr_vivant:
            for cellule1 in range(len(grille)):
                for cellule2 in range(len(grille[0])):
                    grille[cellule1][cellule2] = "O"
                    cellule[cellule1][cellule2].config(bg="white")
        else:
            while grille[ligne][colonne] == "O":
                ligne = randint(0, len(grille) - 1)
                colonne = randint(0, len(grille[0]) - 1)
            grille[ligne][colonne] = "O"
            cellule[ligne][colonne].config(bg="white")

    # lance le jeu de la vie pendant 'tour' tours
    a = 0
    while a < tour:
        vivant = 0

        # création d'une grille temporaire pour parcourir la grille initiale sans la modifier
        grille_temp = copy.deepcopy(grille)

        # parcourt toutes les cellules
        for lignes in range(len(grille_temp)):
            for colonnes in range(len(grille_temp[0])):

                # incrémentation du compteur de cellules vivantes
                if grille[lignes][colonnes] == "O":
                    vivant += 1

                # application des règles du jeu de la vie sur la grille GUI et la grille console
                if cellule_autour(grille, lignes, colonnes) == 3:
                    grille_temp[lignes][colonnes] = "O"
                    cellule[lignes][colonnes].config(bg="white")

                elif cellule_autour(grille, lignes, colonnes) == 2:
                    grille_temp[lignes][colonnes] = grille[lignes][colonnes]
                    if grille[lignes][colonnes] == "X":
                        cellule[lignes][colonnes].config(bg="black")
                    else:
                        cellule[lignes][colonnes].config(bg="white")

                else:
                    grille_temp[lignes][colonnes] = "X"
                    cellule[lignes][colonnes].config(bg="black")

        # pause entre chaque tour pour régler la vitesse de lecture
        time.sleep(vitesse)

        # replace la grille à chaque tour
        frame_grille.place(
            x=window.winfo_width() / 2 - nombre_case_x * taille_case / 2,
            y=(window.winfo_height() / 2 + 40) - nombre_case_y * taille_case / 2,)

        # affichages du nombre de tours effectués
        a += 1
        gene = str(a) + "e génération"
        generation.config(text=gene)

        # affichaque du compteur de cellules vivantes
        compteur_vivant.config(text=str(vivant) + "/" + str(nombre_case_x * nombre_case_y))

        # mise à jour de la grille initale par la grille temporaire maintenant remplie
        grille = copy.deepcopy(grille_temp)

        # mise à jour de la fenêtre
        window.update()


if __name__ == "__main__":
    # initialisation des variables globales à modifier
    nombre_case_y = 30
    nombre_vivant = 660
    nombre_tour = 10000
    taille_case = 19

    # variables globales fixes
    nombre_case_x = int(nombre_case_y * 2) - 1
    is_fullscreen = True
    vitesse = 0.001
    # initialisation de la fenetre
    window = Tk()
    window.title("Jeu de la vie")
    window.geometry("1280x720")
    window.iconbitmap("icone.ico")
    window.resizable(0, 0)
    window.config(background="#141418")
    window.attributes("-fullscreen", False)
    window.bind_all("<Key-Escape>", echap)
    window.bind_all("<Key-F11>", fullscreen)
    window.bind_all("<Key-space>", speed)
    window.bind_all("<Key-Return>", restart)


    # paramètres de la bannière supérieure
    frame_top = Frame(
        window,
        borderwidth=2,
        bg="#010D19",
        highlightthickness=5,
        highlightbackground="black",)

    generation = Label(frame_top, text="1e génération", font=("System", 35), bg="#010D19", fg="#A5A5B5")

    text_vitesse = Label(frame_top, text="Vitesse : x10", font=("System", 35), bg="#010D19", fg="#A5A5B5")

    compteur_vivant = Label(frame_top, text=str(nombre_vivant) + "/" + str(nombre_case_x * nombre_case_y), font=("System", 35), bg="#010D19", fg="#A5A5B5")

    # crée le plateau GUI
    frame_grille = Frame(window, bd=3, bg="white")
    cellule = []

    for i in range(nombre_case_y):  # crée une liste de canvas pour pouvoir modifier chaque case de la grille indépendamment
        liste = []
        for j in range(nombre_case_x):
            liste.append(Canvas(frame_grille, bg="black", bd=0, height=19, width=19, highlightthickness=0,))

        cellule.append(liste)

    for horizontal in range(nombre_case_y):  # crée une grille à partir de la liste de canvas
        for vertical in range(nombre_case_x):
            cellule[horizontal][vertical].grid(row=horizontal, column=vertical)

    # affichage de la bannière et des textes
    frame_top.pack(fill=X, pady=20)
    generation.place(relx=0.99, rely=0, anchor="ne")
    text_vitesse.place(relx=0.01, rely=0, anchor="nw")
    compteur_vivant.pack()

    # lancement du jeu
    jeu(plateau(nombre_case_x, nombre_case_y, "X"), nombre_vivant, nombre_tour)

    # lancement de la fenêtre
    window.mainloop()

