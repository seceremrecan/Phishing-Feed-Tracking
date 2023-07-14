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
    Saves the given URLs to the database.

    Args:
        db (Session): Database session.
        urls (list): URLs to be saved.
        model (Base): Database model.
    """
    db.query(model).delete()
    unique_urls = set(urls)
    db.bulk_save_objects([model(url=url) for url in unique_urls])
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
