import pytest
from src.models import Bibliothèque,Livre,Livre_numerique
from src.gestion_json import json

@pytest.fixture
def bibliotheque1():
    return Bibliothèque("Première bibliothèque")

@pytest.fixture
def livre1():
    return Livre("1984", "George Orwell", "12345")

@pytest.fixture
def livreNumerique1():
    return Livre_numerique("Dune", "Frank Herbert", "98765", 50)