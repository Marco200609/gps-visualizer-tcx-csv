# GPS Visualizer (TCX → CSV → Carte)

Ce dépôt contient un projet scolaire réalisé au lycée (NSI). Le code est un prototype pédagogique — il fonctionne, mais il n’est pas optimisé ni structuré comme un projet professionnel.

Résumé
------
Ce projet fournit deux scripts Python pour convertir et visualiser des parcours GPS :
- `tcx2csv.py` : convertit un fichier TCX en CSV (format attendu : heure;latitude;longitude;altitude;cardio).
- `Projet.py` : application interactive Tkinter qui charge un CSV, trace le parcours sur une carte (tkintermapview) et affiche des mesures (distance cumulée, vitesse instantanée, calories estimées, effort).

Fonctionnalités
--------------
- Conversion TCX → CSV (ligne de commande) avec `tcxreader`.
- Visualisation du parcours sur une carte intégrée (Tkinter + tkintermapview).
- Curseur interactif pour parcourir les points et afficher :
  - heure, cardio (BPM), altitude (m)
  - distance cumulée (km)
  - vitesse instantanée (km/h)
  - calories estimées (kcal) en fonction du poids
  - effort (%) en fonction de l'âge

Prérequis
---------
- Python 3.8 ou supérieur
- pip
- Librairies Python :
  - tcxreader
  - tkintermapview
  - tkinter

Installation rapide
------------------
1. Cloner le dépôt (ou copier les fichiers).
2. Installer les dépendances :
```bash
python3 -m pip install tcxreader tkintermapview tkinter
```

Format CSV attendu
------------------
- Séparateur : point-virgule (`;`)
- En-tête : `heure;latitude;longitude;altitude;cardio`

Utilisation détaillée
---------------------

1) Conversion TCX → CSV
```bash
python3 tcx2csv.py chemin/vers/fichier.tcx
```
Le script crée un fichier CSV dans le même dossier (même nom, extension `.csv`).

2) Application graphique (visualisation)
```bash
python3 Projet.py
```
- À l'ouverture, une boîte de dialogue te demande de choisir un fichier CSV.
- La carte affiche le parcours, un marqueur pour le début/fin, un curseur permet de sélectionner un point et d'afficher les informations calculées.
- Boutons :
  - "ouvrir CSV" : choisir un autre fichier CSV
  - "changer informations" : entrer poids et âge (nécessaires pour calories / effort)
  - "centrer sur le parcours" : recentre la vue sur l'ensemble du trajet

Limites connues et notes techniques
----------------------------------
- Robustesse : prévoir une meilleure gestion des données manquantes / doublons / erreurs de format CSV.
- Interface : améliorer l'interface avec un thème plus récent (custumtkinter) et entre autres afficher des informations au-dessous de la carte.
- Performances : pour de très gros CSV (tens de milliers de points), l'interface peut devenir lente ; envisager le découpage ou l'optimisation de l'affichage.
- Ajouter graphiques (matplotlib) : altitude / cardio / vitesse en fonction du temps.
- Supporter d'autres formats (GPX, FIT).
