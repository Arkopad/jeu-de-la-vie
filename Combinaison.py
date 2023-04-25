import tkinter as tk
from Affichage import Affichage
import numpy as np
import time
from tkinter import messagebox


class Combinaison(Affichage):
    def __init__(self):
        #Attributs principaux
        self.colonne = 3
        self.ligne = 3
        self.nb_cellues = self.colonne * self.ligne

        #Initialisation de la fenetre
        super().__init__(nom=f'Combinaison {self.ligne}x{self.colonne}', geometry=(500,500), nb_cellues=self.nb_cellues, dimensions=(self.ligne, self.colonne))
        self.width = self.racine.winfo_width()
        self.height = self.racine.winfo_height()

        #Widgets
        self.widgets()

    
    def widgets(self):
        """
        Fonction permettant de créer les widgets de la fenetre
        in: None
        out: None
        """

        #Définition de la grille
        self.frame = tk.Frame(self.racine)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        for i in range(self.ligne):
            self.frame.grid_rowconfigure(i, weight=1)
            for j in range(self.colonne):
                self.frame.grid_columnconfigure(j, weight=1)
                canvas = tk.Canvas(self.frame, width=self.taille_cellule, height=self.taille_cellule, background="#141418", bd=1, relief="solid")
                canvas.grid(row=i, column=j, sticky='nsew')
                canvas.bind("<Button-1>", self.change_couleur)
                self.canvases[i][j] = canvas

        self.police_titre = lambda : ("Comic sans Ms", int(float((self.width+self.height)/2)/20), "bold") #Valeur d'actualisation du label en fonction de la taille de la fenetre
        self.titre = tk.Label(self.racine, text="Combinaison 3x3", font=self.police_titre(), background="#141418", foreground="white")
        self.titre.pack(anchor="n", fill='x')
        
        self.police_calcul = lambda : ("Comic sans Ms", int(float((self.width+self.height)/2)/40), "bold") #Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.bouton_calcul = tk.Button(self.racine, text="Calculer", font=self.police_calcul(), background="#141418", foreground="white", command=self.calcul_combinaison)
        self.bouton_calcul.pack(side="bottom", fill='x')

        self.police_affichage = lambda : ("Comic sans Ms", int(float((self.width+self.height)/2)/40), "bold") #Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.bouton_afficage = tk.Button(self.racine, text="Afficher", font=self.police_calcul(), background="#141418", foreground="white", command=self.affichage_combinaison)
        self.bouton_afficage.pack(side="bottom", fill='x')

        self.actualisation(self.titre, self.police_titre)
        self.actualisation(self.bouton_calcul, self.police_calcul)
        self.actualisation(self.bouton_afficage, self.police_affichage)


    def change_couleur(self, event):
        """
        Fonction permettant de changer la couleur du canvas sur lequel on a cliqué
        in: event
        out: None
        """
        canvas = event.widget
        if canvas.cget("background") == "#141418":
            canvas.config(background="white")
        else:
            canvas.config(background="#141418")  
    

    def jeu_de_la_vie(self, grille):
        """
        Fonction permettant de calculer le jeu de la vie à l'instant t+1
        in: grille
        out: grille        
        """
        #Initialisation de la grille
        grille_suivante = np.zeros((self.ligne, self.colonne))

        #Calcul de la grille suivante
        for i in range(self.ligne):
            for j in range(self.colonne):
                #Calcul du nombre de voisins
                nb_voisins = 0
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if k >= 0 and k < self.ligne and l >= 0 and l < self.colonne and (k != i or l != j):
                            nb_voisins += grille[k][l]

                #Calcul de la grille suivante
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

    def calcul_combinaison(self):
        """
        Fonction permettant de calculer toutes les combinaisons possibles d'une grille 3x3 avec le jeu de la vie en force brute
        in: event
        out: None
        """
        #Nombre de combinaisons stables
        self.nb_combinaisons_stable = 0

        #Initialisation de la liste des combinaisons
        self.combinaisons = []

        #Calcul de toutes les combinaisons
        for i in range(2**self.nb_cellues):
            #Calcul de la combinaison
            combinaison = []
            for j in range(self.nb_cellues):
                combinaison.append((i >> j) & 1)
            combinaison = np.array(combinaison).reshape((self.ligne, self.colonne))

            #Calcul de la grille suivante
            grille_suivante = self.jeu_de_la_vie(combinaison)

            #Vérification de la stabilité de la combinaison
            if np.array_equal(grille_suivante, combinaison):
                self.nb_combinaisons_stable += 1
                self.combinaisons.append(combinaison)

        
        messagebox.showinfo("Nombres de combinaisons stables.",f"Nombre de combinaisons stables: {self.nb_combinaisons_stable-1}")

    def affichage_combinaison(self):
        """
        Fonction permettant d'afficher toutes les combinaisons
        in: None
        out: None
        """
        for i in range(len(self.combinaisons)):
            for j in range(len(self.combinaisons[i])):
                for k in range(len(self.combinaisons[i][j])):
                    if self.combinaisons[i][j][k] == 1:
                        self.canvases[j][k].config(background="white")
                    else:
                        self.canvases[j][k].config(background="#141418")
            self.racine.update()
            self.racine.after(500)
            self.racine.update()

        


if __name__ == '__main__':
    combinaison = Combinaison()
    combinaison.racine.mainloop()
