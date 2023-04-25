# Importation des librairies
import tkinter as tk

# Importation des classes des différents modes de jeu
import MenuLibre
import LancerJeu


class MenuPrincipal:
    def __init__(self, nbr_vivant, nbr_tour):
        # Création de la fenêtre principale
        self.racine = tk.Tk()
        self.racine.title("Jeu de la vie")
        self.racine.geometry("1280x720")
        icone = tk.PhotoImage(file="icon.png")
        self.racine.iconphoto(True, icone)
        self.racine.resizable(0, 0)
        self.racine.config(background="#141418")
        self.racine.attributes("-fullscreen", False)

        self.parametre = None
        self.nbr_vivant = nbr_vivant
        self.nbr_tours = nbr_tour

        self.racine.bind_all("<Key-Escape>", self.echap)

        self.creer_widgets()

    def creer_widgets(self):
        # Création des widgets de la fenêtre principale
        self.frame_top = tk.Frame(
            self.racine,
            borderwidth=2,
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=12)

        self.generation = tk.Label(
            self.frame_top,
            text="JEU DE LA VIE",
            font=("System", 35),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.generation.pack(pady=4)

        # Bouton pour accéder au mode libre
        self.libre = tk.Button(
            self.racine,
            text="Mode libre",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", 35),
            command=self.mode_libre,
        )
        # self.libre.bind("<Button-1>", self.mode_libre)
        self.libre.pack(ipady=6, expand=True)

        # Bouton pour accéder au mode aléatoire
        self.aleatoire = tk.Button(
            self.racine,
            text="Mode aléatoire",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", 35),
            command=self.mode_aleatoire,
        )
        self.aleatoire.pack(ipady=6, expand=True)

        # Bouton pour changer les paramètres du jeu
        self.raccourcis = tk.Button(
            self.racine,
            text="Paramètres",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", 35),
            command=self.parametres,
        )
        self.raccourcis.pack(ipady=10, expand=True)

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
            text="F11 : Activer/Désactiver plein écran               Echap : Quitter l'application",
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

    def mode_libre(self):
        # Destruction de la fenêtre principale pour accéder au mode libre
        self.racine.destroy()
        libre = MenuLibre.MenuLibre(self.nbr_vivant, self.nbr_tours, {})
        libre.racine.mainloop()

    def mode_aleatoire(self):
        # Destruction de la fenêtre principale pour accéder au mode aléatoire
        self.racine.destroy()
        aleatoire = LancerJeu.LancerJeu(
            self.nbr_vivant, self.nbr_tours, "Aleatoire", {}
        )
        aleatoire.racine.mainloop()

    def parametres(self):
        # Bouton paramètre pour régler le nombre de cellules vivantes initiales, le nombre de tours et afficher les touches disponibles
        if self.parametre != None:
            self.parametre.destroy()

        self.parametre = tk.Toplevel(self.racine, bg="#141418")
        self.parametre.resizable(False, False)

        self.curseur_nbr_vivant = tk.Scale(
            self.parametre,
            orient="horizontal",
            from_=0,
            to=1770,
            resolution=1,
            tickinterval=1770,
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

        self.curseur_nbr_tours = tk.Scale(
            self.parametre,
            orient="horizontal",
            from_=0,
            to=1000,
            resolution=5,
            tickinterval=200,
            length=350,
            label="Nombre de tours",
            bg="#141418",
            fg="#A5A5B5",
            font="System",
            highlightbackground="#141418",
            troughcolor="#A5A5B5",
            activebackground="#A5A5B5",
        )
        self.curseur_nbr_tours.pack(ipady=6, expand=True)
        self.curseur_nbr_tours.set(self.nbr_tours)

        self.valider = tk.Button(
            self.parametre,
            text="Valider",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", 15),
            command=self.enregistre_parametre,
        )
        self.valider.pack(ipady=6, expand=True)

    def enregistre_parametre(self):
        self.nbr_vivant = self.curseur_nbr_vivant.get()
        self.nbr_tours = self.curseur_nbr_tours.get()
        self.parametre.destroy()


if __name__ == "__main__":
    # Lancement de la fenêtre principale
    menu_principal = MenuPrincipal(660, 1000)
    menu_principal.racine.mainloop()
