import logging
from database_config import  save_urls_to_db
from sqlalchemy.orm import Session as DBSession
from models import URL
import requests


def fetch_and_save_phishtank_csv(db: DBSession, url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        csv_data = response.text.split("\n")
        rows = [row.split(",") for row in csv_data[1:] if row]
        urls = [row[1][:1000] for row in rows]  # URL'leri 1000 karakterle sınırlıyoruz

        # Bölümleri belirleyin, örneğin her seferinde 1000 kayıt ekleyebilirsiniz.
        chunk_size = 1000
        for i in range(0, len(urls), chunk_size):
            chunk = urls[i : i + chunk_size]
            save_urls_to_db(db, chunk, URL)

        logging.info("Phishtank URLs fetched and saved successfully")
    except Exception as e:
        logging.error(f"Error: {str(e)}")