import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import time
import random
import os
from pathlib import Path
import logging

class EcofinScraper:
    def __init__(self, data_path='data/articles_ecofin_x_derniers_jours.json', 
                 scrape_interval_hours=12, days_back=4):
        """
        Initialise le scraper Ecofin
        
        Args:
            data_path (str): Chemin de sauvegarde du fichier JSON
            scrape_interval_hours (int): Intervalle entre deux sessions de scraping (en heures)
            days_back (int): Nombre de jours à remonter pour le scraping
        """
        self.base_url = "https://www.agenceecofin.com"
        self.search_url = f"{self.base_url}/a-la-une/recherche-article/articles"
        
        # Configuration du scraping
        self.days_back = days_back
        self.scrape_interval_hours = scrape_interval_hours
        
        # Configuration des chemins
        self.data_path = Path(data_path)
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def needs_scraping(self):
        """
        Vérifie si un nouveau scraping est nécessaire
        
        Returns:
            bool: True si un scraping est requis, False sinon
        """
        # Si le fichier n'existe pas, on doit scraper
        if not self.data_path.exists():
            self.logger.info("Fichier JSON inexistant. Scraping nécessaire.")
            return True
        
        # Vérifier la date de dernière modification
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(self.data_path))
        time_since_last_scrape = datetime.now() - file_modified_time
        
        # Scraper si le fichier est plus vieux que l'intervalle
        needs_update = time_since_last_scrape > timedelta(hours=self.scrape_interval_hours)
        
        if needs_update:
            self.logger.info(f"Données obsolètes. Dernière mise à jour : {file_modified_time}")
        
        return needs_update

    def parse_french_date(self, date_str):
        """
        Convertit une date au format français en objet datetime
        
        Args:
            date_str (str): Date au format français
        
        Returns:
            datetime: Date parsée ou None
        """
        date_str = date_str.lower().strip()
        today = datetime.now()

        months_translation = {
            'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
            'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
            'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
        }

        try:
            if '/' in date_str:
                day, month, year = map(int, date_str.split('/'))
                return datetime(year, month, day)

            elif date_str == "aujourd'hui":
                return today

            elif date_str == "hier":
                return today - timedelta(days=1)

            else:
                for month_name, month_num in months_translation.items():
                    if month_name in date_str:
                        parts = date_str.split()
                        day = int(parts[0])
                        year = int(parts[-1]) if len(parts) > 2 else today.year
                        return datetime(year, month_num, day)

        except Exception as e:
            self.logger.error(f"Erreur de parsing de date: {date_str} - {e}")
            return None

    def scrape_articles(self):
        """
        Scrape les articles d'Ecofin des derniers jours
        
        Returns:
            list: Liste des articles scrapés
        """
        all_articles_data = []
        current_page = 0
        ten_days_ago = datetime.now() - timedelta(days=self.days_back)

        self.logger.info(f"Début du scraping pour les articles depuis {ten_days_ago}")

        while True:
            params = {
                'submit_x': '0',
                'submit_y': '0',
                'filterTousLesFils': 'Tous',
                'filterCategories': 'Sous-rubrique',
                'filterFrench': 'French',
                'userSearch': '1',
                'testlimitstart': current_page * 20
            }

            try:
                time.sleep(random.uniform(1, 3))
                response = requests.get(self.search_url, params=params)
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('table', class_='ts')

                found_recent_articles = False

                for article in articles:
                    try:
                        link = self.base_url + article.find('h3', class_='r').find('a')['href']
                        date_elem = article.find('span', class_='f nsa')
                        
                        if date_elem:
                            date_str = date_elem.text.strip()
                            article_date = self.parse_french_date(date_str)

                            if article_date and article_date >= ten_days_ago:
                                time.sleep(random.uniform(1, 3))
                                article_response = requests.get(link)
                                article_soup = BeautifulSoup(article_response.text, 'html.parser')

                                title = article_soup.find('h1', class_='itemTitle').text.strip()
                                content_div = article_soup.find('div', class_='itemIntroText')
                                content = ' '.join([p.text.strip() for p in content_div.find_all('p', class_='texte')])

                                article_data = {
                                    'titre': title,
                                    'contenu': content,
                                    'date_publication': date_str,
                                    'lien': link
                                }

                                all_articles_data.append(article_data)
                                found_recent_articles = True

                                self.logger.info(f"Article ajouté - Titre: {title}, Date: {date_str}")

                    except Exception as e:
                        self.logger.error(f"Erreur lors du traitement d'un article: {e}")

                if not found_recent_articles:
                    break

                current_page += 1

            except Exception as e:
                self.logger.error(f"Erreur lors de la récupération de la page {current_page}: {e}")
                break

        # Enregistrer les données dans un fichier JSON
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(all_articles_data, f, ensure_ascii=False, indent=4)
            
            self.logger.info(f"Total d'articles traités : {len(all_articles_data)}")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'enregistrement du fichier JSON : {e}")

        return all_articles_data

    def get_articles(self):
        """
        Récupère les articles, avec scraping conditionnel
        
        Returns:
            list: Liste des articles
        """
        if self.needs_scraping():
            self.scrape_articles()
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture du fichier JSON : {e}")
            return []

def main():
    scraper = EcofinScraper()
    articles = scraper.get_articles()
    print(f"Nombre d'articles chargés : {len(articles)}")

if __name__ == "__main__":
    main()