"""
Lycée Saint-André :: 1NSI
Mini-projet GPS/CSV
02/03/2023

pip install tcxreader
"""

# Bannière
print("********************")
print("*** TCX2CSV v0.1 ***")
print("********************")


# Librairies
try:
    import sys
    from tcxreader.tcxreader import TCXReader, TCXTrackPoint
except ImportError as erreur:
    print("=> ERREUR : La librairie tcxreader n'est pas installée !")
    print("=> Veuillez l'installer avec la commande suivante :")
    print("  $ python3 -m pip install tcxreader")
    sys.exit(-1)

# Lecture du nom de fichier à convertir en paramètre
chemin_fichier_tcx = ""
chemin_fichier_csv = ""
if len(sys.argv) != 2:
    print("=> ERREUR : Il manque le fichier TCX à convertir en paramètre, par exemple :")
    print("  $ python3 ./tcx2csv.py ./mon_parcours.tcx")
    sys.exit(-2)
else:
    chemin_fichier_tcx = sys.argv[1]
    chemin_fichier_csv = chemin_fichier_tcx.replace("tcx", "csv")


# Ouverture du fichier TCX et récupération des points

try:
    tcx_reader = TCXReader()
    TCXTrackPoint = tcx_reader.read(chemin_fichier_tcx)
    points = TCXTrackPoint.trackpoints
    print(f"=> ouverture du fichier TCX : {chemin_fichier_tcx} ...")
except FileNotFoundError as erreur:
    print(f"=> ERREUR : Impossible de trouver le fichier : {chemin_fichier_tcx} !")
    sys.exit(-3)

# Création du fichier CSV
print(f"=> création du fichier csv : {chemin_fichier_csv} ...")
fichier_csv = open(chemin_fichier_csv, "w")
fichier_csv.write("heure;latitude;longitude;altitude;cardio\n")

# Lecture des points des fichiers TCX
parcours = []
compteur_tcx = 0
for point in points:
    position = {}
    heure = f"{point.time}"
    position["heure"] = heure[11:]
    position["latitude"] = point.latitude
    position["longitude"] = point.longitude
    position["altitude"] = point.elevation
    position["cardio"] = point.hr_value
    parcours.append(position)
    compteur_tcx += 1
    """
    ligne = ""
    heure = f"{point.time}"
    ligne += f"{heure[11:]};"
    ligne += f"{point.latitude};"
    ligne += f"{point.longitude};"
    ligne += f"{point.elevation};"
    ligne += f"{point.hr_value}\n"
    print(ligne)
    fichier_csv.write(ligne)
    """

# Ecriture dans le fichier CSV
compteur_csv = 0
for position in parcours:
    if position['heure'] is not None and \
        position['latitude'] is not None and \
        position['longitude'] is not None and \
        position['altitude'] is not None and \
        position['cardio'] is not None:
        ligne = ""    
        ligne += f"{position['heure']};"
        ligne += f"{position['latitude']};"
        ligne += f"{position['longitude']};"
        ligne += f"{position['altitude']};"
        ligne += f"{position['cardio']}\n"
        print(ligne)
        fichier_csv.write(ligne)
        compteur_csv += 1


# Fermeture des fichiers
print("=> Fermeture des fichiers")
fichier_csv.close()

# Bilan
print(f"=> Nombre de points TCX trouvés : {compteur_tcx}")
print(f"=> Nombre de points CSV écrits  : {compteur_csv}")
if compteur_tcx != compteur_csv:
    print("=> ERREUR : il doit y avoir des erreurs dans le fichier TCX !")

