#Modélisation d'une bibliothèque
from datetime import datetime
from src.file_manager import *
from src.exceptions import ErreurBibliotheque,ErreurLivre,ErreurLivreNumerique
class Bibliotheque:
    def __init__(self, nom:str):
        if not isinstance(nom, str) or not nom.strip():
            raise ErreurBibliotheque("Le nom de la bibliothèque doit être une chaîne non vide.",code_erreur=104)
        self._nom:str = nom
        self._liste_livres:list = []

    def ajouter_livre_dans_liste(self,livre):
        if not isinstance(livre,Livre):
            raise ErreurBibliotheque("Vous essayer d'ajouter autre chose qu'une instance de Livre ou de Livre_numerique dans la bibliothèque", code_erreur=101)
        self._liste_livres.append(livre)
    
    def ajouter_livre(self, livre):
        if not isinstance(livre,Livre):
            raise ErreurBibliotheque("Vous essayer d'ajouter autre chose qu'une instance de Livre ou de Livre_numerique dans la bibliothèque et dans le fichier json", code_erreur=102)
        self.ajouter_livre_dans_liste(livre)
        ajouter_livre_dans_json(livre)
            
    def importer_json(self):
        donnees=recup_donnees_json()
        importer_donnes_json(self,donnees)
            
    def supprimer_livre_par_ISBN(self, isbn:str):
        if not isinstance(isbn,str):
            raise ErreurBibliotheque("Vous essayer de supprimer autre chose qu'une instance de Livre ou de Livre_numerique de la bibliothèque", code_erreur=103)
        supprimer_livre_par_ISBN_dans_json(isbn)
        self._liste_livres=[livre for livre in self._liste_livres if livre.ISBN!=isbn]
        
    def rechercher_livre_par_titre(self, chaine:str):
        if not isinstance(chaine,str):
            raise ErreurBibliotheque("La chaine de recherche doit être un str", code_erreur=105)
        return [livre for livre in self._liste_livres if chaine in livre.Titre]

    def rechercher_livre_par_auteur(self, chaine:str):
        if not isinstance(chaine,str):
            raise ErreurBibliotheque("La chaine de recherche doit être un str", code_erreur=105)
        return [livre for livre in self._liste_livres if chaine in livre.Auteur]
    
    def Getliste_livres(self)->list:
        return self._liste_livres
    
    def Getnom(self)->str:
        return self._nom

    @property
    def afficher(self):
        return (self._nom, self._liste_livres)

#Modélisation d'une classe livre
class Livre:
    def __init__(self,titre:str,auteur:str,ISBN:str):
        if not isinstance(titre, str) or not titre.strip():
            raise ErreurLivre("Le titre doit être une chaîne non vide.",code_erreur=101)
        if not isinstance(auteur, str) or not auteur.strip():
            raise ErreurLivre("L'auteur doit être une chaîne non vide.",code_erreur=102)
        if not isinstance(ISBN, str) or not ISBN.strip():
            raise ErreurLivre("L'ISBN doit être une chaîne non vide.",code_erreur=103)
        self._titre=titre
        self._auteur=auteur
        self._ISBN=ISBN

    @property
    def Titre(self)->str:
        return self._titre
    @property
    def Auteur(self)->str:
        return self._auteur
    @property
    def ISBN(self)->str:
        return self._ISBN
    
#Modélisation d'une classe livre numérique
class Livre_numerique(Livre):
    def __init__(self,titre:str,auteur:str,ISBN:str,taille_fichier:int):
        if not isinstance(taille_fichier, int) or taille_fichier<0:
            raise ErreurLivreNumerique("La taille du fichier doit être un entier positif (int>=0) .",code_erreur=101)
        super().__init__(titre,auteur,ISBN)
        self._taille_fichier:int=taille_fichier

    @property
    def tailleFichier(self)->int:
        return self._taille_fichier
    
class Utilisateur():
    def __init__(self,nom,mdp):
        self.Nom=nom
        self.MDP=mdp
        self.IsAdmin=False
        self.livres_empruntes=[]
        self.livres_empruntes_ce_mois=0
        self.livres_par_mois=5
    
    def promouvoir(self):
        if not self.IsAdmin:
            self.IsAdmin=True
            self.livres_par_mois*=2

    def enregistrer_utilisateur_dans_json(self):
        ajouter_utilisateur_dans_json(self)

    def emprunter_livre(self, livre, date_debut, date_fin):
        date_debut_dt = datetime.strptime(date_debut, "%d/%m/%Y")
        date_fin_dt = datetime.strptime(date_fin, "%d/%m/%Y")

        if self.livres_empruntes_ce_mois >= self.livres_par_mois:
            print("Vous avez emprunté tous vos livres ce mois-ci, veuillez revenir le mois prochain.")
            return

        for l in self.livres_empruntes:
            emprunt_start = datetime.strptime(l[1][0], "%d/%m/%Y")
            emprunt_end = datetime.strptime(l[1][1], "%d/%m/%Y")
            if (date_debut_dt <= emprunt_end and date_fin_dt >= emprunt_start):
                print(self.Nom+" ne peut pas emprunter 2 livres en même temps.")
                return

        self.livres_empruntes.append((livre, (date_debut, date_fin)))
        ajouter_livre_emprunte(self, livre, date_debut, date_fin)
        self.livres_empruntes_ce_mois+=1
        print(self.Nom+" a emprunté le livre du "+date_debut+" au "+date_fin)

    def reset_livres_empruntes_ce_mois(self):
        self.livres_empruntes_ce_mois

        
