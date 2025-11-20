import json
import csv
from src.exceptions import ErreurDonnees
from src.models import Livre_numerique

def ajouter_livre_dans_json(livre):
    fichier_json='data/data.json'
    from src.models import Livre_numerique,Livre
    if not isinstance(fichier_json,str):
        raise ErreurDonnees("Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",code_erreur=101)
    if not isinstance(livre,Livre):
        raise ErreurDonnees("Erreur, le livre entré doit être un instance de Livre ou de Livre_numerique",code_erreur=107)

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

def ajouter_utilisateur_dans_json(utilisateur):
    fichier_json='data/utilisateurs.json'
    from src.models import Utilisateur
    if not isinstance(fichier_json,str):
        raise ErreurDonnees("Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",code_erreur=101)
    if not isinstance(utilisateur,Utilisateur):
        raise ErreurDonnees("Erreur, le livre entré doit être un instance de Livre ou de Livre_numerique",code_erreur=107)

    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise ErreurDonnees("Impossible d'ouvrir le fichier Json renseigné",106)

    donnees.append({
        'nom': utilisateur.Nom,
        'mot de passe': utilisateur.MDP,
        'Admin?': utilisateur.IsAdmin,
        'liste de livres empruntés': []
    })
    with open(fichier_json, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2)
    
def ajouter_livre_emprunte(utilisateur, livre, date_debut, date_fin):
    from src.models import Livre, Livre_numerique
    fichier_json = 'data/utilisateurs.json'

    # Vérifications simples
    if not isinstance(utilisateur, str):  # on utilise le nom pour identifier l'utilisateur
        raise ErreurDonnees("Le nom de l'utilisateur doit être une string", code_erreur=107)
    if not isinstance(livre, Livre):
        raise ErreurDonnees("Le livre doit être une instance de Livre ou Livre_numerique", code_erreur=107)

    # Détermination des attributs du livre
    if isinstance(livre, Livre_numerique):
        est_numerique = True
        taille_fichier = livre.tailleFichier
    else:
        est_numerique = False
        taille_fichier = 0

    try:
        with open(fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise ErreurDonnees("Impossible d'ouvrir le fichier JSON des utilisateurs", 106)

    for utilisateur_parcouru in donnees:
        if utilisateur_parcouru['nom'] == utilisateur:
            utilisateur_parcouru['liste de livres empruntés'].append({
                'titre': livre.Titre,
                'auteur': livre.Auteur,
                'ISBN': livre.ISBN,
                'taille_du_fichier': taille_fichier,
                'est_numerique': est_numerique,
                'date_debut': date_debut,
                'date_fin': date_fin
            })
            break
    else:
        raise ErreurDonnees(f"L'utilisateur {utilisateur} n'existe pas dans le JSON", 107)

    with open(fichier_json, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2)

def recup_donnees_json():
    fichier_json='data/data.json'
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
            if not isinstance(livre["taille_du_fichier"], int) or livre["taille_du_fichier"]<0:
                raise ErreurDonnees("La taille du fichier doit être un entier positif (int>=0) .",code_erreur=108)
            else:
                bibliotheque.ajouter_livre_dans_liste(Livre_numerique(livre["titre"],livre["auteur"],livre["ISBN"],livre["taille_du_fichier"]))
        else: 
            
            bibliotheque.ajouter_livre_dans_liste(Livre(livre["titre"],livre["auteur"],livre["ISBN"]))

def supprimer_livre_par_ISBN_dans_json(isbn:str):
    fichier_json='data/data.json'
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

def exporter_donnees_en_csv():
    fichier_json='data/data.json'
    fichier_csv='data/data.csv'
    if not isinstance(fichier_json,str):
        raise ErreurDonnees("Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",code_erreur=101)
    if not isinstance(fichier_csv,str):
        raise ErreurDonnees("Erreur, le nom du fichier csv doit être un str décrivant le chemin relatif",code_erreur=106)
    donnees=recup_donnees_json()
    if len(donnees)==0:
        raise ErreurDonnees("Erreur, les données importées sont vides")
    descripteurs=list(donnees[0].keys())
    with open(fichier_csv, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=descripteurs)
        writer.writeheader()
        writer.writerows(donnees)
def reinitialiser_json():
    fichier_json = 'data/data.json'
    if not isinstance(fichier_json, str):
        raise ErreurDonnees(
            "Erreur, le nom du fichier Json doit être un str décrivant le chemin relatif",
            code_erreur=101
        )

    livres_initiales = [
        {
            "titre": "Les Misérables",
            "auteur": "Victor Hugo",
            "ISBN": "VH1234",
            "taille_du_fichier": 0,
            "est_numerique": False
        },
        {
            "titre": "Alice au pays des merveilles",
            "auteur": "Lewis Carroll",
            "ISBN": "LC5678",
            "taille_du_fichier": 15,
            "est_numerique": True
        },
        {
            "titre": "Harry Potter à l'école des sorciers",
            "auteur": "J.K. Rowling",
            "ISBN": "JK0001",
            "taille_du_fichier": 120,
            "est_numerique": True
        },
        {
            "titre": "Orgueil et Préjugés",
            "auteur": "Jane Austen",
            "ISBN": "JA1122",
            "taille_du_fichier": 0,
            "est_numerique": False
        },
        {
            "titre": "Moby Dick",
            "auteur": "Herman Melville",
            "ISBN": "HM3344",
            "taille_du_fichier": 0,
            "est_numerique": False
        },
        {
            "titre": "Le Seigneur des Anneaux : La Communauté de l'Anneau",
            "auteur": "J.R.R. Tolkien",
            "ISBN": "JR5678",
            "taille_du_fichier": 200,
            "est_numerique": True
        },
        {
            "titre": "Jane Eyre",
            "auteur": "Charlotte Brontë",
            "ISBN": "CB7788",
            "taille_du_fichier": 0,
            "est_numerique": False
        },
        {
            "titre": "Dracula",
            "auteur": "Bram Stoker",
            "ISBN": "BS9900",
            "taille_du_fichier": 30,
            "est_numerique": True
        },
        {
            "titre": "Le Vieil Homme et la Mer",
            "auteur": "Ernest Hemingway",
            "ISBN": "EH5566",
            "taille_du_fichier": 0,
            "est_numerique": False
        },
        {
            "titre": "Les Aventures de Tom Sawyer",
            "auteur": "Mark Twain",
            "ISBN": "MT1122",
            "taille_du_fichier": 10,
            "est_numerique": True
        }
    ]

    try:
        with open(fichier_json, 'w', encoding='utf-8') as f:
            json.dump(livres_initiales, f, indent=2)
    except Exception:
        raise ErreurDonnees("Impossible de réinitialiser le fichier JSON", 106)
