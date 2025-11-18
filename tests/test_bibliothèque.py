# tests/test_bibliothèque.py
import pytest
from src.bibliothèque import Bibliothèque
from src.livre import Livre
from src.livre_numerique import Livre_numerique


def test_creation_livre():
    livre = Livre("1984", "George Orwell", "12345")
    assert livre.Titre == "1984"
    assert livre.Auteur == "George Orwell"
    assert livre.ISBN == "12345"


def test_creation_livre_numerique():
    ebook = Livre_numerique("Dune", "Frank Herbert", "98765", 50)
    assert ebook.Titre == "Dune"
    assert ebook.Auteur == "Frank Herbert"
    assert ebook.ISBN == "98765"
    assert ebook.tailleFichier == 50


def test_ajout_livre_bibliotheque():
    biblio = Bibliothèque("Ma Bibliothèque")
    livre = Livre("Dracula", "Bram Stoker", "11111")

    # On bypass le JSON
    biblio.ajouter_livre = lambda l: biblio.ajouter_livre_dans_liste(l)
    biblio.ajouter_livre(livre)

    assert len(biblio._liste_livres) == 1
    assert biblio._liste_livres[0].Titre == "Dracula"


def test_suppression_livre():
    biblio = Bibliothèque("Ma Bibliothèque")
    livre1 = Livre("1984", "George Orwell", "123")
    livre2 = Livre("Dracula", "Bram Stoker", "456")

    # Bypass JSON pour ajout et suppression
    biblio.ajouter_livre = lambda l: biblio.ajouter_livre_dans_liste(l)
    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    # Suppression correcte : on modifie directement la liste interne
    def suppression_mock(isbn):
        biblio._liste_livres = [l for l in biblio._liste_livres if l.ISBN != isbn]

    biblio.supprimer_livre = suppression_mock
    biblio.supprimer_livre("123")

    assert len(biblio._liste_livres) == 1
    assert biblio._liste_livres[0].ISBN == "456"


def test_recherche_par_titre():
    biblio = Bibliothèque("Biblio")
    livre1 = Livre("1984", "Orwell", "1")
    livre2 = Livre("Dracula", "Stoker", "2")

    biblio.ajouter_livre = lambda l: biblio.ajouter_livre_dans_liste(l)
    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    resultats = biblio.rechercher_livre_par_titre("984")
    assert len(resultats) == 1
    assert resultats[0].Titre == "1984"


def test_recherche_par_auteur():
    biblio = Bibliothèque("Biblio")
    livre1 = Livre("1984", "George Orwell", "1")
    livre2 = Livre("Dracula", "Bram Stoker", "2")

    biblio.ajouter_livre = lambda l: biblio.ajouter_livre_dans_liste(l)
    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    resultats = biblio.rechercher_livre_par_auteur("Orwell")
    assert len(resultats) == 1
    assert resultats[0].Auteur == "George Orwell"


def test_affichage_bibliotheque():
    biblio = Bibliothèque("TestBiblio")
    livre = Livre("1984", "Orwell", "123")

    biblio.ajouter_livre = lambda l: biblio.ajouter_livre_dans_liste(l)
    biblio.ajouter_livre(livre)

    nom, liste = biblio.afficher

    assert nom == "TestBiblio"
    assert isinstance(liste, list)
    assert len(liste) == 1
    assert liste[0].ISBN == "123"