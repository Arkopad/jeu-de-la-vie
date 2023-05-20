## README

### Prérequis

Les librairies suivantes sont nécéssaires pour lancer le programme :

- tkinter

```sh
pip3 install tkinter
```

- numpy

```sh
pip3 install numpy
```

- tqdm

```sh
pip3 install tqdm
```

- numba

```sh
pip3 install numba
```

### Lancement 

1. Télécharger le dossier 
2. Executer le fichier 'MenuPrincipal.py'

### Présentation

Le programme possède trois fonctionnalités :
1. Mode Combinaison : Dans une grille 2x2, 3x3, 4x4 ou 5x5, ce mode permet de trouver et d'afficher toutes les combinaisons stables. (attention, en grille 5x5, le temps de calcul peut être long)
2. Mode aléatoire : dans une grille de taille choisie, lance le jeu de la vie avec un nombre de cellules vivantes initiales placées aléatoirement sur la grille (attention, au delà de 50 cases, le temps de calcul peut être voire très long)
3. Mode Libre : Permet de placer manuellement les cellules sur la grille avant de lancer le jeu de la vie. Permet également de sauvegarder et de charger des grilles

### Touches 

Les touches utilisables sont expliquées sur chaque fênetre en appuyant sur "F3" ou "CTRL+T" ou en appuyant sur le bouton "TOUCHES" dans le mode combinaison. 

#### A propos

Auteurs : MEYNARD Lucien, SAMAIN Luc, NARAYANIN Timothée

Etudiants 2e année INSA Lyon

formateur utilisé : Black

![Jeu de la vie](https://cdn-icons-png.flaticon.com/512/4071/4071999.png "Jeu de la vie")
