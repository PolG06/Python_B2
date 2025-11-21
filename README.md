--Gestion d'une bibliothèque avec python, avec plusieurs fonctionnalités--

--À propos:--

Il s'agit de mon projet de la fin de mon module python de ma 2ème année de Bachelor en Informatique, ce projet est l'aboutissement d'une semaine d'apprentissage. Le but de ce fichier est de gérer une bibliothèque de livres:

--Fonctionnalités principales:--
- Ajout, suppression et recherche de livres
- Utilisation de POO et du principe d'héritage
- Sauvegarde automatique dans un fichier JSON
- Export des données en CSV
- Tests unitaires complets avec pytest et couverture de code

--Dans le fichier, a été créé un environnement virtuel pour simplifier la manipulation et l'importation d'autres fichiers externes --

--Comment cela a été fait:--
#permet de créer le fichier de l'environnement virtuel
python -m venv mon_env   
#pour l'activer: 
#sur Windows:
mon_env\Scripts\activate
#sur MacOs/Linux:
source venv/bin/activate

--Prérequis--
python (version supérieure ou égale à la 3.13)
bibliothèque pytest (version supérieure ou égale à la 9.0.1)
bibliothèque pytest-cov (version supérieure ou égale à la 7.0.0)


--Comment utiliser le projet:--

1-Dans un terminal, entrer la commande: git clone https://github.com/PolG06/Python_B2
2-installer les bibliothèques et logiciels conformément au fichier requirement.txt
3-Ouvrir et lancer le fichier main grâce à un IDE qui supporte python (Je recommande VSCode)

--Structure du projet:--
.
├── main.py                  → Point d'entrée de l'application
├── requirements.txt         → Dépendances Python (prérequis à avoir pour lancer le projet)
├── .coverage
├── data/                    → Fichiers de données     
├── src/                     → Classes, Méthodes, Fonctions du projet
├── tests/                   → Fichiers de test
├── mon_env/                 → Environnement virtuel que l'on a créé
└── README.md

--pour lancer les tests, dans un terminal, aller à la racine du projet et taper: python -m pytest --cov tests

--Construit avec VSCode--