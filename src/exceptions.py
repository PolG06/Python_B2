class ErreurBibliotheque(Exception):
    """Exception personnalisée concernant la bibliothèque"""
    def __init__(self, message: str, code_erreur: int = 0):
        super().__init__(message)
        self.code_erreur = code_erreur

class ErreurDonnees(Exception):
    """Exception personnalisée concernant les fichiers de données"""
    def __init__(self, message: str, code_erreur: int = 0):
        super().__init__(message)
        self.code_erreur = code_erreur

class ErreurLivre(Exception):
    """Exception personnalisée concernant les fichiers de données"""
    def __init__(self, message: str, code_erreur: int = 0):
        super().__init__(message)
        self.code_erreur = code_erreur

class ErreurLivreNumerique(Exception):
    """Exception personnalisée concernant les fichiers de données"""
    def __init__(self, message: str, code_erreur: int = 0):
        super().__init__(message)
        self.code_erreur = code_erreur