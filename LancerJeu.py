# Importation des librairies
import tkinter as tk
from random import randint
import copy
import time

# Importation des classes des différents modes de jeu
import MenuLibre
import MenuPrincipal


class LancerJeu:
    def __init__(self, nbr_vivant, nbr_tour, mode, grille):

        # CHANGER ICI LA VITESSE SELON LE SYSTEME D'EXPLOITATION (Windows = 0, Linux = 0.05 ou 0.01)
        self.vitesse = 0


        # Création de la fenêtre
        self.mode = mode  # Mode libre ou aléatoire
        self.grille = grille  # Grille de jeu permettant de garder la grille de départ en revenant au mode libre
        self.racine = tk.Tk()
        self.racine.title("Jeu de la vie")
        self.racine.geometry("1280x720")
        icone = tk.PhotoImage(file="icon.png")
        self.racine.iconphoto(True, icone)
        self.racine.resizable(0, 0)
        self.racine.config(background="#141418")
        self.racine.attributes("-fullscreen", False)

        # Configuration des touches
        self.racine.bind_all("<Key-Escape>", self.echap)
        self.racine.bind_all("<Key-F11>", self.fullscreen)
        self.racine.bind_all("<Key-Return>", self.restart)

        # variables globales
        self.nombre_vivant = nbr_vivant
        self.nombre_tour = nbr_tour
        self.nombre_case_y = 30
        self.taille_case = 19
        self.nombre_case_x = int(self.nombre_case_y * 2) - 1
        self.is_fullscreen = False
        self.frame_grille = tk.Frame(self.racine, bd=3, bg="white")
        self.cellule = []
        self.seconde = 0
        
        
        # Appel des différentes fonctions
        self.plateau_GUI()
        self.creer_widgets()
        self.timer()
        self.lancer_jeu()

    def creer_widgets(self):
        """
        def: Création et placement des différents widgets sur la fenêtre
        in: None
        out: None
        """

        # Bannière supérieure
        self.frame_top = tk.Frame(
            self.racine,
            borderwidth=2,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=6)

        # Affichage de la enième génération
        self.generation = tk.Label(
            self.frame_top,
            text="1e tour",
            font=("System", 35),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.generation.place(relx=0.99, rely=0, anchor="ne")

        # Affichage le timer
        self.text_timer = tk.Label(
            self.frame_top,
            text="00:00",
            font=("System", 35),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.text_timer.place(relx=0.01, rely=0, anchor="nw")

        # Affichage du nombre de cellules vivantes sur le nombre total de cellules
        self.compteur_vivant = tk.Label(
            self.frame_top,
            text=str(self.nombre_vivant)
            + "/"
            + str(self.nombre_case_x * self.nombre_case_y),
            font=("System", 35),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.compteur_vivant.pack()

        # Bannière inférieure de rappel des touches
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
            text="F11 : Activer/Désactiver plein écran                 Entrée : Relancer le jeu               Echap : Revenir au menu principal",
            font=("System", 15),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.rappel_touches.pack()

        # place la grille au centre de la fenêtre
        self.racine.update()
        self.frame_grille.place(
            x=self.racine.winfo_width() / 2
            - self.nombre_case_x * self.taille_case / 2,
            y=(self.racine.winfo_height() / 2 + 12)
            - self.nombre_case_y * self.taille_case / 2,
        )

    def echap(self, event):
        """
        def: sur appui de la touche "échap", retourne au menu principal ou au menu libre
        in: None
        out: None
        """
        if event.keysym == "Escape":
            if self.mode == "Libre":
                self.racine.destroy()
                # Lancement du menu libre
                menu_principal = MenuLibre.MenuLibre(
                    self.nombre_vivant, self.nombre_tour, self.grille
                )
                menu_principal.racine.mainloop()

            elif self.mode == "Aleatoire":
                self.racine.destroy()
                # Lancement du menu principal
                menu_principal = MenuPrincipal.MenuPrincipal(
                    self.nombre_vivant, self.nombre_tour
                )
                menu_principal.racine.mainloop()

    def fullscreen(self, event):
        """
        def: sur appui de la touche "F11" active/désactive le plein écran
        in: None
        out: None
        """
        if event.keysym == "F11":
            if self.is_fullscreen == True:
                for lignes in range(self.nombre_case_y):
                    for colonnes in range(self.nombre_case_x):
                        self.cellule[lignes][colonnes].config(height="19", width="19")
                        self.taille_case = 19

                self.is_fullscreen = False
                self.racine.attributes("-fullscreen", False)
            else:
                for lignes in range(self.nombre_case_y):
                    for colonnes in range(self.nombre_case_x):
                        self.cellule[lignes][colonnes].config(height="30", width="30")
                        self.taille_case = 30

                self.racine.attributes("-fullscreen", True)
                self.is_fullscreen = True
    

    def timer(self):
        """
        def: actualise le timer toutes les secondes
        in: None
        out: None
        """
        
        self.start_time = time.time()
        
    def restart(self, event):
        """
        def: sur appui de la touche "entrée", relance le jeu de la vie
        in: None
        out: None
        """
        # reset le timer
        self.start_time = time.time()

        if event.keysym == "Return":
            self.jeu(
                self.plateau(self.nombre_case_x, self.nombre_case_y, "X"),
                self.nombre_vivant,
                self.nombre_tour,
            )

        
    def plateau_GUI(self):
        """
        def: Crée le plateau de jeu du GUI sous la forme d'une grille de canva
        in: None
        out: None
        """
        for i in range(self.nombre_case_y):
            # crée une liste de canvas pour pouvoir modifier chaque case de la grille indépendamment
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
            self.cellule.append(liste)
        

    def plateau(self, x, y, charactere):
        """
        def: crée le plateau console sous la forme d'une liste 2D ou 'X' est une cellule morte et 'O' une cellule vivante
        in:
            x : le nombre de cellules sur x
            y : le nombre de cellules sur y
            charactere : le charactere qui remplira la liste 2D
        out:
            plateau : la liste 2D de taille {x}*{y} remplie de {charactere}
        """
        plateau = []
        for i in range(y):
            lignes = []
            for j in range(x):
                lignes.append(charactere)
            plateau.append(lignes)
        return plateau

    def cellule_autour(self, grille, ligne, colonne):
        """
        def: Retourne le nombre de cellules vivantes parmi les 8 cellules entourant la cellule de coordonnées sur la {ligne}eme ligne et la {colonne}eme colonne
        in:
            grille : la liste 2D à étudier
            ligne : la ligne de la cellule à étudier
            colonne : la colonne de la cellule à étudier
        out:
            cellule_vivante : nombre de cellule(s) vivante(s) autour de la cellule étudiée
        """
        cellule_vivante = 0
        cellule_morte = 0
        for i in range(max(ligne - 1, 0), min(ligne + 2, len(grille))):
            for j in range(max(colonne - 1, 0), min(colonne + 2, len(grille[0]))):
                if i == ligne and j == colonne:
                    continue
                if grille[i][j] == "X":
                    cellule_morte += 1
                else:
                    cellule_vivante += 1
        return cellule_vivante

    def jeu(self, grille, nbr_vivant, tour):
        """
        def: Lance le jeu
        in:
            grille : la grille de jeu
            nbr_vivant : le nombre initial de cellules vivantes
            tour : le nombre maximum d'itérations de l'algorithme
        out: None
        """
        if self.mode == "Aleatoire":
            # place les cellules vivantes dans le plateau console et le plateau GUI de manière aléatoire
            for vivant in range(nbr_vivant):
                ligne = randint(0, len(grille) - 1)
                colonne = randint(0, len(grille[0]) - 1)
                if len(grille) * len(grille[0]) < nbr_vivant:
                    for cellule1 in range(len(grille)):
                        for cellule2 in range(len(grille[0])):
                            grille[cellule1][cellule2] = "O"
                            self.cellule[cellule1][cellule2].config(bg="white")
                else:
                    while grille[ligne][colonne] == "O":
                        ligne = randint(0, len(grille) - 1)
                        colonne = randint(0, len(grille[0]) - 1)
                    grille[ligne][colonne] = "O"
                    self.cellule[ligne][colonne].config(bg="white")

        if self.mode == "Libre":
            # place les cellules vivantes dans le plateau console et le plateau GUI selon la grille initiale
            liste = list(self.grille.values())[0]
            for ligne in range(len(liste)):
                for colonne in range(len(liste[0])):
                    if liste[ligne][colonne] == "O":
                        grille[ligne][colonne] = "O"
                        self.cellule[ligne][colonne].config(bg="white")

        # lance le jeu de la vie pendant {tour} tours
        for i in range(tour + 1):
            vivant = 0

            elapsed_time = int(time.time() - self.start_time) + self.seconde
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            time_string = "{:02d}:{:02d}".format(minutes, seconds)
            self.text_timer.configure(text=time_string)

            # Création d'une grille temporaire pour parcourir la grille initiale sans la modifier
            grille_temp = copy.deepcopy(grille)

            # Parcourt toutes les cellules
            for ligne in range(len(grille)):
                for colonne in range(len(grille[0])):

                    # Incrémentation du compteur de cellules vivantes
                    if grille[ligne][colonne] == "O":
                        vivant += 1

                    # Application des règles du jeu de la vie sur la grille GUI et la grille console
                    cellules_autour = self.cellule_autour(grille, ligne, colonne)
                    if cellules_autour == 3:
                        grille_temp[ligne][colonne] = "O"
                        bg = "white"
                    elif cellules_autour == 2:
                        grille_temp[ligne][colonne] = grille[ligne][colonne]
                        bg = "black" if grille[ligne][colonne] == "X" else "white"
                    else:
                        grille_temp[ligne][colonne] = "X"
                        bg = "black"

                    # Changement de couleur de la cellule sur le GUI
                    self.cellule[ligne][colonne].config(bg=bg)

            time.sleep(self.vitesse)

            # affichages du nombre de tours effectués
            gene = str(i) + "e tour"
            self.generation.config(text=gene)

            # affichaque du compteur de cellules vivantes
            self.compteur_vivant.config(
                text=str(vivant) + "/" + str(self.nombre_case_x * self.nombre_case_y)
            )

            # mise à jour de la grille initale par la grille temporaire maintenant remplie
            grille = copy.deepcopy(grille_temp)

            # mise à jour de la fenêtre
            self.racine.update()

            

    def lancer_jeu(self):
        self.jeu(
            self.plateau(self.nombre_case_x, self.nombre_case_y, "X"),
            self.nombre_vivant,
            self.nombre_tour,
        )
