# import des librairies
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import csv
import os

# import des classes
import MenuPrincipal
import LancerJeu


class MenuLibre:
    def __init__(self, nbr_vivant, nbr_cases, grille):
        # Création de la fenêtre
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
        self.racine.bind_all("<Control-s>", self.sauvegarder_fichier)
        self.racine.bind_all("<Key-F2>", self.charger_fichier)
        self.racine.bind_all("<Control-l>", self.charger_fichier)
        self.racine.bind_all("<Key-Return>", self.lancer_jeu)
        self.racine.bind_all("<Key-BackSpace>", self.reset)
        self.racine.bind_all("<Key-F3>", self.affiche_touches)
        self.racine.bind_all("<Control-t>", self.affiche_touches)
        self.racine.bind_all("<Key-F4>", self.changer_taille_grille)
        self.racine.bind_all("<Control-g>", self.changer_taille_grille)

        # variables globales
        self.grille = grille
        self.parametre = None
        self.nombre_vivant = nbr_vivant
        self.nom_fichier = "No File"
        self.compteur_nbr_vivant = 0
        self.nombre_case_y = nbr_cases
        self.nombre_case_x = int(self.nombre_case_y * 2) - 1
        self.is_fullscreen = False
        self.frame_grille = tk.Frame(self.racine, bd=3, bg="white")
        self.cellule = []

        # Appel des différentes fonctions
        self.creer_widgets()
        self.plateau_GUI()

    def creer_widgets(self):
        """
        def: crée et affiche les widgets sur la fenêtre principale
        in: None
        out: None
        """
        # Affichage de la bannière supérieure
        self.frame_top = tk.Frame(
            self.racine,
            borderwidth=2,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=6)

        # Affichage du compteur de cellules vivantes placé au centre de la bannière supérieure
        self.compteur_vivant = tk.Label(
            self.frame_top,
            text=str(self.compteur_nbr_vivant)
            + "/"
            + str(self.nombre_case_x * self.nombre_case_y),
            font=("System", 30),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.compteur_vivant.pack()

        # Affichage du nom du fichier placé à droite de la bannière supérieure
        self.nom = tk.Label(
            self.frame_top,
            text=self.nom_fichier,
            font=("System", 30),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.nom.place(relx=0.99, rely=0, anchor="ne")

        # Affichage la taille de la grille placé à gauche de la bannière supérieure
        self.text_taille = tk.Label(
            self.frame_top,
            text=f"{self.nombre_case_x}x{self.nombre_case_y}",
            font=("System", 30),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.text_taille.place(relx=0.01, rely=0, anchor="nw")

        # Bannière rappel des touches inférieure
        self.frame_bot = tk.Frame(
            self.racine,
            borderwidth=2,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_bot.pack(fill=tk.X, pady=6, side=tk.BOTTOM)

        # Affichage du rappel des touches générales
        self.rappel_touches = tk.Label(
            self.frame_bot,
            text="F3/CTRL+T : Afficher les touches",
            font=("System", 15),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.rappel_touches.pack(padx=10)

        # Affichage de la grille de jeu
        self.racine.update()
        self.racine.update_idletasks()  # permet de mettre à jour la fenêtre (on utilise pas juste update par ce que des fois ca bug pour aucune raison)
        self.racine.after(
            150
        )  # on ajoute un temps de pause pour etre sur que la taille de la fenetre est mise a jour sinon des fois ca bug
        # on calcule la taille des cases en fonction de la taille de la fenetre et du nombre de cases (en pratique le min est toujours sur la hauteur)
        self.taille_case = min(
            (self.racine.winfo_width() - 50) / self.nombre_case_x,
            (
                self.racine.winfo_height()
                - self.frame_top.winfo_height()
                - self.frame_bot.winfo_height()
                - 50
            )
            / self.nombre_case_y,
        )
        self.frame_grille.place(
            x=self.racine.winfo_width() / 2 - self.nombre_case_x * self.taille_case / 2,
            y=(self.racine.winfo_height() / 2 + 12)
            - self.nombre_case_y * self.taille_case / 2,
        )

    def echap(self, event):
        """
        def: sur appui de la touche "échap", quitte la fenêtre et retourne au menu principal
        in:
        out:
        """
        if event.keysym == "Escape":
            self.racine.destroy()
            menu_principal = MenuPrincipal.MenuPrincipal(
                self.nombre_vivant, self.nombre_case_y
            )
            menu_principal.racine.mainloop()

    def affiche_touches(self, event):
        """
        def: sur appui de la touche "F3" ou "control+t", affiche les touches disponibles
        in:
        out:
        """
        if event.keysym == "F3" or event.keysym == "t":
            messagebox.showinfo(
                "Touches",
                " Echap : Revenir au menu principal \n\n F4/CTRL+G : Changer la taille de la grille \n\n F1/CTRL+S : Sauvegarder la grille \n\n F2/CTRL+L : Charger une grille \n\n Entrée : Lancer le jeu \n\n Backspace : Effacer la grille",
            )

    def changer_taille_grille(self, event):
        """
        def: affiche une fenetre permettant de changer la taille de la grille avec un curseur
        in:
        out:
        """
        if event.keysym == "F4" or event.keysym == "g":
            # on controle si la fenetre est deja ouverte, si oui on la ferme
            if self.parametre != None:
                self.parametre.destroy()
            # on ouvre la fenetre
            self.parametre = tk.Toplevel(self.racine, bg="#141418")
            self.parametre.resizable(False, False)
            self.parametre.title("Paramètres")

            # curseur pour choisir le nombre de cases de la grille de jeu
            self.curseur_nbr_cases = tk.Scale(
                self.parametre,
                orient="horizontal",
                from_=10,
                to=100,
                resolution=1,
                tickinterval=90,
                length=350,
                label="Nombre de cases sur y",
                bg="#141418",
                fg="#A5A5B5",
                font="System",
                highlightbackground="#141418",
                troughcolor="#A5A5B5",
                activebackground="#A5A5B5",
            )
            self.curseur_nbr_cases.pack(pady=20, padx=20, expand=True)
            self.curseur_nbr_cases.set(self.nombre_case_y)

            # Bouton valider pour enregistrer les paramètres et changer l'affichage
            self.valider = tk.Button(
                self.parametre,
                text="Valider",
                bg="#010D19",
                fg="#A5A5B5",
                font=("System", 15),
                command=self.enregistre_parametre,
            )
            self.valider.pack(pady=20, expand=True)

    def enregistre_parametre(self):
        """
        def: sur appui du bouton "valider", affiche un message de confirmation et change la taille de la grille en recréant la fenetre
        in: None
        out: None
        """
        reponse = messagebox.askquestion(
            "Attention",
            "Attention, changer la taille de la grille efface le contenu, êtes-vous sûr de vouloir continuer ?",
        )
        if reponse == "yes":
            self.nbr_cases = self.curseur_nbr_cases.get()
            self.parametre.destroy()
            self.racine.destroy()
            libre = MenuLibre(self.nombre_vivant, self.nbr_cases, {})
            libre.racine.mainloop()

    def reset(self, event):
        """
        def: sur appui de la touche "backspace", reset la grille après un message de confirmation
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
                self.nombre_vivant, self.nombre_case_y, "Libre", self.grille
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
                    height=self.taille_case,
                    width=self.taille_case,
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

    def change_couleur(self, event):
        """
        def: change la couleur du canva sur lequel on clique (noir ou blanc) et met à jour le compteur de cellules vivantes
        in: None
        out: None
        """
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
        """
        def: sur appui de la touche "F1" ou "CTRL+S", sauvegarde la grille dans un fichier csv nommé par l'utilisateur en convertissant la grille GUI en liste 2D
        in:
        out:
        """
        if event.keysym == "F1" or event.keysym == "s":
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
                filetypes=[("Fichiers CSV", "*.csv")],
                defaultextension=f"_{self.nombre_case_x}x{self.nombre_case_y}.csv",
            )
            if file_path:
                self.nom_fichier = os.path.basename(file_path)[:-4]
                if len(self.nom_fichier) > 20:
                    self.nom_fichier = self.nom_fichier[:16] + "..."
                with open(file_path, "w", newline="") as f:
                    fichier = csv.writer(f)
                    for ligne in range(len(grille)):
                        fichier.writerow(grille[ligne])
            self.nom.config(text=self.nom_fichier)

    def charger_fichier(self, event):
        """
        def: sur appui de la touche "F2" ou "CTRL+L", charge un fichier csv et le transforme en une liste 2D pour afficher la grille dans le GUI
        in:
        out:
        """
        if event.keysym == "F2" or event.keysym == "l":
            # Lis le fichier csv et le transforme en une liste 2D
            grille = []
            file_path = filedialog.askopenfilename(
                filetypes=[("Fichiers CSV", "*.csv")]
            )
            if file_path:
                self.nom_fichier = os.path.basename(file_path)[:-4]
                if len(self.nom_fichier) > 20:
                    self.nom_fichier = self.nom_fichier[:16] + "..."
                with open(file_path, "r", newline="") as f:
                    fichier = csv.reader(f)

                    for row in fichier:
                        grille.append(row)

                    # Si la grille est trop grande, on affiche un message d'erreur
                    if len(grille) > self.nombre_case_y:
                        messagebox.showerror(
                            "Erreur",
                            "La grille est trop grande pour la fenêtre actuelle, veuillez changez la taille dans les paramètres",
                        )
                        return

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
