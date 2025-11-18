#Modélisation d'une classe livre numérique
from src.livre import Livre
class Livre_numerique(Livre):
    def __init__(self,titre:str,auteur:str,ISBN:str,taille_fichier:int):
        super().__init__(titre,auteur,ISBN)
        self._taille_fichier:int=taille_fichier

    @property
    def tailleFichier(self)->int:
        return self._taille_fichier