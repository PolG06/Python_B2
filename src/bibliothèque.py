#Modélisation d'une bibliothèque
from src.gestion_json import *
class Bibliothèque:
    def __init__(self, nom):
        self._nom:str = nom
        self._liste_livres:list = []

    def ajouter_livre_dans_liste(self,livre):
        if isinstance(livre,Livre):
            self._liste_livres.append(livre)
        else: 
            print ("Erreur lors de l'exécution de la fonction ajouter_livre_dans_liste")
            print ("le livre entré n'est pas une instance de Livre ou de Livre_numerique: "+livre)

    def ajouter_livre(self, livre):
        if isinstance(livre,Livre):
            self.ajouter_livre_dans_liste(livre)
            ajouter_livre_dans_json(livre)
        else: 
            print ("Erreur lors de l'exécution de la fonction ajouter_livre")
            print ("le livre entré n'est pas une instance de Livre ou de Livre_numerique: "+livre)

    def importer_json(self):
        donnees=recup_donnees_json()
        importer_donnes_json(self,donnees)

    def supprimer_livre(self, isbn):
        if isinstance(isbn,str):
            supprimer_livre_par_ISBN_dans_json(isbn)
            self._liste_livres=[livre for livre in self._liste_livres if livre.ISBN!=isbn]
        else:
            print ("Erreur lors de l'exécution de la fonction supprimer_livre")
            print ("l'ISBN entré n'est pas un str: "+isbn)
    



    def rechercher_livre_par_titre(self, chaine):
        return [livre for livre in self._liste_livres if chaine in livre.Titre]

    def rechercher_livre_par_auteur(self, chaine):
        return [livre for livre in self._liste_livres if chaine in livre.Auteur]

    @property
    def afficher(self):
        return self._nom, self._liste_livres
    
