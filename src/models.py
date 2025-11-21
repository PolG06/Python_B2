#Modélisation d'une bibliothèque
from datetime import datetime,date
from src.file_manager import *
from src.exceptions import ErreurBibliotheque,ErreurLivre,ErreurLivreNumerique
class Bibliotheque:
    def __init__(self, nom:str):
        if not isinstance(nom, str) or not nom.strip():
            raise ErreurBibliotheque("Le nom de la bibliothèque doit être une chaîne non vide.",code_erreur=104)
        self.nom:str = nom
        self.liste_livres:list = []
        self.liste_emprunts=[]

    def ajouter_livre_dans_liste(self,livre):
        if not isinstance(livre,Livre):
            raise ErreurBibliotheque("Vous essayer d'ajouter autre chose qu'une instance de Livre ou de Livre_numerique dans la bibliothèque", code_erreur=101)
        self.liste_livres.append(livre)
    
    def ajouter_livre(self, livre):
        if not isinstance(livre,Livre):
            raise ErreurBibliotheque("Vous essayer d'ajouter autre chose qu'une instance de Livre ou de Livre_numerique dans la bibliothèque et dans le fichier json", code_erreur=102)
        self.ajouter_livre_dans_liste(livre)
        ajouter_livre_dans_json(livre)
            
    def importer_json(self):
        donnees=recup_donnees_json()
        importer_donnees_json(self,donnees)
            
    def supprimer_livre_par_ISBN(self, isbn:str):
        if not isinstance(isbn,str):
            raise ErreurBibliotheque("Vous essayer de supprimer autre chose qu'une instance de Livre ou de Livre_numerique de la bibliothèque", code_erreur=103)
        supprimer_livre_par_ISBN_dans_json(isbn)
        self.liste_livres=[livre for livre in self.liste_livres if livre.ISBN!=isbn]
        
    def rechercher_livre_par_titre(self, chaine:str):
        if not isinstance(chaine,str):
            raise ErreurBibliotheque("La chaine de recherche doit être un str", code_erreur=105)
        return [livre for livre in self.liste_livres if chaine in livre.titre]

    def rechercher_livre_par_auteur(self, chaine:str):
        if not isinstance(chaine,str):
            raise ErreurBibliotheque("La chaine de recherche doit être un str", code_erreur=105)
        return [livre for livre in self.liste_livres if chaine in livre.auteur]

    def ajouter_emprunt(self,utilisateur,livre,debut,fin):
        self.liste_emprunts.append(Emprunt(livre,utilisateur,debut,fin))
    
    def envoyer_notification_livre_dispo(self):
        for livre in self.liste_livres:
            for utilisateur in livre.utilisateur_interesse:
                #simulation d'envoi de mail
                print("Info pour "+utilisateur.nom+"Qui a l'adresse mail: "+utilisateur.adresse_mail+", Le livre que vous convoitiez: "+livre.titre+" est de nouveau disponible")

    def rendre_livre(self,livre,utilisateur,note=None,commentaire=None):
        for emprunt in self.liste_emprunts:
            if emprunt.livre==livre and emprunt.utilisateur==utilisateur:
                if note!=None or commentaire!=None:
                    emprunt.rendre_livre(utilisateur,note,commentaire)
                if emprunt.retard_rendu():
                    return emprunt.amande()
                else:
                    return 0
                
    def peut_etre_emprunte(self,livre,date_debut,date_fin)->bool:
        if isinstance(livre,Livre_numerique):
            return True
        else:
            debut_emprunt = datetime.strptime(date_debut, "%d/%m/%Y")
            fin_emprunt = datetime.strptime(date_fin, "%d/%m/%Y")

            compteur = 0

            for emprunt in self.liste_emprunts:
                debut_en_cours = datetime.strptime(emprunt.debut, "%d/%m/%Y")
                fin_en_cours = datetime.strptime(emprunt.fin, "%d/%m/%Y")
                # si chevauchement et le livre n'a pas encore été rendu alors que cela aurait du
                if debut_emprunt <= fin_en_cours and fin_emprunt >= debut_en_cours:
                    compteur += 1
                elif (fin_en_cours<datetime.today() and not emprunt.est_rendu):
                    compteur+=1
            return compteur < livre.nombre_exemplaires
                    
    def emprunter_livre(self, utilisateur, livre, date_debut, date_fin):
        pouvoir_emprunter=True
        date_debut_dt = datetime.strptime(date_debut, "%d/%m/%Y")
        date_fin_dt = datetime.strptime(date_fin, "%d/%m/%Y")

        if utilisateur.livres_empruntes_ce_mois >= utilisateur.livres_par_mois:
            print("Cet utilisateur emprunté tous vos livres ce mois-ci, veuillez revenir le mois prochain.")
            pouvoir_emprunter=False

        for l in utilisateur.livres_empruntes:
            emprunt_start = datetime.strptime(l[1][0], "%d/%m/%Y")
            emprunt_end = datetime.strptime(l[1][1], "%d/%m/%Y")
            if (date_debut_dt <= emprunt_end and date_fin_dt >= emprunt_start):
                print(utilisateur.nom+" ne peut pas emprunter 2 livres en même temps.")
                pouvoir_emprunter=False
            
            for emprunt in self.liste_emprunts:
                if emprunt.utilisateur==utilisateur and emprunt.livre==livre and not emprunt.est_rendu:
                    pouvoir_emprunter=False

        if not self.peut_emprunter(livre,date_debut,date_fin):
            print ("Tous les exemplaires de ce livre ont été réservés, vous ne pouvez pas effectuer cette reservation")
            pouvoir_emprunter=False

        if pouvoir_emprunter:
            if self in livre.utilisateur_interesse:
                livre.utilisateur_interesse.remove(utilisateur)

            self.ajouter_emprunt(utilisateur,livre,date_debut,date_fin)
            utilisateur.livres_empruntes.append((livre, (date_debut, date_fin)))
            ajouter_livre_emprunte(utilisateur, livre, date_debut, date_fin,False)
            utilisateur.livres_empruntes_ce_mois+=1
            print(utilisateur.nom+" a emprunté le livre du "+date_debut+" au "+date_fin)
        else:
            print("Vous recevrez un mail quand le produit sera de nouveau disponible")
            livre.utilisateur_interesse.append(utilisateur)
             
    def afficher(self):
        return (self.nom, self.liste_livres)

