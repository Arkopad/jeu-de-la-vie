import tkinter as tk 
from Affichage import Affichage
from tkinter import messagebox
import numpy as np

class jeu_de_la_vie(Affichage):
    def __init__(self):
        #Attributs principaux
        self.colonne = 6
        self.ligne = 6
        self.nb_cellues = self.colonne * self.ligne

        #Initialisation de la fenetre
        super().__init__(nom=f"Jeu de la vie! (en {self.ligne}x{self.colonne})", geometry=(500,500), nb_cellues=self.nb_cellues, dimensions=(self.ligne, self.colonne))
        self.width = self.racine.winfo_width()
        self.height = self.racine.winfo_height()

        #Commande Affichage:

        #Attributs secondaires:
        self.mode_edition = True

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
        self.titre = tk.Label(self.racine, text=f"Jeu de la vie! (en {self.ligne}x{self.colonne})", font=self.police_titre(), background="#141418", foreground="white")
        self.titre.pack(anchor="n", fill='x')
        
        # Création d'un cadre pour les boutons
        self.buttons_frame = tk.Frame(self.racine)
        self.buttons_frame.pack(side="bottom")

        self.police_edition = lambda : ("Comic sans Ms", int(float((self.width+self.height)/2)/40), "bold") #Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.bouton_edition = tk.Button(master=self.buttons_frame, text="Mode edition activé", font=self.police_edition(), background="#141418", foreground="white", command=self.edition)
        self.bouton_edition.pack(side="left")

        self.police_clear = lambda : ("Comic sans Ms", int(float((self.width+self.height)/2)/40), "bold") #Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.bouton_clear = tk.Button(master=self.buttons_frame, text="Clear", font=self.police_clear(), background="#141418", foreground="white", command=self.clear)
        self.bouton_clear.pack(side="left")

        self.police_quitter = lambda : ("Comic sans Ms", int(float((self.width+self.height)/2)/40), "bold") #Valeur d'actualisation du label du bouton en fonction de la taille de la fenetre
        self.quitter = tk.Button(master=self.buttons_frame, text="Quitter", font=self.police_quitter(), background="#9E1C00", foreground="white", command=self.exit)
        self.quitter.pack(side="left", fill='x')

        self.actualisation(self.titre, self.police_titre)
        self.actualisation(self.bouton_edition, self.police_edition)
        self.actualisation(self.bouton_clear, self.police_clear)

        

    def edition(self):
        """
        Activer/desactiver le mode edition
        in: None
        out: None
        """
        if self.mode_edition:
            self.mode_edition = False
            self.bouton_edition.configure(text="Mode jeu activé")
            self.temps = 0
            self.jeu()
        else:
            self.mode_edition = True
            self.bouton_edition.configure(text="Mode édition activé")
       

    def change_couleur(self, event):
        """
        Fonction permettant de changer la couleur du canvas sur lequel on clique
        in: event (evenement de la souris)
        out: None
        """
        if self.mode_edition:
            canvas = event.widget
            if canvas.cget("background") == "#141418":
                canvas.configure(background="white")
            else:
                canvas.configure(background="#141418")
        else:
            messagebox.showerror("Erreur", "Vous devez activer le mode edition pour pouvoir modifier la grille")

    def jeu_de_la_vie(self, grille):
        """
        Fonction permettant de calculer le jeu de la vie à l'instant t+1 depuis l'instant t.
        in: grille (tableau NumPy avec 0 et 1)
        out: grille_suivante (tableau NumPy avec 0 et 1)
        """
        
        # Initialiser la grille suivante avec des zéros
        grille_suivante = np.array([[0 for j in range(self.colonne)] for i in range(self.ligne)])
        # Parcourir chaque cellule de la grille
        for i in range(self.ligne):
            for j in range(self.colonne):
                # Calculer le nombre de voisins vivants
                nb_voisins = 0
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if k >= 0 and k < self.ligne and l >= 0 and l < self.colonne and (k != i or l != j):
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

    def jeu(self):
        """
        Fonction permettant de lancer le jeu de la vie
        in: None
        out: None
        """
        if not self.mode_edition:
            print(f"Temps du jeu={self.temps}")
            # Initialiser la grille avec des zéros
            grille = np.array([[0 for j in range(self.colonne)] for i in range(self.ligne)])
            # Parcourir chaque cellule de la grille
            for i in range(self.ligne):
                for j in range(self.colonne):
                    if self.canvases[i][j].cget("background") == "white":
                        grille[i][j] = 1
            # Calculer la grille suivante
            grille_suivante = self.jeu_de_la_vie(grille)
            # Parcourir chaque cellule de la grille
            for i in range(self.ligne):
                for j in range(self.colonne):
                    if grille_suivante[i][j] == 1:
                        self.canvases[i][j].configure(background="white")
                    else:
                        self.canvases[i][j].configure(background="#141418")
            self.racine.after(1000, self.jeu)
            self.temps += 1
    
    def clear(self):
        """
        Fonction permettant de clear la grille
        in: None
        out: None
        """
        for i in range(self.ligne):
            for j in range(self.colonne):
                self.canvases[i][j].configure(background="#141418")

    def exit(self):
        """
        Fonction permettant de quitter le programme
        in: None
        out: None
        """
        self.racine.destroy()


if __name__ == '__main__':
    GameOfLife = jeu_de_la_vie()
    GameOfLife.racine.mainloop()