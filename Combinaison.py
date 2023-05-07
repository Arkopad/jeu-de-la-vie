import tkinter as tk
from Affichage import Affichage
import MenuPrincipal
import numpy as np
import time
from tkinter import messagebox
from tqdm import tqdm
from numba import njit, prange


"""
=======================================================================================================================
====================================================FONCTIONS NUMBA====================================================
=======================================================================================================================
"""


@njit()
def jeu_de_la_vie(nb_lignes, nb_colonnes, grille):
    """
    Fonction permettant de calculer le jeu de la vie à l'instant t+1 depuis l'instant t.
    in: grille (tableau NumPy avec 0 et 1)
    out: grille_suivante (tableau NumPy avec 0 et 1)
    """

    # Initialiser la grille suivante avec des zéros
    grille_suivante = np.array(
        [[0 for j in range(nb_colonnes)] for i in range(nb_lignes)]
    )
    # Parcourir chaque cellule de la grille
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            # Calculer le nombre de voisins vivants
            nb_voisins = 0
            for k in range(max(i - 1, 0), min(i + 2, nb_lignes)):
                for l in range(max(j - 1, 0), min(j + 2, nb_colonnes)):
                    if (
                        k >= 0
                        and k < nb_lignes
                        and l >= 0
                        and l < nb_colonnes
                        and (k != i or l != j)
                    ):
                        nb_voisins += grille[k][l]
            # Appliquer les règles du jeu de la vie
            if grille[i][j] == 1:
                if nb_voisins < 2 or nb_voisins > 3:
                    grille_suivante[i][j] = 0
                else:
                    grille_suivante[i][j] = 1
            else:
                if nb_voisins == 3:
                    grille_suivante[i][j] = 1
                else:
                    grille_suivante[i][j] = 0

    return grille_suivante


@njit
def combinaison_numba(nb_lignes, nb_colonnes, nb_cellules):
    # Initialisation de variables utiles:
    total = 2**nb_cellules
    intervalle = total // 100  # pour l'affichage de l'avancée

    # Nombre de combinaisons stables
    nb_combinaisons_stables = 0

    # Initialisation de la liste des combinaisons
    combinaisons = []

    # Calcul de toutes les combinaisons
    combinaison_actuelle = np.zeros((nb_lignes, nb_colonnes), dtype=np.int64)
    for bin in range(total):
        # Affichage de l'avancée
        if bin % intervalle == 0:
            progress = bin * 100 / total
            progress_str = round(progress, 1)
            print("Progression : ", progress_str, "%")

        # Calcul de la combinaison
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                combinaison_actuelle[i, j] = (bin >> (i * nb_lignes + j)) & 1

        # Calcul de la grille suivante
        grille_suivante = jeu_de_la_vie(nb_lignes, nb_colonnes, combinaison_actuelle)

        # Vérification de la stabilité de la combinaison
        if np.array_equal(grille_suivante, combinaison_actuelle):
            nb_combinaisons_stables += 1
            combinaisons.append(grille_suivante)

    return combinaisons, nb_combinaisons_stables


"""
=======================================================================================================================
======================================================COMBINAISON======================================================
=======================================================================================================================
"""


