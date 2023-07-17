from fastapi import FastAPI
import os
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, PhishingURL, UsomURL, PhishtankURL,UrlHaus,PhishStatsURL
from database_config import DATABASE_URL, fetch_and_save_urls, SessionLocal, fetch_and_save_urls_csv,fetch_and_save_urls_csv_phishstats

engine = create_engine(DATABASE_URL)


session = SessionLocal()

config = configparser.ConfigParser()
config.read(".env")


# FastAPI application
app = FastAPI()


@app.on_event("startup")
def startup():
    """
    Creates database tables on application startup.
    """
    Base.metadata.create_all(bind=engine)


@app.post("/phishing")
def create_phishing_url(url: str):
    """
    Creates a new phishing URL.

    Args:
        url (str): URL to be created.

    Returns:
        dict: Success message.
    """
    db = SessionLocal()
    phishing_url = PhishingURL(url=url)
    db.add(phishing_url)
    db.commit()
    db.refresh(phishing_url)
    return {"message": "Phishing URL created successfully"}


@app.get("/")
def root():
    """
    Handles the root path.

    Returns:
        dict: Success message.
    """
    return {"message": "GET request successfully processed."}


@app.get("/phishing")
def get_phishing_urls():
    """
    Retrieves phishing URLs.

    Returns:
        dict: Response containing phishing URLs.
    """
    db = SessionLocal()
    urls = db.query(PhishingURL).all()
    return {"phishing_urls": [url.url for url in urls]}


@app.get("/usom")
def get_usom_urls():
    """
    Retrieves USOM URLs.

    Returns:
        dict: Response containing USOM URLs.
    """
    db = SessionLocal()
    urls = db.query(UsomURL).all()
    return {"usom_urls": [url.url for url in urls]}

@app.get("/urlhaus")
def get_urlhaus_urls():
    """
    Retrieves USOM URLs.

    Returns:
        dict: Response containing USOM URLs.
    """
    db = SessionLocal()
    urls = db.query(UrlHaus).all()
    return {"urlhaus": [url.url for url in urls]}


@app.get("/phishtank")
def get_phishtank_urls():
    """
    Retrieves Phishtank URLs.

    Returns:
        dict: Response containing Phishtank URLs.
    """
    db = SessionLocal()
    urls = db.query(PhishtankURL).all()
    return {"phishtank": [url.url for url in urls]}

@app.get("/phishstats")
def get_phishstats_urls():
    """
    Retrieves PhishStats URLs.

    Returns:
        dict: Response containing PhishStats URLs.
    """
    db = SessionLocal()
    urls = db.query(PhishStatsURL).all()
    return {"phishstats": [url.url for url in urls]}


fetch_and_save_urls(
    session,
    os.getenv("OpenPhish_URL", config["urls"]["openphish_url"]),
    PhishingURL,
    "Phishing URLs fetched and saved successfully"
)
fetch_and_save_urls(
    session,
    os.getenv("URLHAUS_URL", config["urls"]["urlhaus_url"]),
    UrlHaus,
    "UrlHaus URLs fetched and saved successfully"
)

fetch_and_save_urls(
    session,
    os.getenv("USOM_URL", config["urls"]["usom_url"]),
    UsomURL,
    "USOM URLs fetched and saved successfully"
)

fetch_and_save_urls_csv_phishstats(
    session,
    os.getenv("PhishStats_URL", config["urls"]["phishstats_url"]),
    PhishStatsURL,
    "PhishStats URLs fetched and saved successfully"
)

fetch_and_save_urls_csv(
    session,
    os.getenv("PhishTank_URL", config["urls"]["phishtank_url"]),
    PhishtankURL,
    "Phishtank URLs fetched and saved successfully"
)
