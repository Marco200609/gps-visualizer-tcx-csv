"""
Marco Giraud-Thomas 1ère F

Absent lors du premier cours
"""

# Librairies nécessaires

import csv
import tkinter
from math import *
from tkinter import *
from tkinter import filedialog
import tkintermapview

# Variables globales contenant toutes les données

# Demande quel fichier CSV ouvrir

fichier = filedialog.askopenfilename(title="choisir un fichier"".csv", filetypes=[("fichier CSV", "*.csv")])

prc = []
parcours = []
latitude = []
longitude = []
position = []
heure = []
cardio = []
alti = []
Poid = None
Age = None


# lit le fichier CSV selectionné et stocke les données dans un dictionnaire

def lire_csv():
    global parcours
    with open(fichier) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            row['latitude'] = float(row['latitude'])
            row['longitude'] = float(row['longitude'])
            row['altitude'] = float(row['altitude'])
            row['cardio'] = int(row['cardio'])
            prc.append(row)

    # verification des doublons :

    for h in prc:
        if h["heure"] not in parcours:
            parcours.append(h)


# Permet de connaître l'heure au point donné

def connaitre_temps(indice):
    t = heure[indice]
    li = t.split(":")
    h = int(li[0]) * 3600
    m = int(li[1]) * 60
    s = int(li[2])
    time = h + m + s
    return time


# Permet de connaître la distance au point donné

def connaitre_distance(indice):
    distance = 0
    for k in range(indice - 1):
        distance += 6371 * acos(sin(radians(latitude[k])) * sin(radians(latitude[k + 1])) + cos(radians(latitude[k])) *
                                cos(radians(latitude[k + 1])) * cos(radians(longitude[k] - longitude[k + 1])))
    return distance


# Permet de connaître la vitesse au point donné

def connaitre_vitesse(indice):
    diftemps = connaitre_temps(indice) - connaitre_temps(indice - 1)

    # verification que diftemps n'est pas égal à 0

    if diftemps == 0:
        diftemps = connaitre_temps(indice) - connaitre_temps(indice - 2)
    elif diftemps == 0:
        diftemps = connaitre_temps(indice) - connaitre_temps(indice - 3)
    elif diftemps == 0:
        print("Erreur CSV doublon !")
        return 0

    vitesse = (6371 * acos(sin(radians(latitude[indice - 1])) * sin(radians(latitude[indice]))
                           + cos(radians(latitude[indice - 1])) * cos(radians(latitude[indice]))
                           * cos(radians(longitude[indice - 1] - longitude[indice])))) / (diftemps / 3600)

    if vitesse < 0:
        vitesse = 0

    return vitesse


# Permet de connaître les calories au point donné

def connaitre_calorie(indice, poid):
    return connaitre_distance(indice) * poid * 1.036


# Permet de connaître l'effort au point donné

def connaitre_effort(indice, age):
    intensite = cardio[indice] / (207 - (0.7 * age))
    return intensite * 100


# permet de recentrer la fenêtre

def replacer_fenetre():
    map_widget.fit_bounding_box((latitude_max, longitude_min), (latitude_min, longitude_max))


# créé une seconde fenêtre pour la selection du poids et de l'âge

def ouvrir_fenetre():
    global Poid, Age
    # Créé la deuxième fenêtre

    second_window = tkinter.Toplevel()
    second_window.title("informations")

    # Ajoute deux cases d'entrée de texte

    tkinter.Label(second_window, text="Merci d'entrer votre poids : ").grid(row=0, column=0)
    poid = tkinter.Entry(second_window)
    poid.grid(row=0, column=1)

    tkinter.Label(second_window, text="Merci d'entrer votre âge : ").grid(row=1, column=0)
    age = tkinter.Entry(second_window)
    age.grid(row=1, column=1)

    # Ajoute un bouton pour valider les entrées

    def validation():
        global Poid, Age
        Poid = poid.get()
        Age = age.get()
        second_window.destroy()

    valider = tkinter.Button(second_window, text="Valider", command=validation)
    valider.grid(row=2, column=1)


# permet d'afficher les informations importantes en fonction du point selectionné avec le curseur

