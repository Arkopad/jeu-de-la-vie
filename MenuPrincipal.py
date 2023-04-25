   # Importation des librairies
import tkinter as tk
from tkinter import messagebox

# Importation des classes des différents modes de jeu
import MenuLibre
import LancerJeu
from Affichage import Affichage


class MenuPrincipal(Affichage):
    def __init__(self, nbr_vivant, nbr_tour):
        # Création de la fenêtre principale
        super().__init__(nom=f'Menu_principale', geometry=(1280,720), nb_cellues=0)
        self.racine.iconbitmap("icone.ico")

        self.parametre = None
        self.nbr_vivant = nbr_vivant
        self.nbr_tours = nbr_tour

        self.racine.bind_all("<Key-Escape>", self.echap)

        self.creer_widgets()

    def creer_widgets(self):
        # Création des widgets de la fenêtre principale
        self.frame_top = tk.Frame(
            self.racine,
            borderwidth=int(float(self.width + self.height)/1000),
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )
        self.frame_top.pack(fill=tk.X, pady=12)

        self.fram_top_borderwidth = lambda : int(float(self.width + self.height)/1000) #Valeur d'actualisation de la bordure en fonction de la taille de la fenetre
        self.frame_actualisation.append((self.frame_top, self.fram_top_borderwidth))

        # Label du titre du jeu
        self.generation = tk.Label(
            self.frame_top,
            text="JEU DE LA VIE",
            font=("System", int(float((self.width+self.height)/50))),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.generation.pack(pady=4)

        self.police_generation = lambda : ("System", int(float((self.width+self.height)/50))) #Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.generation, self.police_generation))




        # Bannière rappel des touches
        self.frame_bot = tk.Frame(
            self.racine,
            borderwidth=int(float(self.width + self.height)/1000),
            bg="#010D19",
            highlightthickness=5,
            highlightbackground="black",
        )

        self.frame_bot.pack(fill=tk.X, pady=6, side=tk.BOTTOM)
        self.fram_bot_borderwidth = lambda : int(float(self.width + self.height)/1000) #Valeur d'actualisation de la bordure en fonction de la taille de la fenetre
        self.frame_actualisation.append((self.frame_bot, self.fram_bot_borderwidth))
        
        self.rappel_touches = tk.Label(
            self.frame_bot,
            text="F11 : Activer/Désactiver plein écran               Echap : Quitter l'application",
            font=("System", int(float((self.width+self.height)/133))),
            bg="#010D19",
            fg="#A5A5B5",
        )
        self.rappel_touches.pack()

        self.police_rappel_touches = lambda : ("System", int(float((self.width+self.height)/133))) #Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.rappel_touches, self.police_rappel_touches))





        # Bouton pour accéder au mode libre
        self.libre = tk.Button(
            self.racine,
            text="Mode libre",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", int(float((self.width+self.height)/50))),
            command=self.mode_libre,
        )
        # self.libre.bind("<Button-1>", self.mode_libre)
        self.libre.pack(ipady=6, expand=True)

        self.taille_libre = lambda : ("System", int(float((self.width+self.height)/50))) #Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.libre, self.taille_libre))


        # Bouton pour accéder au mode aléatoire
        self.aleatoire = tk.Button(
            self.racine,
            text="Mode aléatoire",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", int(float((self.width+self.height)/50))),
            command=self.mode_aleatoire,
        )
        self.aleatoire.pack(ipady=6, expand=True)

        self.taille_aleatoire = lambda : ("System", int(float((self.width+self.height)/50))) #Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.aleatoire, self.taille_aleatoire))

        # Bouton pour changer les paramètres du jeu
        self.raccourcis = tk.Button(
            self.racine,
            text="Paramètres",
            bg="#010D19",
            fg="#A5A5B5",
            font=("System", int(float((self.width+self.height)/50))),
            command=self.parametres,
        )
        self.raccourcis.pack(ipady=10, expand=True)

        self.taille_raccourcis = lambda : ("System", int(float((self.width+self.height)/50))) #Valeur d'actualisation du label en fontion de la taille de la fenetre
        self.actualisation_widgets.append((self.raccourcis, self.taille_raccourcis))


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
         
        
        self.text = tk.Label(self.parametre, text="Retour arrière : Effacer la grille ",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=0, expand=True)
        
        self.text = tk.Label(self.parametre,text = " Entrée : Re/Lancer le jeu",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=0, expand=True)
        
        self.text = tk.Label(self.parametre,text = "Echap : Quitter l'application/Revenir au menu principal",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=0, expand=True)

        
        self.text = tk.Label(self.parametre, text="Mode libre :",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=0, expand=True)
        
        self.text = tk.Label(self.parametre,text = "F1: Sauvegarder la grille",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=0, expand=True)
        
        self.text = tk.Label(self.parametre,text = "F2: Charger la grille",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=8, expand=True)
        
        
        self.text = tk.Label(self.parametre, text="Mode aléatoire :",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=0, expand=True)
        
        self.text = tk.Label(self.parametre,text = "Espace : changer la vitesse",
                             bg="#141418",
                             fg="#A5A5B5",
                             font="System")
        self.text.pack(ipady=8, expand=True)
        
        
        

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
