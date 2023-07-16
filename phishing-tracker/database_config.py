import os
import configparser
import logging
import requests

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
    existing_urls = db.query(model).all()
    existing_url_set = set(url.url for url in existing_urls)
    new_urls = [url for url in urls if url not in existing_url_set]
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

def fetch_and_save_urls_json(db: Session, url: str, model: Base, success_message: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        urls = [entry['url'] for entry in data]

        save_urls_to_db(db, urls, model)
        logging.info(success_message)
    except Exception as e:
        logging.error(f"Error: {str(e)}")        
