import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import webbrowser


connexion = sqlite3.connect("Projet.db") #connexion avec la bdd
curseur = connexion.cursor() #curseur permet de faire des requetes sql


print("Veuillez indiquer le médicament recherché : ")
nom_med = '\t'+input().upper()+' '

connexion.close()

# Ouvrir le fichier texte en mode lecture
with open("CIS_bdpm.txt", "r") as fichier:
    Tab_ligne = []
    for ligne in fichier:
        # Vérifier si le mot-clé est dans la ligne
        if nom_med in ligne:
            # Rechercher le premier numéro entier dans la ligne
            Tab_ligne.append(ligne)
            
    for i in Tab_ligne :  
        CIS = re.search('\d+', i)
        # Recherche expression reguliere jusqu'au mot Autorisation, qu'on lui retire
        nom = str(re.search(r'\t(.*?)\b{}\b'.format('Autorisation'), i).group(1))
        if CIS:
        # Convertir le numéro trouvé en entier et l'affecter à la variable "numero"
            CIS = int(CIS.group())
            # Afficher le numéro trouvé
            print("'{}' : {}".format(CIS, nom))
            
            
#######################################################################################################
print("Veuillez indiquer le CIS du médicament choisi : ")            
CIS_choose = input() 
link = "https://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid={}&typedoc=R".format(CIS_choose)
#print(link)                      

#Test ouverture url
#webbrowser.open(link)

########################################################################################################
# Récupérer le contenu de la page web
reponse = requests.get(link)

#Rcp = list("RcpCompoQualiQuanti", "RcpContreindications")

# Vérifier si la requête a réussi (code de statut HTTP 200)
if reponse.status_code == 200:
    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(reponse.text, "html.parser")

    paragraphes = soup.find_all("p", class_="AmmAnnexeTitre1")

    # Afficher les paragraphes trouvés
    for i, paragraphe in enumerate(paragraphes):
       print(paragraphe.get_text())
       print() 
        
    dictionnaire_med = {
        "1": "DENOMINATION DU MEDICAMENT", 
        "2": "COMPOSITION QUALITATIVE ET QUANTITATIVE",
        "3": "FORME PHARMACEUTIQUE",
        "4": "DONNEES CLINIQUES",
        "5": "PROPRIETES PHARMACOLOGIQUES",
        "6": "DONNEES PHARMACEUTIQUES",
        "7": "TITULAIRE DE LAUTORISATION DE MISE SUR LE MARCHE",
        "8": "NUMERO(S) DAUTORISATION DE MISE SUR LE MARCHE",
        "9": "DATE DE PREMIERE AUTORISATION/DE RENOUVELLEMENT DE LAUTORISATION",
        "10": "DATE DE MISE A JOUR DU TEXTE",
        "11": "DOSIMETRIE",
        "12": "INSTRUCTIONS POUR LA PREPARATION DES RADIOPHARMACEUTIQUES",        
    }
    
    print("Choisir le numéro de l'information : ")            
    cle_choose = str(input())
    print(dictionnaire_med[cle_choose])
    
    
    
    
    
else:
    print("Impossible de récupérer le contenu de la page web.")
    