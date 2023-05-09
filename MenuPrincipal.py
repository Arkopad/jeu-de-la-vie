"""
=======================================================================================================================
===================================================FICHIER PRINCIPAL===================================================
=======================================================================================================================
"""

# Importation des librairies
import tkinter as tk
from tkinter import messagebox

# Importation des classes
import MenuLibre
import LancerJeu
from Affichage import Affichage
import CombinaisonSansBords
import CombinaisonAvecBords


class MenuPrincipal(Affichage):
    def __init__(self, nbr_vivant, nbr_cases):
        # Création de la fenêtre principale avec la classe Affichage
        super().__init__(nom=f"Menu Principal", geometry=(1280, 720), nb_cellues=0)
        icone = tk.PhotoImage(file="icon.png")
        self.racine.iconphoto(True, icone)

        # Initialisation des variables
        self.parametre_aleatoire = None
        self.parametre_combinaison = None
        self.nbr_vivant = nbr_vivant
        self.nbr_cases = nbr_cases
        self.liste_police = ("System", "")
        self.bords = tk.IntVar()

        # Affectation des touches
        self.racine.bind_all("<Key-Escape>", self.echap)
        self.racine.bind_all("<Key-F3>", self.affiche_touches)
        self.racine.bind_all("<Control-t>", self.affiche_touches)

        # Création des widgets
        self.creer_widgets()

    def creer_widgets(self):
        """
        def: crée et affiche les widgets sur la fenêtre principale
        """

        # Frame du titre du jeu en haut de l'écran
        self.frame_top = tk.Frame(
            self.racine,
            borderwidth=int(float(self.width + self.height) / 1000),
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=12)
        self.fram_top_borderwidth = lambda: int(
            float(self.width + self.height) / 1000
        )  # Valeur d'actualisation de la bordure en fonction de la taille de la fenetre
        self.frame_actualisation.append((self.frame_top, self.fram_top_borderwidth))

        # Label du titre du jeu
        self.titre = tk.Label(
            self.frame_top,
            text="JEU DE LA VIE",
            font=("system", int(float((self.width + self.height) / 50))),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.titre.pack(pady=4)
        self.police_titre = lambda: (
            "system",
            int(float((self.width + self.height) / 50)),
        )  # Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.titre, self.police_titre))

        # Bannière rappel des touches en bas de l'écran
        self.frame_bot = tk.Frame(
            self.racine,
            borderwidth=int(float(self.width + self.height) / 1000),
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_bot.pack(fill=tk.X, pady=6, side=tk.BOTTOM)
        self.fram_bot_borderwidth = lambda: int(
            float(self.width + self.height) / 1000
        )  # Valeur d'actualisation de la bordure en fonction de la taille de la fenetre
        self.frame_actualisation.append((self.frame_bot, self.fram_bot_borderwidth))

        # Texte rappel des touches
        self.rappel_touches = tk.Label(
            self.frame_bot,
            text="F3/CTRL+T : Afficher les touches",
            font=("System", int(float((self.width + self.height) / 133))),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.rappel_touches.pack()
        self.police_rappel_touches = lambda: (
            "System",
            int(float((self.width + self.height) / 133)),
        )  # Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append(
            (self.rappel_touches, self.police_rappel_touches)
        )

        # Bouton pour accéder au mode libre
        self.libre = tk.Button(
            self.racine,
            text="Mode libre",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", int(float((self.width + self.height) / 50))),
            command=self.mode_libre,
        )
        self.libre.pack(ipady=6, expand=True)
        self.taille_libre = lambda: (
            "System",
            int(float((self.width + self.height) / 50)),
        )  # Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.libre, self.taille_libre))

        # Bouton pour accéder au mode aléatoire
        self.aleatoire = tk.Button(
            self.racine,
            text="Mode aléatoire",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", int(float((self.width + self.height) / 50))),
            command=self.mode_aleatoire,
        )
        self.aleatoire.pack(ipady=6, expand=True)
        self.taille_aleatoire = lambda: (
            "System",
            int(float((self.width + self.height) / 50)),
        )  # Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.aleatoire, self.taille_aleatoire))

        # Bouton pour accéder au mode combinaison
        self.combinaison = tk.Button(
            self.racine,
            text="Combinaison",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", int(float((self.width + self.height) / 50))),
            command=self.mode_combinaison,
        )
        self.combinaison.pack(ipady=6, expand=True)
        self.taille_combinaison = lambda: (
            "System",
            int(float((self.width + self.height) / 50)),
        )  # Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.combinaison, self.taille_combinaison))

    def echap(self, event):
        """
        def: sur appui de la touche "échap", quitte la fenêtre et arrête le programme
        """
        if event.keysym == "Escape":
            self.racine.destroy()

    def affiche_touches(self, event):
        """
        def: sur appui de la touche "F3" ou "CTRL+T", affiche les touches disponibles dans un messagebox
        """
        if event.keysym == "F3" or event.keysym == "t":
            messagebox.showinfo(
                "Touches",
                "Echap : Quitter l'application",
            )

    def mode_libre(self):
        """
        def: sur appui du bouton "mode libre", détruit la fenêtre principale et lance le mode libre
        """
        # Destruction de la fenêtre principale pour accéder au mode libre
        self.racine.destroy()
        libre = MenuLibre.MenuLibre(self.nbr_vivant, self.nbr_cases, {})
        libre.racine.mainloop()

    def mode_aleatoire(self):
        """
        def: sur appui du bouton "mode aléatoire", détruit la fenêtre principale et affiche la fenêtre paramètre
        """
        # contrôle si la fenêtre paramètre existe déjà
        if self.parametre_aleatoire != None:
            self.parametre_aleatoire.destroy()
        # Création de la fenêtre paramètre
        self.parametre_aleatoire = tk.Toplevel(self.racine, bg="#141418")
        self.parametre_aleatoire.resizable(False, False)
        self.parametre_aleatoire.title("Paramètres")

        # affichage du curseur pour choisir le nombre de cases de la grille de jeu
        self.curseur_nbr_cases = tk.Scale(
            self.parametre_aleatoire,
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
        self.curseur_nbr_cases.pack(ipady=6, expand=True)
        self.curseur_nbr_cases.set(self.nbr_cases)
        self.curseur_nbr_cases.bind("<ButtonRelease-1>", self.maj_nbr_vivant)

        # affichage du curseur pour choisir le nombre de cellules vivantes initiales
        self.curseur_nbr_vivant = tk.Scale(
            self.parametre_aleatoire,
            orient="horizontal",
            from_=0,
            to=self.curseur_nbr_cases.get()
            * (int(self.curseur_nbr_cases.get() * 2) - 1),
            resolution=1,
            tickinterval=int(
                (
                    self.curseur_nbr_cases.get()
                    * (int(self.curseur_nbr_cases.get() * 2) - 1)
                )
                / 2
            ),
            length=350,
            label="Nombre de cellules vivantes",
            bg="#141418",
            fg="#A5A5B5",
            font="System",
            highlightbackground="#141418",
            troughcolor="#A5A5B5",
            activebackground="#A5A5B5",
        )
        self.curseur_nbr_vivant.pack(ipady=6, expand=True)
        self.curseur_nbr_vivant.set(self.nbr_vivant)

        # Bouton valider pour enregistrer les paramètres et lancer le mode aléatoire
        self.valider = tk.Button(
            self.parametre_aleatoire,
            text="Valider",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", 15),
            command=self.enregistre_parametre_aleatoire,
        )
        self.valider.pack(ipady=6, expand=True)

    def mode_combinaison(self):
        """
        def: sur appui du bouton "mode combinaison", détruit la fenêtre principale et affiche la fenêtre paramètre
        """
        # contrôle si la fenêtre paramètre existe déjà
        if self.parametre_combinaison != None:
            self.parametre_combinaison.destroy()

        # Création de la fenêtre paramètre
        self.parametre_combinaison = tk.Toplevel(self.racine, bg="#141418")
        self.parametre_combinaison.resizable(False, False)
        self.parametre_combinaison.title("Paramètres")

        # affichage du curseur pour choisir le nombre de cases de la grille de jeu (3, 4 ou 5)
        self.curseur_nbr_cases = tk.Scale(
            self.parametre_combinaison,
            orient="horizontal",
            from_=3,
            to=5,
            resolution=1,
            tickinterval=1,
            length=350,
            label="Nombre de cases",
            bg="#141418",
            fg="#A5A5B5",
            font="System",
            highlightbackground="#141418",
            troughcolor="#A5A5B5",
            activebackground="#A5A5B5",
        )
        self.curseur_nbr_cases.pack(ipady=6, expand=True)
        self.curseur_nbr_cases.set(4)

        # check pour choisir combinaison avec bords ou sans bords
        self.check_bords = tk.Checkbutton(
            self.parametre_combinaison,
            text="Combinaison avec bords ?",
            bg="#141418",
            fg="#A5A5B5",
            font="System",
            highlightbackground="#141418",
            var= self.bords,
        )
        self.check_bords.pack(ipady=6, expand=True)


        # Bouton valider pour enregistrer les paramètres et lancer le mode aléatoire
        self.valider = tk.Button(
            self.parametre_combinaison,
            text="Valider",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", 15),
            command=self.enregistre_parametre_combinaison,
        )
        self.valider.pack(ipady=6, expand=True)

    def maj_nbr_vivant(self, event):
        """
        def: quand on relache le curseur du nombre de cases, met à jour le curseur du nombre de cellules vivantes
        """
        self.curseur_nbr_vivant.config(
            to=self.curseur_nbr_cases.get()
            * (int(self.curseur_nbr_cases.get() * 2) - 1)
        )

        self.curseur_nbr_vivant.config(
            tickinterval=int(
                (
                    self.curseur_nbr_cases.get()
                    * (int(self.curseur_nbr_cases.get() * 2) - 1)
                )
                / 2
            )
        )

    def enregistre_parametre_aleatoire(self):
        """
        def: sur appui du bouton "valider", enregistre les paramètres et détruit la fenêtre paramètre et la fenetre principale pour lancer le mode aléatoire
        """
        # Enregistrement des paramètres
        self.nbr_vivant = self.curseur_nbr_vivant.get()
        self.nbr_cases = self.curseur_nbr_cases.get()
        self.parametre_aleatoire.destroy()

        # Destruction de la fenêtre principale pour accéder au mode aléatoire
        self.racine.destroy()
        aleatoire = LancerJeu.LancerJeu(
            self.nbr_vivant, self.nbr_cases, "Aleatoire", {}
        )
        aleatoire.racine.mainloop()

    def enregistre_parametre_combinaison(self):
        """
        def: sur appui du bouton "valider", enregistre les paramètres et détruit la fenêtre paramètre et la fenetre principale pour lancer le mode combinaison
        """
        # Enregistrement des paramètres
        self.nbr_cases = self.curseur_nbr_cases.get()
        self.parametre_combinaison.destroy()

        # Destruction de la fenêtre principale pour accéder au mode aléatoire
        self.racine.destroy()
        if self.bords.get() == True:
            aleatoire = CombinaisonAvecBords.CombinaisonAvecBords(self.nbr_cases)
            aleatoire.racine.mainloop()
        else:
            aleatoire = CombinaisonSansBords.CombinaisonSansBords(self.nbr_cases)
            aleatoire.racine.mainloop()


if __name__ == "__main__":
    # Lancement de la fenêtre principale
    menu_principal = MenuPrincipal(1000, 20)
    menu_principal.racine.mainloop()
