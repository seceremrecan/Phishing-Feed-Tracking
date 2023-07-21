import os
import configparser
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as DBSession
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
    response = Session().get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch URL data")


def save_urls_to_db(db: DBSession, urls, model):
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
        url_objects = [model(url=url) for url in new_urls]
        db.bulk_save_objects(url_objects)
        db.commit()
        print(f"{len(url_objects)} new URLs added to the database.")