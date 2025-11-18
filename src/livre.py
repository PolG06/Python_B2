#Modélisation d'une classe livre
class Livre:
    def __init__(self,titre:str,auteur:str,ISBN:str):
        self._titre:str=titre
        self._auteur:str=auteur
        self._ISBN:str=ISBN

    @property
    def Titre(self)->str:
        return self._titre
    @property
    def Auteur(self)->str:
        return self._auteur
    @property
    def ISBN(self)->str:
        return self._ISBN
    