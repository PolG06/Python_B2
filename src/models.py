#Modélisation d'une bibliothèque
from src.gestion_json import *
from src.exceptions import ErreurBibliotheque,ErreurDonnees,ErreurLivre,ErreurLivreNumerique
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
