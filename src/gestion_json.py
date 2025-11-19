import json
import csv
from exceptions import ErreurDonnees

def ajouter_livre_dans_json(livre,fichier_json:str='../data/data.json'):
    from src.models import Livre_numerique
    if not isinstance(fichier_json,str):
        raise ErreurDonnees("Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",code_erreur=101)

    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise ErreurDonnees("Impossible d'ouvrir le fichier Json renseigné",106)

    if isinstance(livre, Livre_numerique):
        est_numerique=True
        taille_fichier = livre.tailleFichier
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
    if not isinstance(fichier_json,str):
        raise ErreurDonnees("Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",code_erreur=101)
    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            datas=json.load(f)
            if not isinstance(datas,list):
                raise (ErreurDonnees("Les données récupérées ne sont pas au bon format, vous devriez récupérer une liste de dictionnaires",code_erreur=101))
            if not all(isinstance(d, dict) for d in datas):
                raise ErreurDonnees("Chaque élément du JSON doit être un dictionnaire.", code_erreur=102)
            return datas
    except (FileNotFoundError, json.JSONDecodeError):
        raise ErreurDonnees("Impossible d'ouvrir le fichier Json renseigné",106)

def importer_donnes_json(bibliotheque, donnees:list):
    from src.models import Livre_numerique,Livre
    if not isinstance(donnees,list):
        raise (ErreurDonnees("Les données récupérées ne sont pas au bon format, vous devriez récupérer une liste de dictionnaires",code_erreur=101))
    if not all(isinstance(d, dict) for d in donnees):
        raise ErreurDonnees("Chaque élément du JSON doit être un dictionnaire.", code_erreur=102)
    for livre in donnees:
        if not isinstance(livre["titre"], str) or not livre["titre"].strip():
            raise ErreurDonnees(f"Dans les données importées,Le titre du livre n'est pas valide (!= str ou null): {livre['titre']}",code_erreur=103)
        if not isinstance(livre["auteur"], str) or not livre["auteur"].strip():
            raise ErreurDonnees(f"Dans les données importées, le nom de l'auteur du livre n'est pas valide (!= str ou null): {livre['auteur']}",code_erreur=104)
        if not isinstance(livre["ISBN"], str) or not livre["ISBN"].strip():
            raise ErreurDonnees(f"Dans les données importées, l'ISBN' du livre n'est pas valide (!= str ou null): {livre['ISBN']}",code_erreur=105)
        
        if (livre["est_numerique"]):
            bibliotheque.ajouter_livre(Livre_numerique(livre["titre"],livre["auteur"],livre["ISBN"],livre["taille_du_fichier"]))
        else: 
            if not isinstance(livre["taille_du_fichier"], int) or livre["taille_du_fichier"]<0:
                raise ErreurDonnees("La taille du fichier doit être un entier positif (int>=0) .",code_erreur=101)
            bibliotheque.ajouter_livre(Livre(livre["titre"],livre["auteur"],livre["ISBN"]))

def supprimer_livre_par_ISBN_dans_json(isbn:str, fichier_json:str='../data/data.json'):
    if not isinstance(fichier_json,str):
        raise ErreurDonnees("Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",code_erreur=101)
    if not isinstance(isbn, str) or not isbn.strip():
        raise ErreurDonnees(f"L'ISBN renseigné n'est pas valide : {isbn}", code_erreur=107)
    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise ErreurDonnees("Impossible d'ouvrir le fichier Json renseigné",106)

    donnees = [livre for livre in donnees if livre['ISBN'] != isbn]
    with open(fichier_json, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2)

def exporter_donnees_en_csv(fichier_json:str='../data/data.json',fichier_csv:str='../data/data.csv'):
    if not isinstance(fichier_json,str):
        raise ErreurDonnees("Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",code_erreur=101)
    if not isinstance(fichier_csv,str):
        raise ErreurDonnees("Erreur, le nom du fichier csv doit être un str décrivant le chemin relatif",code_erreur=106)
    donnees=recup_donnees_json(fichier_json)
    if len(donnees)==0:
        raise ErreurDonnees("Erreur, les données importées sont vides")
    descripteurs=list(donnees[0].keys())
    with open(fichier_csv, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=descripteurs)
        writer.writeheader()
        writer.writerows(donnees)
    