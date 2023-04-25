import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import webbrowser


#TRAITEMENT DE LA LIGNE DU FICHIER TEXTE
def traitement_ligne(ligne) : 
    CIS = int(str(re.search('\d+', ligne)))
    nom = str(re.search(r'\t(.*?)+,', ligne).group(0)) 
    admin = str(re.search(r',\s* (.*)', ligne).group(1))
    #curseur.execute("INSERT INTO Medicaments (CIS, nom, administration) VALUES (?, ?, ?)",(CIS, nom, admin))
    #connexion.commit()

    

#LECTURE DU FICHIER TEXTE ET IMPLEMENTATION DE LA TABLE MEDICAMENTS
connexion = sqlite3.connect("Projet.db") #connexion avec la bdd
curseur = connexion.cursor() #curseur permet de faire des requetes sql

with open("CIS_bdpm.txt", "r") as fichier:
    ligne = fichier.readline()
    while ligne :
        traitement_ligne(ligne)
        ligne = fichier.readline()
connexion.close()
print("Done.")
