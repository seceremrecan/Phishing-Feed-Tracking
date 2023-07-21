import csv
from database_config import fetch_url_data, save_urls_to_db
from sqlalchemy.orm import Session as DBSession
from models import URL


def fetch_and_save_phishstats_urls(db: DBSession, url: str):
    try:
        text_data = fetch_url_data(url)
        csv_data = text_data.strip().split("\n")[
            6:
        ]  # Headerı ve gereksiz satırları geçiyorum

        urls = []
        # CSV içeriğini döngüyle oku ve sadece http ile başlayan URLleri al
        reader = csv.reader(csv_data, delimiter=",", quotechar='"')
        for row in reader:
            if len(row) >= 3:
                url = row[2].strip()
                if url.startswith("http"):
                    urls.append(url)

        save_urls_to_db(db, urls, URL)  # Veritabanına kaydetme işlemi

        print("Phishstats URLs fetched and saved successfully")
    except Exception as e:
        print(f"Error: {str(e)}")