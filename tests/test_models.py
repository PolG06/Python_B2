import pytest
from src.models import *
from src.gestion_json import reinitialiser_json
from src.exceptions import *
from tests.conftest import *

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

def test_erreurs_creation_livre_numerique():
    with pytest.raises(ErreurLivre) as exc_info:
        Livre_numerique("Livre Test", True, "I31BS-7",12)
    assert exc_info.value.code_erreur == 102


    with pytest.raises(ErreurLivreNumerique) as exc_info:
        Livre_numerique("Livre Test", "Jean Dubois", "I31BS-7","1225")
    assert exc_info.value.code_erreur == 101

def tests_erreurs_creation_bibliotheque():

    with pytest.raises(ErreurBibliotheque) as exc_info:
        Bibliotheque(4)
    assert exc_info.value.code_erreur == 104

    with pytest.raises(ErreurBibliotheque) as exc_info:
        Bibliotheque("")
    assert exc_info.value.code_erreur == 104

@pytest.mark.parametrize(
    "titre, auteur, isbn",
    [
        ("Le Mystère de l'Étoile", "Jean Dupont", "AB123-1XYZ"),
        ("Aventures en Forêt", "Claire Martin", "CD456-7JKL"),
        ("Le Secret du Pharaon", "Marc Leblanc", "EF789-2MNO"),
        ("Voyage au Centre du Temps", "Sophie Durand", "GH012-4PQR"),
        ("L'Odyssée Perdue", "Louis Moreau", "IJ345-6STU"),
        ("Les Ombres de la Ville", "Emma Bernard", "KL678-9VWX")
    ]
)
def test_creation_livre_param(titre, auteur, isbn):
    livre = Livre(titre, auteur, isbn)
    assert livre.Titre == titre
    assert livre.Auteur == auteur
    assert livre.ISBN == isbn

@pytest.mark.parametrize(
    "titre, auteur, isbn, taille_fichier",
    [
        ("Le Petit Prince", "Antoine de Saint-Exupéry", "NP123-1", 12),
        ("1984", "George Orwell", "OR198-4", 25),
        ("Harry Potter à l'École des Sorciers", "J.K. Rowling", "HP001-7", 30),
        ("Le Seigneur des Anneaux", "J.R.R. Tolkien", "LOTR-333", 45),
        ("Fondation", "Isaac Asimov", "AS987-6", 40),
        ("Les Misérables", "Victor Hugo", "VH456-2", 55)
    ]
)
def test_creation_livre_numerique_param(titre, auteur, isbn, taille_fichier):
    ln1 = Livre_numerique(titre, auteur, isbn, taille_fichier)
    assert ln1.Titre == titre
    assert ln1.Auteur == auteur
    assert ln1.ISBN == isbn
    assert ln1.tailleFichier == taille_fichier

@pytest.mark.parametrize(
    "nom",
    [
        "Bibliothèque Centrale",
        "Médiathèque du Quartier",
        "Bibliothèque Universitaire",
        "Archives Municipales",
    ]
)
def test_creation_bibliotheque_param(nom):
    b1=Bibliotheque(nom)
    assert b1.afficher==(nom,[])

def test_erreurs_fonctionnement_bibliotheque(bibliotheque1:Bibliotheque,livre1:Livre):
    b1=bibliotheque1
    l1=livre1

    with pytest.raises(ErreurBibliotheque) as exc_info:
        b1.ajouter_livre_dans_liste("livre")
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurBibliotheque) as exc_info:
        b1.ajouter_livre(("Le Petit Prince", "Antoine de Saint-Exupéry", "NP123-1", 12))
    assert exc_info.value.code_erreur == 102

    with pytest.raises(ErreurBibliotheque) as exc_info:
        b1.supprimer_livre_par_ISBN(12)
    assert exc_info.value.code_erreur == 103

    with pytest.raises(ErreurBibliotheque) as exc_info:
        b1.rechercher_livre_par_titre(l1)
    assert exc_info.value.code_erreur == 105

    with pytest.raises(ErreurBibliotheque) as exc_info:
        b1.rechercher_livre_par_auteur(12)
    assert exc_info.value.code_erreur == 105

def test_fonctionnement_bibliotheque(bibliotheque2:Bibliotheque,livre1:Livre):
    b2=bibliotheque2
    assert b2.Getnom()=="Bibliothèque Test"
    assert len(b2.Getliste_livres())==7
    b2.ajouter_livre_dans_liste(livre1)
    assert len(b2.Getliste_livres())==8
    assert livre1 in b2.Getliste_livres()
    b2.supprimer_livre_par_ISBN(livre1.ISBN)
    assert not livre1 in b2.Getliste_livres()
    assert len(b2.Getliste_livres())==7
    b2.ajouter_livre(livre1)
    assert len(b2.rechercher_livre_par_titre("livrequin'existepas"))==0
    assert len(b2.rechercher_livre_par_titre(livre1.Titre))==1
    assert len(b2.Getliste_livres())==8
    assert livre1 in b2.rechercher_livre_par_titre(livre1.Titre)
    assert len(b2.Getliste_livres())==8
    assert len(b2.rechercher_livre_par_auteur("auteurquin'existepas"))==0
    assert len(b2.Getliste_livres())==8
    assert livre1 in b2.rechercher_livre_par_auteur(livre1.Auteur)
    reinitialiser_json()