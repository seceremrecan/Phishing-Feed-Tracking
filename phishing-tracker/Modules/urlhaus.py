from database_config import fetch_url_data, save_urls_to_db
from sqlalchemy.orm import Session as DBSession
from models import URL


def fetch_and_save_urlhaus_urls(db: DBSession, url: str):
    try:
        text_data = fetch_url_data(url)
        urls = text_data.split("\n")
        save_urls_to_db(db, urls, URL)
        print("UrlHaus URLs fetched and saved successfully")
    except Exception as e:
        print(f"Error: {str(e)}")