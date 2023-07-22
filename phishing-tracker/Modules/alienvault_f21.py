import requests
from database_config import save_urls_to_db
from sqlalchemy.orm import Session as DBSession
from models import URL


def fetch_and_save_alienvault_f21_urls(db: DBSession, url: str):
    """
    Fetches all the HTTP and HTTPS URLs from the given URL.

    Args:
        url (str): The API URL to fetch the data from.

    Returns:
        list: List of HTTP and HTTPS URLs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Verileri alıp HTTP ve HTTPS ile başlayan URL'leri filtreliyoruz
        urls = [entry['indicator'] for entry in data['results'] if entry['indicator'].startswith('http://') or entry['indicator'].startswith('https://')]
        print("AlienVault_F21 URLs fetched and saved successfully")
        save_urls_to_db(db, urls, URL)
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Hata: {e}")
        return []
