from flask import Blueprint, render_template, request, jsonify
from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
import json
import os
import logging
from pathlib import Path
from .scrap.ecofin_scrap import EcofinScraper

logging.basicConfig(level=logging.INFO)

main = Blueprint('main', __name__)

class EcofinChatbot:
    def __init__(self, data_path='data/articles_ecofin_10_derniers_jours.json'):
        self.data_path = Path(data_path)
        self.setup_retrieval_system()

    def setup_retrieval_system(self):
        # Vérifier si le fichier existe, sinon scraper
        if not self.data_path.exists():
            scraper = EcofinScraper()
            scraper.scrape_articles()

        # Charger les articles
        with open(self.data_path, "r", encoding="utf-8") as f:
            articles = json.load(f)

        # Convertir en documents LangChain
        documents = []
        for article in articles:
            doc_content = f"{article['titre']} {article['contenu']}"
            documents.append(Document(
                page_content=doc_content,
                metadata={
                    "titre": article["titre"],
                    "date_publication": article["date_publication"],
                    "lien": article["lien"]
                }
            ))

        # Diviser les documents en chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=380, chunk_overlap=80)
        chunks = text_splitter.split_documents(documents)

        # Générer des embeddings
        gemini_embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            headers={'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0')}
        )

        # Créer le vectorstore
        self.vectorstore = FAISS.from_documents(chunks, gemini_embeddings)
        self.retriever = self.vectorstore.as_retriever()

        # Initialiser le LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

        # Prompt Template
        self.prompt_template = """Tu es un assistant spécialisé dans les actualités africaines du site Ecofin. 
Tu couvre l'actualité de 9 secteurs africains : 
gestion publique, finance, télécoms, agro, électricité, mines, hydrocarbures, communication et formation. 
Basé sur les articles que tu as en ta possession et sur tes connaissances natives, réponds à la question de l'utilisateur avec :
- Titre de l'article
- Résumé ou réponse adaptée à la question
- Date de publication
- Lien vers l'article

Articles contextuels: {context}

Question utilisateur: {question}

Réponse:"""

        self.prompt = PromptTemplate.from_template(self.prompt_template)

    def generate_response(self, user_message):
        try:
            results = self.retriever.invoke(user_message)
            logging.info(f"Nombre de documents pertinents trouvés : {len(results)}")

            context = "\n\n".join([
                f"Titre: {res.metadata.get('titre', 'Titre inconnu')}\n"
                f"Date: {res.metadata.get('date_publication', 'Date inconnue')}\n"
                f"Lien: {res.metadata.get('lien', 'Lien non disponible')}\n"
                f"Contenu: {res.page_content[:500]}"
                for res in results
            ])

            prompt_text = self.prompt.format(context=context, question=user_message)
            response = self.llm.invoke([
                SystemMessage(content=prompt_text),
                HumanMessage(content=user_message)
            ])

            return response.content

        except Exception as e:
            logging.error(f"Erreur lors du traitement de la requête : {e}")
            return f"Désolé, une erreur s'est produite : {e}"

chatbot = EcofinChatbot()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            logging.warning("Message non fourni dans la requête.")
            return jsonify({'error': 'Message non fourni'}), 400

        logging.info(f"Message reçu : {user_message}")
        response = chatbot.generate_response(user_message)
        logging.info("Réponse générée avec succès.")
        
        return jsonify({'response': response})

    except Exception as e:
        logging.error(f"Erreur lors du traitement de la requête : {e}")
        return jsonify({'error': str(e)}), 500