import pytest
from src.models import Bibliotheque,Livre,Livre_numerique
from src.gestion_json import *

@pytest.fixture
def bibliotheque1():
    return Bibliotheque("Première bibliothèque")

@pytest.fixture
def bibliotheque2():
    biblio=Bibliotheque("Bibliothèque Test")
    biblio.ajouter_livre_dans_liste(Livre("Le Nom de la Rose", "Umberto Eco", "12MO5"))
    biblio.ajouter_livre_dans_liste(Livre("Le Petit Prince", "Antoine de Saint-Exupéry","AA151"))
    biblio.ajouter_livre_dans_liste(Livre("Le Comte de Monte-Cristo", "Alexandre Dumas","PP78H"))
    biblio.ajouter_livre_dans_liste(Livre("Les Corbeau et le Renard", "Jean de La Fontaine","JJ474"))
    biblio.ajouter_livre_dans_liste(Livre_numerique("Les Fleurs du Mal", "Charles Baudelaire","F156",12))
    biblio.ajouter_livre_dans_liste(Livre_numerique("L'Étranger", "Albert Camus","P9KO",90))
    biblio.ajouter_livre_dans_liste(Livre_numerique("Candide", "Voltaire","FR19878",125))
    return biblio

@pytest.fixture
def livre1():
    return Livre("1984", "George Orwell", "12345")


