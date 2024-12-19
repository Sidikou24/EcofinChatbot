Description:
Le projet est une application web Python basée sur Flask qui scrape des articles du site Ecofin, les transforme en système de recherche basé sur les embeddings, et répond
aux questions des utilisateurs en utilisant un modèle d'intelligence artificielle.

Fonctionnalités principales
- Scraping des derniers articles du site Ecofin.
- Stockage des articles dans un fichier JSON.
- Recherche d'articles pertinents à l'aide de FAISS et des embeddings LangChain.
- Interface utilisateur construite avec Flask.

## Structure du Projet

HiringChallenge/
├── app/
│   ├── scrap/
│   │   ├── ecofin_scrap.py  # Scraping des articles Ecofin.
│   │   ├── __init__.py      # Fichier vide pour le package.
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Style CSS.
│   │   ├── js/
│   │       └── script.js   # Interactions JavaScript.
│   ├── templates/
│   │   └── index.html       # Page HTML principale.
│   ├── __init__.py          # Initialisation du package Flask.
│   └── routes.py            # Définition des routes Flask.
├── data/                    # Stockage des articles (généré automatiquement).
├── ecofinDB.faiss           # Base de données FAISS pour la recherche.
├── .env                     # Variables d'environnement sensibles.
├── config.py                # Configuration de l'application.
├── requierments.txt         # Liste des dépendances.
├── run.py                   # Point d'entrée pour démarrer l'application Flask.
├── .gitignore               # Fichiers/dossiers à exclure du dépôt.


##Installation
Pré-requis
- Python 3.11.5
- Environnement virtuel Python (Recommandé)

Instructions de configuration
1. Clonez le dépôt :
   git clone https://github.com/Sidikou24/EcofinChatbot.git
   cd HiringChallenge
  

2. Créez et activez un environnement virtuel (avec conda ou pip):
   (Perso avec conda)
   conda create --name ecofin
   conda activate ecofin

3. Installez les dépendances (parfois il est necessaire d'installer les dépendances une par une) :
   pip install -r requierments.txt
   

4. Configurez les variables d'environnement dans un fichier `.env` :
   USER_AGENT=VotreUserAgent
   API_KEY=VotreCleAPI (créez un compte 

Utilisation
Exécuter l’Application
1. Lancez l'application Flask :
   python run.py

2. Accédez à l'application dans un navigateur :
   http://127.0.0.1:5000

3. Posez une question sur un des secteur couvert ou demandez simplement au chatbot "Comment peux tu m'aider?"


## Techniques

Scraping
Le fichier `ecofin_scrap.py` :
- Utilise BeautifulSoup pour scraper les articles Ecofin.
- Sauvegarde les articles sous forme JSON.

Architecture Rag 
- Les articles sont convertis en embeddings avec LangChain et FAISS pour la recherche des passages pertinants.
- Le modèle d'embedding utilisé est Google Generative AI.

Architecture
- Front-end : HTML/CSS/JS (dossier `templates` et `static`).
- Back-end : Flask pour les routes et l’API.
- Base de données vectorielle : FAISS pour les embeddings.

Exclusion Git
Le fichier `.gitignore` contient les éléments générés automatiquement et le file .env qui contient les informations sensibles

Contributeurs
- MAMANE DARI SIDIKOU (Auteur principal)

----------------------------------------------------------
Pour toute question, contactez-moi à sidikoudari@gmail.com.

