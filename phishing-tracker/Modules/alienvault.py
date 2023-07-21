import requests
from bs4 import BeautifulSoup
from database_config import fetch_url_data, save_urls_to_db
from sqlalchemy.orm import Session
from models import URL
from database_config import SessionLocal

url = "https://otx.alienvault.com/browse/global/indicators?include_inactive=0&sort=-modified&page=8&limit=100000&indicatorsSearch=role:%22phishing%22&type=URL"

def scrape_and_save_urls():
    """
    Scrape URLs from the webpage and save them to the database.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        urls = []

        # Find all the URLs from the page
        for link in soup.find_all("a", href=True):
            urls.append(link["href"])

        # Filter out non-URLs and duplicates
        urls = list(set(filter(lambda u: u.startswith("http") or u.startswith("https"), urls)))

        # Save URLs to the database
        db = SessionLocal()
        save_urls_to_db(db, urls, URL)
        db.close()

        print("URLs fetched and saved to the database successfully.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")