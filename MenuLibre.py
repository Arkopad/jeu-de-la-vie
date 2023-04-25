import tkinter as tk
import MenuPrincipal
import LancerJeu
from tkinter import filedialog
from tkinter import messagebox
import csv
import os


class MenuLibre:
    def __init__(self, nbr_vivant, nbr_tour, grille):
        self.grille = grille
        self.racine = tk.Tk()
        self.racine.title("Jeu de la vie - Mode Libre")
        self.racine.geometry("1280x720")
        icone = tk.PhotoImage(file="icon.png")
        self.racine.iconphoto(True, icone)
        self.racine.resizable(0, 0)
        self.racine.config(background="#141418")

        # Configuration des touches
        self.racine.bind_all("<Key-Escape>", self.echap)
        self.racine.bind_all("<Key-F1>", self.sauvegarder_fichier)
        self.racine.bind_all("<Key-F2>", self.charger_fichier)
        self.racine.bind_all("<Key-Return>", self.lancer_jeu)
        self.racine.bind_all("<Key-BackSpace>", self.reset)

        # variables globales
        self.nombre_vivant = nbr_vivant
        self.nombre_tour = nbr_tour
        self.nom_fichier = "Aucun fichier chargé"
        self.compteur_nbr_vivant = 0

        self.nombre_case_y = 30
        self.taille_case = 19
        self.nombre_case_x = int(self.nombre_case_y * 2) - 1
        self.is_fullscreen = False
        self.vitesse = 0.001
        self.frame_grille = tk.Frame(self.racine, bd=3, bg="white")
        self.cellule = []

        # Appel des différentes fonctions
        self.plateau_GUI()
        self.creer_widgets()
        

    def creer_widgets(self):
        self.frame_top = tk.Frame(
            self.racine,
            borderwidth=2,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=6)

        self.compteur_vivant = tk.Label(
            self.frame_top,
            text=str(self.compteur_nbr_vivant)
            + "/"
            + str(self.nombre_case_x * self.nombre_case_y),
            font=("System", 35),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.compteur_vivant.pack()

        self.nom = tk.Label(
            self.frame_top,
            text=self.nom_fichier,
            font=("System", 30),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.nom.place(relx=0.99, rely=0, anchor="ne")

        # Bannière rappel des touches
        self.frame_bot = tk.Frame(
            self.racine,
            borderwidth=2,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_bot.pack(fill=tk.X, pady=6, side=tk.BOTTOM)

        self.rappel_touches = tk.Label(
            self.frame_bot,
            text="Retour arrière : Effacer la grille                Entrée : Lancer le jeu               F1 : Sauvegarder la grille                 F2 : Charger une grille               Echap : Revenir au menu principal",
            font=("System", 15),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.rappel_touches.pack()


    def echap(self, event):
        """
        def: sur appui de la touche "échap", quitte la fenêtre
        in:
        out:
        """
        if event.keysym == "Escape":
            self.racine.destroy()
            menu_principal = MenuPrincipal.MenuPrincipal(
                self.nombre_vivant, self.nombre_tour
            )
            menu_principal.racine.mainloop()

    def reset(self, event):
        """
        def: sur appui de la touche "backspace", reset la grille
        in:
        out:
        """
        if event.keysym == "BackSpace":
            reponse = messagebox.askquestion(
                "Attention", "Êtes-vous sûr de vouloir effacer la grille ?"
            )
            if reponse == "yes":
                self.grille = {}
                self.compteur_nbr_vivant = 0
                self.compteur_vivant.config(
                    text=str(self.compteur_nbr_vivant)
                    + "/"
                    + str(self.nombre_case_x * self.nombre_case_y)
                )
                for i in range(self.nombre_case_y):
                    for j in range(self.nombre_case_x):
                        self.cellule[i][j].config(bg="black")

    def lancer_jeu(self, event):
        """
        def: sur appui de la touche "entrée", lance le jeu avec la grille actuelle
        in:
        out:
        """
        if event.keysym == "Return":
            self.grille = {}
            grille = []
            for i in range(self.nombre_case_y):
                ligne = []
                for j in range(self.nombre_case_x):
                    if self.cellule[i][j].cget("background") == "white":
                        ligne.append("O")
                    else:
                        ligne.append("X")
                grille.append(ligne)
            self.grille[self.nom_fichier] = grille

            self.racine.destroy()
            jeu = LancerJeu.LancerJeu(
                self.nombre_vivant, self.nombre_tour, "Libre", self.grille
            )
            jeu.racine.mainloop()

    def plateau_GUI(self):
        """
        def: Crée le plateau de jeu du GUI sous la forme d'une grille de canva
        in: None
        out: None
        """
        for i in range(
            self.nombre_case_y
        ):  # crée une liste de canvas pour pouvoir modifier chaque case de la grille indépendamment
            liste = []
            for j in range(self.nombre_case_x):
                canva = tk.Canvas(
                    self.frame_grille,
                    bg="black",
                    bd=0,
                    height=19,
                    width=19,
                    highlightthickness=0,
                )
                canva.grid(row=i, column=j)
                liste.append(canva)
                canva.bind("<Button-1>", self.change_couleur)
            self.cellule.append(liste)      

        if self.grille != {}:
            liste = list(self.grille.values())[0]
            for ligne in range(len(liste)):
                for colonne in range(len(liste[0])):
                    if liste[ligne][colonne] == "O":
                        self.cellule[ligne][colonne].config(bg="white")
                        self.compteur_nbr_vivant += 1
        
        
        self.racine.update()
        self.frame_grille.place(
            x=self.racine.winfo_width() / 2
            - self.nombre_case_x * self.taille_case / 2,
            y=(self.racine.winfo_height() / 2 + 12)
            - self.nombre_case_y * self.taille_case / 2,
        )

    def change_couleur(self, event):
        canva = event.widget
        if canva.cget("background") == "black":
            canva.config(bg="white")
            self.compteur_nbr_vivant += 1
            self.compteur_vivant.config(
                text=str(self.compteur_nbr_vivant)
                + "/"
                + str(self.nombre_case_x * self.nombre_case_y)
            )
        else:
            canva.config(bg="black")
            self.compteur_nbr_vivant -= 1
            self.compteur_vivant.config(
                text=str(self.compteur_nbr_vivant)
                + "/"
                + str(self.nombre_case_x * self.nombre_case_y)
            )

    def sauvegarder_fichier(self, event):
        if event.keysym == "F1":
            # Transformme la grille GUI en liste 2D avec des 'X' et des 'O'
            grille = []
            for ligne in range(len(self.cellule)):
                grille.append([])
                for colonne in range(len(self.cellule[0])):
                    if self.cellule[ligne][colonne].cget("background") == "black":
                        grille[ligne].append("X")
                    else:
                        grille[ligne].append("O")

            # Sauvegarde la grille dans un fichier csv nommé par l'utilisateur
            file_path = filedialog.asksaveasfilename(
                filetypes=[("Fichiers CSV", "*.csv")], defaultextension=".csv"
            )
            if file_path:
                self.nom_fichier = os.path.basename(file_path)[:-4]
                if len(self.nom_fichier) > 20:
                    self.nom_fichier = self.nom_fichier[:20] + "..."
                with open(file_path, "w", newline="") as f:
                    fichier = csv.writer(f)
                    for ligne in range(len(grille)):
                        fichier.writerow(grille[ligne])
            self.nom.config(text=self.nom_fichier)

    def charger_fichier(self, event):
        if event.keysym == "F2":

            # Lis le fichier csv et le transforme en une liste 2D
            grille = []
            file_path = filedialog.askopenfilename(
                filetypes=[("Fichiers CSV", "*.csv")]
            )
            if file_path:
                self.nom_fichier = os.path.basename(file_path)[:-4]
                if len(self.nom_fichier) > 20:
                    self.nom_fichier = self.nom_fichier[:20] + "..."
                with open(file_path, "r", newline="") as f:
                    fichier = csv.reader(f)
                    for row in fichier:
                        grille.append(row)

            # Mets a jour la grille de canva selon la liste 2D
            self.compteur_nbr_vivant = 0
            for ligne in range(len(grille)):
                for colonne in range(len(grille[0])):
                    if grille[ligne][colonne] == "X":
                        self.cellule[ligne][colonne].config(bg="black")
                    else:
                        self.cellule[ligne][colonne].config(bg="white")
                        self.compteur_nbr_vivant += 1
            self.compteur_vivant.config(
                text=str(self.compteur_nbr_vivant)
                + "/"
                + str(self.nombre_case_x * self.nombre_case_y)
            )

            self.nom.config(text=self.nom_fichier)
