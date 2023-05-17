# Fichier permettant d'initialiser les fenetres des différents menus et options du jeu de la vie.
import tkinter as tk


class Affichage:
    def __init__(
        self,
        nom="Titre",
        geometry=(500, 500),
        nb_cellues=0,
        dimensions=(0, 0),
        *args,
        **kwargs,
    ) -> None:
        """
        Classe permettant de créer une fenêtre tkinter avec un nombre de cellules défini.
        in: nom: str, geometry: tuple, nb_cellues: int
        out: None

        variables: Racine, geometry, nb_cellules, taille_cellule, actualisation_widgets, canvases, width, height, ligne, colonne
        """
        self.ligne = dimensions[0]
        self.colonne = dimensions[1]
        self.racine = tk.Tk()
        self.racine.title(f"Jeu de la vie - {nom}.")
        self.racine.geometry(str(geometry[0]) + "x" + str(geometry[1]))
        self.racine.config(background="#141418")
        self.racine.attributes("-fullscreen", False)
        self.actualisation_widgets = []  # Liste des widgets
        self.canvases = [
            [None for j in range(self.colonne)] for i in range(self.ligne)
        ]  # Liste des canvas
        self.frame_actualisation = []  # Liste des frames

        # !! Configuration des cellules !! PAS OBLIGATOIRE
        self.nb_cellues = nb_cellues
        try:
            self.taille_cellule = geometry[1] / self.colonne
            self.taille_cellule -= (
                self.taille_cellule / 3.33
            )  # On enlève 30% de la taille de la cellule pour laisser de l'espace pour les widgets
        except:
            pass
            # print("Definition de la variable 'self.colonne' ou 'self.ligne', manquante, valeur nulle?")
        # !! Configuration des cellules !! PAS OBLIGATOIRE

        self.racine.update()
        self.width = self.racine.winfo_width()
        self.height = self.racine.winfo_height()

        self.racine.bind(
            "<Configure>",
            lambda event: (
                self.fenetre_redimensionnee(event),
                self.font_redimensionnement(event),
                self.frame_redimensionnement(event),
            ),
        )

    def actualisation(self, widget, rapport) -> None:
        """
        Fonction qui prend en entrée un widget et une fonction lambda qui permet de mettre à jour le widget, et qui l'ajoute à la liste des widgets à actualiser.
        in: widget: tk.Widget, value: lambda
        out: None
        """
        self.actualisation_widgets.append((widget, rapport))

    # Redimensionnement des cellules
    def fenetre_redimensionnee(self, event) -> None:
        """
        Fonction permettant de redimensionner le frame après que la fenêtre l'ai été
        in: None
        out: None
        """
        # Actulaisation des dimensions de la fenêtre
        self.width = self.racine.winfo_width()
        self.height = self.racine.winfo_height()
        # print(f"nouvelle taille de la fenetre{self.width}x{self.height}")

        # Redimensionnement des cellules:
        if self.nb_cellues > 0:
            self.taille_cellule = min(self.width, self.height) / self.colonne
            self.taille_cellule -= (
                self.taille_cellule / 3.33
            )  # On enlève 30% de la taille de la cellule pour laisser de l'espace pour les widgets
            for i in range(self.ligne):
                for j in range(self.colonne):
                    canevas = self.canvases[i][j]
                    if canevas != None:
                        self.canvases[i][j].config(
                            width=self.taille_cellule, height=self.taille_cellule
                        )

    # Redimensionnement des labels et boutons
    def font_redimensionnement(self, event) -> None:
        """
        Fonction permettant de redimensionner les labels en passant par le font.
        in: None
        out: None
        """
        # Actualisation des dimensions de la fenêtre
        self.width = self.racine.winfo_width()
        self.height = self.racine.winfo_height()
        labels = []
        buttons = []

        for widget, value in self.actualisation_widgets:
            if isinstance(widget, tk.Label):
                labels.append((widget, value))
            if isinstance(widget, tk.Button):
                buttons.append((widget, value))

        for (
            label,
            value,
        ) in (
            labels
        ):  # Attention ici value est une fonction lambda(sinon on ne peut pas stocker l'expresssion a actualiser, mais seulement son résultat)
            # print(f"label actualisé:{label.cget('text')}, nouvelle taille du font:{value()}")
            label.config(font=value())

        for button, value in buttons:
            # print(f"boutton actualisé:{button.cget('text')}, nouvelle taille du font:{value()}")
            button.config(font=value())

    def frame_redimensionnement(self, event) -> None:
        """
        Fonction permettant de redimensionner les bordures des frames.
        in: None
        out: None
        """
        # Actualisation des dimensions de la fenêtre
        self.width = self.racine.winfo_width()
        self.height = self.racine.winfo_height()

        for frame, border in self.frame_actualisation:
            # print(f"frame actualisé:{str(frame)}, nouvelle taille de la bordurewidth:{border()}")
            frame.config(borderwidth=border())
