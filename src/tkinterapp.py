import tkinter as tk
from tkinter import ttk,messagebox
from src.models import *
from src.file_manager import * 

class AppBibliotheque ():
    def __init__(self):
        self.bibliotheque=Bibliotheque("Bibliothèque")
        self.fenetre = tk.Tk()
        self.fenetre.title("Python B2")
        self.fenetre.geometry("800x600")

        self.load_data()
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

        frame_search_books_by_author = ttk.LabelFrame(self.fenetre, text="Rechercher par auteur")
        frame_search_books_by_author.pack(fill="x", padx=10, pady=5)

        self.entry_author_search = ttk.Entry(frame_search_books_by_author)
        self.entry_author_search.pack(fill="x", padx=5, pady=2)

        ttk.Button(frame_search_books_by_author, text="Rechercher", command=self.Rechercher_livre_par_auteur).pack(pady=5)

        frame_export_data = ttk.LabelFrame(self.fenetre, text="Exporter les données dans un fichier CSV")
        frame_export_data.pack(fill="x", padx=10, pady=5)
        ttk.Button(frame_export_data, text="Exporter CSV", command=self.Exporter_data_csv).pack(pady=5)

        ttk.Button(text="Fermer", command=self.Fermer, width=15).pack(pady=(15, 5), ipady=10)


    def load_data(self):
        data_recup_json=recup_donnees_json()
        importer_donnes_json(self.bibliotheque,data_recup_json)
        print("Données bien importées!")

    def clic_bouton_show_books(self):
        print("Voici tous vos livres")
        for livre in self.bibliotheque.Getliste_livres():
            if (isinstance (livre,Livre_numerique)):
                print ("-livre numérique: ",livre.Titre,", il a été écrit par ",livre.Auteur,"Son ISBN est: ",livre.ISBN," et sa taille est "+str(livre.tailleFichier))
            elif isinstance (livre,Livre): 
                print ("-livre non-numérique: ",livre.Titre,", il a été écrit par ",livre.Auteur,"Son ISBN est: ",livre.ISBN)
        print("-----------------------------------------------------")
        messagebox.showinfo("Succès","Vos livres s'affichent en console!")
        self.reinitialiser_entry_formulaire()
    
    def Ajouter_nouveau_livre(self):
        titre = self.entry_title.get().strip()
        auteur = self.entry_author.get().strip()
        isbn = self.entry_isbn.get().strip()
        taille_fichier = self.entry_file_size.get().strip()

        if not titre or not auteur or not isbn:
            messagebox.showwarning("Champs manquants","Veuillez remplir tous les champs !")
        else :
            if not taille_fichier:
                self.bibliotheque.ajouter_livre(Livre(titre,auteur,isbn))
            else:
                self.bibliotheque.ajouter_livre(Livre_numerique(titre,auteur,isbn,int(taille_fichier)))
            messagebox.showinfo("Succès","Livre bien ajouté !")
            self.reinitialiser_entry_formulaire()

    def Rechercher_livre_par_auteur(self):
        auteur = self.entry_author_search.get().strip()
        if not auteur:
            messagebox.showwarning("Champs manquants","Veuillez remplir le champ de l'auteur pour pouvoir rechercher des livres!")
        else :
            print("Vous cherchez un ou plusieurs livres écrit dont l'auteur contient la chaine de caractère '"+auteur+"': ")
            print ("Résultat de la recherche: ")
            resultat_recherche=self.bibliotheque.rechercher_livre_par_auteur(auteur)
            if len(resultat_recherche)==0:
                messagebox.showinfo("Succès","La recherche n'a rien donné!")
            else:
                print ("La recherche a donné: ")
                for livre in resultat_recherche:
                    if (isinstance (livre,Livre_numerique)):
                        print ("-livre numérique: ",livre.Titre,", il a été écrit par ",livre.Auteur,"Son ISBN est: ",livre.ISBN," et sa taille est "+str(livre.tailleFichier))
                    elif isinstance (livre,Livre): 
                        print ("-livre non-numérique: ",livre.Titre,", il a été écrit par ",livre.Auteur,"Son ISBN est: ",livre.ISBN)
                messagebox.showinfo("Succès","Les résultats de votre recherche s'affichent dans la console")
            self.reinitialiser_entry_formulaire()
            print("-----------------------------------------------------")

    
    def reinitialiser_entry_formulaire(self):
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_isbn.delete(0, tk.END)
        self.entry_file_size.delete(0, tk.END)
        self.entry_author_search.delete(0, tk.END)


    def Exporter_data_csv(self):
        exporter_donnees_en_csv()
        messagebox.showinfo("Succès","Données bien exportées!")
        self.reinitialiser_entry_formulaire()

    def Fermer(self):
        self.fenetre.destroy()