import json
import csv
from src.livre import Livre
from src.livre_numerique import Livre_numerique


def ajouter_livre_dans_json(livre:Livre,fichier_json:str='../data/data.json'):
    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        donnees = []

    if isinstance(livre, Livre_numerique):
        est_numerique=True
        taille_fichier = livre.TailleFichier
    else:
        taille_fichier = 0
        est_numerique=False

    donnees.append({
        'titre': livre.Titre,
        'auteur': livre.Auteur,
        'ISBN': livre.ISBN,
        'taille_du_fichier': taille_fichier,
        'est_numerique': est_numerique
    })

    with open(fichier_json, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2)

def recup_donnees_json(fichier_json:str='../data/data.json'):
    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def importer_donnes_json(bibliotheque, donnees:list):
    for livre in donnees:
        if (livre["est_numerique"]):
            bibliotheque.ajouter_livre(Livre_numerique(livre["titre"],livre["auteur"],livre["ISBN"],livre["taille_du_fichier"]))
        else: 
            bibliotheque.ajouter_livre(Livre(livre["titre"],livre["auteur"],livre["ISBN"]))

def supprimer_livre_par_ISBN_dans_json(isbn:str, fichier_json:str='../data/data.json'):
    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        donnees = []

    donnees = [livre for livre in donnees if livre['ISBN'] != isbn]

    with open(fichier_json, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2)

def exporter_donnees_en_csv(fichier_json:str='../data/data.json',fichier_csv:str='../data.data.csv'):
    donnees=recup_donnees_json(fichier_json)
    if len(donnees)>0:
        descripteurs=list(donnees[0].keys())
        with open(fichier_csv, 'w', newline='', encoding='utf-8') as fichier:
            writer = csv.DictWriter(fichier, fieldnames=descripteurs)
            writer.writeheader()
            writer.writerows(donnees)