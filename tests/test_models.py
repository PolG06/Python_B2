import pytest
from src.models import *
from src.exceptions import *
from tests.conftest import *

def test_erreurs_creation_livre():
    with pytest.raises(ErreurLivre) as exc_info:
        Livre(1, "Jean Dubois", "I31BS-7",2,"Compte")
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurLivre) as exc_info:
        Livre("Livre Test", True, "I31BS-7",2,"Compte")
    assert exc_info.value.code_erreur == 102

    with pytest.raises(ErreurLivre) as exc_info:
        Livre("Livre Test", "Jean Dubois", "",4,"Compte")
    assert exc_info.value.code_erreur == 103

def test_erreurs_creation_livre_numerique():
    with pytest.raises(ErreurLivre) as exc_info:
        Livre_numerique("Livre Test", True, "I31BS-7",12,"Comte")
    assert exc_info.value.code_erreur == 102


    with pytest.raises(ErreurLivreNumerique) as exc_info:
        Livre_numerique("Livre Test", "Jean Dubois", "I31BS-7","1225","Comte")
    assert exc_info.value.code_erreur == 101

def tests_erreurs_creation_bibliotheque():

    with pytest.raises(ErreurBibliotheque) as exc_info:
        Bibliotheque(4)
    assert exc_info.value.code_erreur == 104

    with pytest.raises(ErreurBibliotheque) as exc_info:
        Bibliotheque("")
    assert exc_info.value.code_erreur == 104

@pytest.mark.parametrize(
    "titre, auteur, isbn, nbr_exempl,categorie",
    [
        ("Le Mystère de l'Étoile", "Jean Dupont", "AB123-1XYZ",1,"Conte"),
        ("Aventures en Forêt", "Claire Martin", "CD456-7JKL",7,"Roman"),
        ("Le Secret du Pharaon", "Marc Leblanc", "EF789-2MNO",6,"Poésie"),
        ("Voyage au Centre du Temps", "Sophie Durand", "GH012-4PQR",2,"Fable"),
        ("L'Odyssée Perdue", "Louis Moreau", "IJ345-6STU",3,"Bande_dessinée"),
        ("Les Ombres de la Ville", "Emma Bernard", "KL678-9VWX",1,"Roman historique")
    ]
)
def test_creation_livre_param(titre, auteur, isbn,nbr_exempl,categorie):
    livre = Livre(titre, auteur, isbn, nbr_exempl,categorie)
    assert livre.titre == titre
    assert livre.auteur == auteur
    assert livre.ISBN == isbn
    assert livre.nombre_exemplaires==nbr_exempl
    assert livre.categorie==categorie

@pytest.mark.parametrize(
    "titre, auteur, isbn, taille_fichier, categorie",
    [
        ("Le Petit Prince", "Antoine de Saint-Exupéry", "NP123-1",100,"conte"),
        ("1984", "George Orwell", "OR198-4",54,"Roman"),
        ("Harry Potter à l'École des Sorciers", "J.K. Rowling", "HP001-7",73,"Science-fiction"),
        ("Le Seigneur des Anneaux", "J.R.R. Tolkien", "LOTR-333",121,"Science-fiction"),
        ("Fondation", "Isaac Asimov", "AS987-6",214,"Roman"),
        ("Les Misérables", "Victor Hugo", "VH456-2",52,"Roman")
    ]
)
def test_creation_livre_numerique_param(titre, auteur, isbn, taille_fichier,categorie):
    ln1 = Livre_numerique(titre, auteur, isbn, taille_fichier,categorie)
    assert ln1.titre == titre
    assert ln1.auteur == auteur
    assert ln1.ISBN == isbn
    assert ln1.tailleFichier == taille_fichier
    assert ln1.categorie==categorie

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
    assert b1.afficher()==(nom,[])

def test_erreurs_fonctionnement_bibliotheque(bibliotheque1:Bibliotheque,livre1:Livre):
    b1=bibliotheque1
    l1=livre1

    with pytest.raises(ErreurBibliotheque) as exc_info:
        b1.ajouter_livre_dans_liste("livre")
    assert exc_info.value.code_erreur == 101

    with pytest.raises(ErreurBibliotheque) as exc_info:
        b1.ajouter_livre(("Le Petit Prince", "Antoine de Saint-Exupéry", "NP123-1", 12,1,"Conte"))
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
    assert b2.nom=="Bibliothèque Test"
    assert len(b2.liste_livres)==7
    b2.ajouter_livre_dans_liste(livre1)
    assert len(b2.liste_livres)==8
    assert livre1 in b2.liste_livres
    b2.supprimer_livre_par_ISBN(livre1.ISBN)
    assert not livre1 in b2.liste_livres
    assert len(b2.liste_livres)==7
    b2.ajouter_livre(livre1)
    assert len(b2.rechercher_livre_par_titre("livrequin'existepas"))==0
    assert len(b2.rechercher_livre_par_titre(livre1.titre))==1
    assert len(b2.liste_livres)==8
    assert livre1 in b2.rechercher_livre_par_titre(livre1.titre)
    assert len(b2.liste_livres)==8
    assert len(b2.rechercher_livre_par_auteur("auteurquin'existepas"))==0
    assert len(b2.liste_livres)==8
    assert livre1 in b2.rechercher_livre_par_auteur(livre1.auteur)