def gerer_curseur(evenement):
    num = int(evenement)
    x = latitude[num]
    y = longitude[num]

    # message d'erreur si le poids et l'âge ne sont pas definis

    if Poid is None or Age is None:
        marker1.set_position(x, y)
        marker1.set_text("Veuillez saisir votre poids et âge !")
    else:

        # affiche les informations

        marker1.set_position(x, y)
        marker1.set_text(("heure : {}\ncardio : {} BPM\naltitude : {} m \ndistance : {} km \nvitesse : {} km/h "
                          "\ncalories : {} kcal \neffort : {} %".format(heure[num], cardio[num], round(alti[num], 2),
                                                                        round(connaitre_distance(num), 2),
                                                                        round(connaitre_vitesse(num), 2),
                                                                        round(connaitre_calorie(num, int(Poid)), 2),
                                                                        round(connaitre_effort(num, int(Age)), 2))))


# permet de redémarer le programme quand l'on change de fichier CSV

def redemmarer():
    global map_widget, parcours, latitude, longitude, position, heure, cardio, alti, fichier, prc

    # demande quel fichier CSV ouvrir

    fichier = filedialog.askopenfilename(title="choisir un fichier"".csv", filetypes=[("fichier CSV", "*.csv")])

    # empêche l'effacement du parcours précédent si aucun fichier n'est choisi

    if fichier == "" or fichier is None:
        return

    # remet à zéro les variables

    parcours = []
    prc = []
    latitude = []
    longitude = []
    position = []
    heure = []
    cardio = []
    alti = []
    map_widget.delete_all_marker()
    map_widget.delete_all_path()

    # lance les fonctions d'initialisation

    lire_csv()
    info_parcours()
    creer()


# creé les boutons, le parcours, les géomarqueurs, le curseur et le centrage sur le parcours

def creer():
    global marker1, position, root_tk, map_widget

    map_widget.grid(column=0, row=0)
    map_widget.set_path(position, color="red", width=2)

    map_widget.fit_bounding_box((latitude_max, longitude_min), (latitude_min, longitude_max))

    map_widget.set_marker(latitude[0], longitude[0], text="début")
    map_widget.set_marker(latitude[-1], longitude[-1], text="fin")

    tkinter.Button(text="ouvrir CSV", command=redemmarer).place(x=200, y=650)

    marker1 = map_widget.set_marker(latitude[0], longitude[0])

    tkinter.Button(text="changer informations", command=ouvrir_fenetre).place(x=285, y=650)

    tkinter.Button(text="centrer sur le parcours", command=replacer_fenetre).place(x=435, y=650)

    Scale(orient=HORIZONTAL, from_=0, to=len(latitude) - 1, command=gerer_curseur, length=660).place(x=50, y=600)


# transforme le dictionnaire contenant les informations du CSV en listes distinctes et exploitables

def info_parcours():
    global latitude_max, latitude_min, longitude_max, longitude_min, heure, cardio, alti, position

    # création d'une liste de latitudes

    for pos in parcours:
        latitude.append(pos["latitude"])
    latitude_max = max(latitude)
    latitude_min = min(latitude)

    # création d'une liste de longitudes

    for pos in parcours:
        longitude.append(pos["longitude"])
    longitude_max = max(longitude)
    longitude_min = min(longitude)

    # création d'une liste d'heures

    for line in parcours:
        heure.append(line['heure'])

    # création d'une liste de cardios

    for line in parcours:
        cardio.append(line['cardio'])

    # création d'une liste d'altitudes

    for pos in parcours:
        alti.append(pos["altitude"])

    for x, y in zip(latitude, longitude):
        position.append((x, y))


# lance les fonctions d'initialisation

lire_csv()
info_parcours()

# création de la fenêtre tkinter

root_tk = Tk()
root_tk.geometry(f"{800}x{900}")
root_tk.title("map_view_example.py")

# création de la carte

map_widget = tkintermapview.TkinterMapView(
    root_tk,
    width=800,
    height=600,
    corner_radius=100
)

# lance la fonction "créer" après la création de ma fenêtre

creer()

root_tk.mainloop()
