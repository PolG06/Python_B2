import pytest
from src.models import *
from src.gestion_json import *
from src.exceptions import ErreurDonnees
from tests.conftest import *

def test_erreur_type_fichier_json(livre1):
    with pytest.raises(ErreurDonnees) as exc_info:
        ajouter_livre_dans_json(livre1, fichier_json=123)
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurDonnees) as exc_info:
        ajouter_livre_dans_json("livre1")
    assert exc_info.value.code_erreur == 107

def test_fichier_json_inexistant(livre1):
    fichier_inexistant = "inexistant.json"
    with pytest.raises(ErreurDonnees) as exc_info:
        ajouter_livre_dans_json(livre1, fichier_json=fichier_inexistant)
    assert exc_info.value.code_erreur == 106


def test_erreurs_recup_donnees_json():
    with pytest.raises(ErreurDonnees) as exc_info:
        recup_donnees_json(123)
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurDonnees) as exc_info:
        recup_donnees_json("inexistant.json")
    assert exc_info.value.code_erreur == 106

    with pytest.raises(ErreurDonnees) as exc_info:
        recup_donnees_json(12)
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurDonnees) as exc_info:
        recup_donnees_json([1,5,6,5,8,7,9])
    assert exc_info.value.code_erreur == 102


def test_erreurs_importer_donnes_json(bibliotheque):

    with pytest.raises(ErreurDonnees) as exc_info:
        importer_donnes_json(bibliotheque, "liste_donnees")
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
    assert exc_info.value.code_erreur == 107

def test_erreurs_supprimer_livre_par_ISBN():

    with pytest.raises(ErreurDonnees) as exc_info:
        supprimer_livre_par_ISBN_dans_json("123", fichier_json=123)
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurDonnees) as exc_info:
        supprimer_livre_par_ISBN_dans_json(123)
    assert exc_info.value.code_erreur == 107

    with pytest.raises(ErreurDonnees) as exc_info:
        supprimer_livre_par_ISBN_dans_json("")
    assert exc_info.value.code_erreur == 107

    with pytest.raises(ErreurDonnees) as exc_info:
        supprimer_livre_par_ISBN_dans_json("123", fichier_json="inexistant.json")
    assert exc_info.value.code_erreur == 106

def test_erreurs_exporter_donnees_en_csv(tmp_path):

    with pytest.raises(ErreurDonnees) as exc_info:
        exporter_donnees_en_csv(fichier_json=123)
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurDonnees) as exc_info:
        exporter_donnees_en_csv(fichier_csv=456)
    assert exc_info.value.code_erreur == 106

def test_erreurs_reinitialiser_json():
    
    with pytest.raises(ErreurDonnees) as exc_info:
        reinitialiser_json(123)
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurDonnees) as exc_info:
        reinitialiser_json(["data.json"])
    assert exc_info.value.code_erreur == 101


    with pytest.raises(ErreurDonnees) as exc_info:
        reinitialiser_json("inexistant.json")
    assert exc_info.value.code_erreur == 106


