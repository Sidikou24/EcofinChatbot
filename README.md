## Description:
Le projet est une application web Python basée sur Flask qui scrape des articles du site Ecofin, les transforme en système de recherche basé sur les embeddings, et répond aux questions des utilisateurs en utilisant un modèle d'intelligence artificielle.

## Fonctionnalités principales
- Scraping des derniers articles du site Ecofin.
- Stockage des articles dans un fichier JSON.
- Recherche d'articles pertinents à l'aide de FAISS et des embeddings intégrés via LangChain.
- Génération des réponses via le LLM Gemini.
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


## Installation
Pré-requis
- Python 3.11.5
- Environnement virtuel Python (Recommandé)

## Instructions de configuration
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
   USER_AGENT=VotreUserAgent (Identifiant utilisé lors des requêtes HTTP. Une Chaine de caractère valide)
   API_KEY=VotreCleAPI (Obtenez votre propre clé sur https://aistudio.google.com/app/apikey?hl=fr)

## Utilisation
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
- Le modèle d'embedding utilisé est models/embedding-001.
  
Configuration du modèle
- Modèle : gemini-1.5-flash
- Température : 0.7 (pour un équilibre entre créativité et précision)

Traitement des données
- Chunking : 380 caractères par segment
- Chevauchement : 80 caractères

Architecture web
- Front-end : HTML/CSS/JS (dossier `templates` et `static`).
- Back-end : Flask pour les routes et l’API.
- Base de données vectorielle : FAISS pour les embeddings.

Gestion des erreurs
-Le fichier ecofin_scrap.py intègre un système de gestion des erreurs robuste basé sur Python logging. 
-Cela permet de suivre les activités, détecter les erreurs lors du scraping et des enregistrements JSON, et de prendre des actions correctives.

Exclusion Git
Le fichier `.gitignore` contient les éléments générés automatiquement et le file .env qui contient les informations sensibles

Limitations connues
-Les résultats dépendent des données disponibles dans les 10 derniers jours.
-Le scraping peut échouer si le site web Ecofin change son architecture ou bloque les requêtes automatiques.

## Contributeurs
- MAMANE DARI SIDIKOU (Auteur principal)

----------------------------------------------------------
Pour toute question, contactez-moi à sidikoudari@gmail.com.

