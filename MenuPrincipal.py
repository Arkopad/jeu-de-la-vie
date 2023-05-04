# Importation des librairies
import tkinter as tk
from tkinter import messagebox

# Importation des classes
import MenuLibre
import LancerJeu
from Affichage import Affichage


class MenuPrincipal(Affichage):
    def __init__(self, nbr_vivant, nbr_cases):
        # Création de la fenêtre principale avec la classe Affichage
        super().__init__(nom=f"Menu_principal", geometry=(1280, 720), nb_cellues=0)
        icone = tk.PhotoImage(file="icon.png")
        self.racine.iconphoto(True, icone)

        # Initialisation des variables
        self.parametre = None
        self.nbr_vivant = nbr_vivant
        self.nbr_cases = nbr_cases

        # Affectation des touches
        self.racine.bind_all("<Key-Escape>", self.echap)
        self.racine.bind_all("<Key-F3>", self.affiche_touches)
        self.racine.bind_all("<Control-t>", self.affiche_touches)

        # Création des widgets
        self.creer_widgets()

    def creer_widgets(self):
        """
        def: crée et affiche les widgets sur la fenêtre principale
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
        self.frame_top.pack(fill=tk.X, pady=12)
        self.fram_top_borderwidth = lambda: int(
            float(self.width + self.height) / 1000
        )  # Valeur d'actualisation de la bordure en fonction de la taille de la fenetre
        self.frame_actualisation.append((self.frame_top, self.fram_top_borderwidth))

        # Label du titre du jeu
        self.generation = tk.Label(
            self.frame_top,
            text="JEU DE LA VIE",
            font=("System", int(float((self.width + self.height) / 50))),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.generation.pack(pady=4)
        self.police_generation = lambda: (
            "System",
            int(float((self.width + self.height) / 50)),
        )  # Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.generation, self.police_generation))

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

    def echap(self, event):
        """
        def: sur appui de la touche "échap", quitte la fenêtre et arrête le programme
        in: None
        out: None
        """
        if event.keysym == "Escape":
            self.racine.destroy()

    def affiche_touches(self, event):
        """
        def: sur appui de la touche "F3" ou "control+t", affiche les touches disponibles dans un messagebox
        in: None
        out: None
        """
        if event.keysym == "F2" or event.keysym == "t":
            messagebox.showinfo(
                "Touches",
                "Touches disponibles dans le menu principal : \n\nEchap : Quitter l'application",
            )

    def mode_libre(self):
        """
        def: sur appui du bouton "mode libre", détruit la fenêtre principale et lance le mode libre
        in: None
        out: None
        """
        # Destruction de la fenêtre principale pour accéder au mode libre
        self.racine.destroy()
        libre = MenuLibre.MenuLibre(self.nbr_vivant, self.nbr_cases, {})
        libre.racine.mainloop()

    def mode_aleatoire(self):
        """
        def: sur appui du bouton "mode aléatoire", détruit la fenêtre principale et affiche la fenêtre paramètre
        in: None
        out: None
        """
        # contrôle si la fenêtre paramètre existe déjà
        if self.parametre != None:
            self.parametre.destroy()
        # Création de la fenêtre paramètre
        self.parametre = tk.Toplevel(self.racine, bg="#141418")
        self.parametre.resizable(False, False)
        self.parametre.title("Paramètres")

        # affichage du curseur pour choisir le nombre de cases de la grille de jeu
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
        self.curseur_nbr_cases.pack(ipady=6, expand=True)
        self.curseur_nbr_cases.set(self.nbr_cases)
        self.curseur_nbr_cases.bind("<ButtonRelease-1>", self.maj_nbr_vivant)

        # affichage du curseur pour choisir le nombre de cellules vivantes initiales
        self.curseur_nbr_vivant = tk.Scale(
            self.parametre,
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
            self.parametre,
            text="Valider",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", 15),
            command=self.enregistre_parametre,
        )
        self.valider.pack(ipady=6, expand=True)

    def maj_nbr_vivant(self, event):
        """
        def: quand on relache le curseur du nombre de cases, met à jour le curseur du nombre de cellules vivantes
        in: None
        out: None
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

    def enregistre_parametre(self):
        """
        def: sur appui du bouton "valider", enregistre les paramètres et détruit la fenêtre paramètre et la fenetre principale pour lancer le mode aléatoire
        in: None
        out: None
        """
        # Enregistrement des paramètres
        self.nbr_vivant = self.curseur_nbr_vivant.get()
        self.nbr_cases = self.curseur_nbr_cases.get()
        self.parametre.destroy()

        # Destruction de la fenêtre principale pour accéder au mode aléatoire
        self.racine.destroy()
        aleatoire = LancerJeu.LancerJeu(
            self.nbr_vivant, self.nbr_cases, "Aleatoire", {}
        )
        aleatoire.racine.mainloop()


if __name__ == "__main__":
    # Lancement de la fenêtre principale
    menu_principal = MenuPrincipal(1000, 20)
    menu_principal.racine.mainloop()