class Combinaison(Affichage):
    def __init__(self, nbr_cases):
        # Attributs principaux
        self.colonne = nbr_cases
        self.ligne = nbr_cases
        self.nb_cellues = self.colonne * self.ligne
        self.numero_combinaison = 0

        # Initialisation de la fenetre
        super().__init__(
            nom=f"Combinaison {self.ligne}x{self.colonne}",
            geometry=(600, 600),
            nb_cellues=self.nb_cellues,
            dimensions=(self.ligne, self.colonne),
        )
        icone = tk.PhotoImage(file="icon.png")
        self.racine.iconphoto(True, icone)
        self.width = self.racine.winfo_width()
        self.height = self.racine.winfo_height()

        self.racine.bind_all("<Key-Escape>", self.echap)

        # Widgets
        self.widgets()

    def widgets(self):
        """
        Fonction permettant de créer les widgets de la fenetre
        in: None
        out: None
        """

        # Frame du titre du jeu en haut de l'écran
        self.frame_top = tk.Frame(
            self.racine,
            borderwidth=int(float(self.width + self.height) / 1000),
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=6)
        self.fram_top_borderwidth = lambda: int(
            float(self.width + self.height) / 1000
        )  # Valeur d'actualisation de la bordure en fonction de la taille de la fenetre
        self.frame_actualisation.append((self.frame_top, self.fram_top_borderwidth))

        # Label du titre du jeu
        self.titre = tk.Label(
            self.frame_top,
            text=f"Combinaison {self.ligne}x{self.colonne}",
            font=("System", int(float((self.width + self.height) / 50))),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.titre.pack(pady=4)
        self.police_generation = lambda: (
            "System",
            int(float((self.width + self.height) / 50)),
        )  # Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.titre, self.police_generation))

        # Définition de la grille
        self.frame = tk.Frame(self.racine, bd=2, bg="#A5A5B5")
        self.frame.place(relx=0.5, rely=0.515, anchor="center")
        for i in range(self.ligne):
            self.frame.grid_rowconfigure(i, weight=1)
            for j in range(self.colonne):
                self.frame.grid_columnconfigure(j, weight=1)
                canvas = tk.Canvas(
                    self.frame,
                    width=self.taille_cellule,
                    height=self.taille_cellule,
                    bg="black",
                    bd=2,
                    highlightthickness=2,
                    highlightbackground="#A5A5B5",
                )
                canvas.grid(row=i, column=j, sticky="nsew")
                canvas.bind("<Button-1>", self.change_couleur)
                self.canvases[i][j] = canvas

        # Création d'un cadre pour les boutons
        self.buttons_frame = tk.Frame(self.racine)
        self.buttons_frame.pack(side="bottom")

        self.police_calcul = lambda: (
            "Comic sans Ms",
            int(float((self.width + self.height) / 2) / 40),
            "bold",
        )  # Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.bouton_calcul = tk.Button(
            master=self.buttons_frame,
            text="Calculer",
            font=self.police_calcul(),
            background="#141418",
            foreground="white",
            command=self.calcul_combinaison,
        )
        self.bouton_calcul.pack(side="left", fill="x")

        self.police_affichage = lambda: (
            "Comic sans Ms",
            int(float((self.width + self.height) / 2) / 40),
            "bold",
        )  # Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.bouton_afficage = tk.Button(
            master=self.buttons_frame,
            text="Afficher",
            font=self.police_calcul(),
            background="#141418",
            foreground="white",
            command=self.affichage_combinaison,
        )
        self.bouton_afficage.pack(side="left", fill="x")

        self.police_fast = lambda: (
            "Comic sans Ms",
            int(float((self.width + self.height) / 2) / 40),
            "bold",
        )  # Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.fast = tk.Button(
            master=self.buttons_frame,
            text="FASTER",
            font=self.police_fast(),
            background="#ab3fff",
            foreground="white",
            command=self.fast,
        )
        self.fast.pack(side="left", fill="x")

        self.actualisation(self.bouton_calcul, self.police_calcul)
        self.actualisation(self.bouton_afficage, self.police_affichage)
        self.actualisation(self.fast, self.police_fast)

    def change_couleur(self, event):
        """
        Fonction permettant de changer la couleur du canvas sur lequel on a cliqué
        in: event
        out: None
        """
        canvas = event.widget
        if canvas.cget("background") == "black":
            canvas.config(background="white")
        else:
            canvas.config(background="black")

    def calcul_combinaison(self):
        # Initialisation de variables utiles:
        total = 2**self.nb_cellues

        # Nombre de combinaisons stables
        self.nb_combinaisons_stables = 0

        # Initialisation de la liste des combinaisons
        self.combinaisons = []

        # Calcul de toutes les combinaisons
        combinaison_actuelle = np.zeros((self.ligne, self.colonne), dtype=np.int64)
        for bin in tqdm(range(total)):
            # Calcul de la combinaison
            for i in range(self.ligne):
                for j in range(self.colonne):
                    combinaison_actuelle[i, j] = (bin >> (i * self.ligne + j)) & 1

            # Calcul de la grille suivante
            grille_suivante = jeu_de_la_vie(
                self.ligne, self.colonne, combinaison_actuelle
            )

            # Vérification de la stabilité de la combinaison
            if np.array_equal(grille_suivante, combinaison_actuelle):
                self.nb_combinaisons_stables += 1
                self.combinaisons.append(grille_suivante)

    def fast(self):
        """
        Fonction permettant de calculer toutes les combinaisons possibles d'une grille avec le jeu de la vie en force brute
        in: event
        out: None
        """
        start_time = time.time()
        self.combinaisons, self.nb_combinaisons_stables = combinaison_numba(
            self.ligne, self.colonne, self.nb_cellues
        )
        print("Temps écoulé:", time.time() - start_time)
        messagebox.showinfo(
            "Nombres de combinaisons stables.",
            f"Nombre de combinaisons stables: {self.nb_combinaisons_stables-1}",
        )

        # permet de faire défiler les combinaisons avec touches gauches et droite
        self.racine.bind_all("<Right>", self.defilement_droit)
        self.racine.bind_all("<Left>", self.defilement_gauche)

    def affichage_combinaison(self):
        """
        Fonction permettant d'afficher toutes les combinaisons
        in: None
        out: None
        """
        for i in range(self.nb_combinaisons_stables):
            for j in range(len(self.combinaisons[i])):
                for k in range(len(self.combinaisons[i][j])):
                    if self.combinaisons[i][j][k] == 1:
                        self.canvases[j][k].config(background="white")
                    else:
                        self.canvases[j][k].config(background="black")
            self.racine.update()
            self.racine.after(50)
            self.racine.update()

    def defilement_droit(self, event):
        """
        Fonction permettant de faire défiler les combinaisons avec la touche droite
        """
        # on utilise le modulo pour éviter de dépasser le nombre de combinaisons
        self.numero_combinaison = (
            self.numero_combinaison + 1
        ) % self.nb_combinaisons_stables

        for j in range(len(self.combinaisons[self.numero_combinaison])):
            for k in range(len(self.combinaisons[self.numero_combinaison][j])):
                if self.combinaisons[self.numero_combinaison][j][k] == 1:
                    self.canvases[j][k].config(background="white")
                else:
                    self.canvases[j][k].config(background="black")
        self.racine.update()

    def defilement_gauche(self, event):
        """
        Fonction permettant de faire défiler les combinaisons avec la touche gauche
        """
        # on utilise le modulo pour éviter de dépasser le nombre de combinaisons
        self.numero_combinaison = (
            self.numero_combinaison - 1
        ) % self.nb_combinaisons_stables

        for j in range(len(self.combinaisons[self.numero_combinaison])):
            for k in range(len(self.combinaisons[self.numero_combinaison][j])):
                if self.combinaisons[self.numero_combinaison][j][k] == 1:
                    self.canvases[j][k].config(background="white")
                else:
                    self.canvases[j][k].config(background="black")
        self.racine.update()

    def echap(self, event):
        """
        def: sur appui de la touche "échap", retourne au menu principal
        in: None
        out: None
        """
        if event.keysym == "Escape":
            self.racine.destroy()
            # Lancement du menu principal
            menu_principal = MenuPrincipal.MenuPrincipal(1000, 20)
            menu_principal.racine.mainloop()


if __name__ == "__main__":
    combinaison = Combinaison(4)
    combinaison.racine.mainloop()
