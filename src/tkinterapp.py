import tkinter as tk
from tkinter import ttk,Frame
from src.models import Bibliotheque

class AppBibliotheque ():
    def __init__(self):
        self.bibliotheque=Bibliotheque("Bibliothèque")
        self.fenetre = tk.Tk()
        self.fenetre.title("Python B2")
        self.fenetre.geometry("400x300")

        self.creer_widgets()
        self.run()
    
    def run(self):
        self.fenetre.mainloop()
    
    def creer_widgets(self):

        
        main_label = tk.Label(self.fenetre, text="Gestion de votre Bibliothèque", font=("Arial", 14))
        main_label.pack(pady=10)
        frame_add_book = ttk.LabelFrame(self.fenetre, text="Ajouter un livre")
        frame_add_book.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_add_book, text="Titre:").pack(anchor="w", padx=5, pady=2)
        self.entry_title = ttk.Entry(frame_add_book)
        self.entry_title.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_add_book, text="Auteur:").pack(anchor="w", padx=5, pady=2)
        self.entry_author = ttk.Entry(frame_add_book)
        self.entry_author.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_add_book, text="ISBN:").pack(anchor="w", padx=5, pady=2)
        self.entry_isbn = ttk.Entry(frame_add_book)
        self.entry_isbn.pack(fill="x", padx=5, pady=2)

        ttk.Label(frame_add_book, text="Taille du fichier (si livre numérique):").pack(anchor="w", padx=5, pady=2)
        self.entry_file_size = ttk.Entry(frame_add_book)
        self.entry_file_size.pack(fill="x", padx=5, pady=2)

        ttk.Button(frame_add_book, text="Valider", command=self.Ajouter_nouveau_livre).pack(pady=5)

        frame_show_books = ttk.LabelFrame(self.fenetre, text="Afficher la liste des livres")
        frame_show_books.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_show_books, text="Afficher", command=self.clic_bouton_show_books).pack(pady=5)

        frame_search_books = ttk.LabelFrame(self.fenetre, text="Rechercher par auteur")
        frame_search_books.pack(fill="x", padx=10, pady=5)

        self.entry_author_search = ttk.Entry(frame_search_books)
        self.entry_author_search.pack(fill="x", padx=5, pady=2)

        ttk.Button(frame_search_books, text="Rechercher", command=self.Rechercher_livre_par_auteur).pack(pady=5)

    def load_data(self):
        pass

    def clic_bouton_show_books():
        print("Bouton show books cliqué!")
    
    def Ajouter_noveau_livre():
        print("Bouton ajouter_livre cliqué!")

    def Rechercher_livre_par_auteur():
        print("Bouton recherché cliqué!")