import pytest
from src.models import *
from src.file_manager import *
from src.exceptions import ErreurDonnees
from tests.conftest import *

def test_erreur_type_fichier_json():

    with pytest.raises(ErreurDonnees) as exc_info:
        ajouter_livre_dans_json("livre1")
    assert exc_info.value.code_erreur == 107

def test_erreurs_importer_donnes_json(bibliotheque):

    with pytest.raises(ErreurDonnees) as exc_info:
        importer_donnes_json(bibliotheque, 12)
    assert exc_info.value.code_erreur == 101

    donnees_non_dict = [1, 2, 3]
    with pytest.raises(ErreurDonnees) as exc_info:
        importer_donnes_json(bibliotheque, donnees_non_dict)
    assert exc_info.value.code_erreur == 102

    donnees_titre_invalide = [{"titre": "", "auteur": "Jean", "ISBN": "123", "est_numerique": False, "taille_du_fichier": 0}]
    with pytest.raises(ErreurDonnees) as exc_info:
        importer_donnes_json(bibliotheque, donnees_titre_invalide)
    assert exc_info.value.code_erreur == 103

    donnees_auteur_invalide = [{"titre": "Livre1", "auteur": "", "ISBN": "123", "est_numerique": False, "taille_du_fichier": 0}]
    with pytest.raises(ErreurDonnees) as exc_info:
        importer_donnes_json(bibliotheque, donnees_auteur_invalide)
    assert exc_info.value.code_erreur == 104

    donnees_ISBN_invalide = [{"titre": "Livre1", "auteur": "Jean", "ISBN": "", "est_numerique": False, "taille_du_fichier": 0}]
    with pytest.raises(ErreurDonnees) as exc_info:
        importer_donnes_json(bibliotheque, donnees_ISBN_invalide)
    assert exc_info.value.code_erreur == 105

    donnees_taille_invalide = [{"titre": "Livre1", "auteur": "Jean", "ISBN": "123", "est_numerique": False, "taille_du_fichier": -1}]
    with pytest.raises(ErreurDonnees) as exc_info:
        importer_donnes_json(bibliotheque, donnees_taille_invalide)
    assert exc_info.value.code_erreur == 108

def test_erreurs_supprimer_livre_par_ISBN():

    with pytest.raises(ErreurDonnees) as exc_info:
        supprimer_livre_par_ISBN_dans_json(123)
    assert exc_info.value.code_erreur == 107

    with pytest.raises(ErreurDonnees) as exc_info:
        supprimer_livre_par_ISBN_dans_json("")
    assert exc_info.value.code_erreur == 107





