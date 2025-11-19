import pytest
from src.models import Livre
from src.exceptions import ErreurLivre

def test_erreurs_creation_livre():

    with pytest.raises(ErreurLivre) as exc_info:
        Livre(1, "Jean Dubois", "I31BS-7")
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurLivre) as exc_info:
        Livre("Livre Test", True, "I31BS-7")
    assert exc_info.value.code_erreur == 102

    with pytest.raises(ErreurLivre) as exc_info:
        Livre("Livre Test", "Jean Dubois", "")
    assert exc_info.value.code_erreur == 103