import os
import csv
import configparser
import logging
import requests
from requests import Session


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from models import Base

config = configparser.ConfigParser()
config.read(".env")

db_host = os.getenv("DB_HOST", config["database"]["host"])
db_user = os.getenv("DB_USER", config["database"]["user"])
db_password = os.getenv("DB_PASSWORD", config["database"]["password"])
db_name = os.getenv("DB_NAME", config["database"]["database"])
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Session()


def fetch_url_data(url):
    """
    Fetches data from the given URL.

    Args:
        url (str): URL to fetch data from.

    Returns:
        str: Fetched data.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch URL data")


def save_urls_to_db(db: Session, urls, model):
    """
    Updates the URLs in the database.

    Args:
        db (Session): Database session.
        urls (list): URLs to be updated.
        model (Base): Database model.
    """
    existing_urls = db.query(model).filter(model.url.in_(urls)).all()
    existing_url_set = set(url.url for url in existing_urls)
    new_urls = list(set(urls) - existing_url_set)
    
    if new_urls:
        db.bulk_save_objects([model(url=url) for url in new_urls])
        db.commit()





def fetch_and_save_urls(db: Session, url, model, success_message):
    """
    Fetches data from the given URL and saves the URLs to the database.

    Args:
        db (Session): Database session.
        url (str): URL to fetch data from.
        model (Base): Database model.
        success_message (str): Success message after saving.
    """
    try:
        text_data = fetch_url_data(url)
        urls = text_data.split("\n")
        save_urls_to_db(db, urls, model)
        logging.info(success_message)
    except Exception as e:
        logging.error(f"Error: {str(e)}")

     
def fetch_and_save_urls_csv(db: Session, url: str, model: Base, success_message: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        csv_data = response.text.split("\n")
        rows = [row.split(",") for row in csv_data[1:] if row]
        urls = [row[1] for row in rows]
        save_urls_to_db(db, urls, model)
        logging.info(success_message)
    except Exception as e:
        logging.error(f"Error: {str(e)}")



def fetch_and_save_urls_csv_phishstats(db: Session, url: str, model: Base, success_message: str):
    response = requests.get(url)
    csv_data = response.text.strip().split('\n')[6:]  # Header'ı ve gereksiz satırları atlıyoruz

    urls = []

    # CSV içeriğini döngüyle oku ve sadece http ile başlayan URL'leri al
    reader = csv.reader(csv_data, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) >= 3:
            url = row[2].strip()
            if url.startswith('http'):
                urls.append(url)

    #print(urls)
    save_urls_to_db(db, urls, model)  # Veritabanına kaydetme işlemi

    print(success_message)