#Modélisation d'une classe livre
class Livre:
    Compteur=0
    def __init__(self,titre:str,auteur:str,ISBN:str,nombre_exemplaires:int,categorie:str):
        if not isinstance(titre, str) or not titre.strip():
            raise ErreurLivre("Le titre doit être une chaîne non vide.",code_erreur=101)
        if not isinstance(auteur, str) or not auteur.strip():
            raise ErreurLivre("L'auteur doit être une chaîne non vide.",code_erreur=102)
        if not isinstance(ISBN, str) or not ISBN.strip():
            raise ErreurLivre("L'ISBN doit être une chaîne non vide.",code_erreur=103)
        self.titre=titre
        self.auteur=auteur
        self.ISBN=ISBN
        self.utilisateur_interesse=[]
        self.nombre_exemplaires=nombre_exemplaires
        self.categorie=categorie
        self.retours=[]
        Livre.Compteur+=1
        self.Id=Livre.Compteur

    def ajouter_retour(self,utilisateur,note=None,commentaire=None):
        self.retours.append((utilisateur,note,commentaire))
    
    
#Modélisation d'une classe livre numérique
class Livre_numerique(Livre):
    def __init__(self,titre:str,auteur:str,ISBN:str,taille_fichier:int,categorie:str):
        if not isinstance(taille_fichier, int) or taille_fichier<0:
            raise ErreurLivreNumerique("La taille du fichier doit être un entier positif (int>=0) .",code_erreur=101)
        super().__init__(titre,auteur,ISBN,None,categorie)
        self._taille_fichier:int=taille_fichier

    @property
    def tailleFichier(self)->int:
        return self._taille_fichier
    
class Utilisateur():
    Compteur=0
    def __init__(self,nom,mdp,adresse_mail):
        self.Nom=nom
        self.MDP=mdp
        self.adresse_mail=adresse_mail
        self.IsAdmin=False
        self.livres_empruntes=[]
        self.livres_empruntes_ce_mois=0
        self.livres_par_mois=5
        self.penalite=0
        Utilisateur.Compteur+=1
        self.Id=Utilisateur.Compteur
    
    def promouvoir(self):
        if not self.IsAdmin:
            self.IsAdmin=True
            self.livres_par_mois*=2

    def enregistrer_utilisateur_dans_json(self):
        ajouter_utilisateur_dans_json(self)

    def reset_livres_empruntes_ce_mois(self):
        self.livres_empruntes_ce_mois=0


class Emprunt ():
    def __init__(self,livre,utilisateur,debut,fin):
        self.livre=livre
        self.utilisateur=utilisateur
        self.debut=debut
        self.fin=fin
        self.est_rendu=False
    
    def retard_rendu(self):
        fin_emprunt = datetime.strptime(self.fin, "%d/%m/%Y")
        return fin_emprunt.date() < date.today() and not self.est_rendu
    
    def rendre_livre(self):
        self.est_rendu=True
    
    def amande(self):
        if self.retard_rendu():
            emprunt_end = datetime.strptime(self.fin, "%d/%m/%Y")
            date_ajd= date.today()
            return ((date_ajd-emprunt_end.date()).days)/2

        



        




        
