import requests
import csv
from urllib.parse import urlparse
from database_config import save_urls_to_db
from sqlalchemy.orm import Session as DBSession
from models import URL

def fetch_and_filter_github_daniel_urls(db: DBSession, url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        urls = []

        # CSV verisini çözerek doğru URL'leri alıyoruz
        reader = csv.reader(response.text.strip().split('\n'))
        for row in reader:
            timestamp, user, url_type, url, tags, tweet_url = row
            parsed_url = urlparse(url)
            if parsed_url.scheme in ['http', 'https']:
                urls.append(url)
        print("Github_Daniel_Lopez URLs fetched and saved successfully")        
        save_urls_to_db(db, urls, URL)
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Hata: {e}")
        return []
