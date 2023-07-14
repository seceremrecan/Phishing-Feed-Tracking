from fastapi import FastAPI


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, PhishingURL, UsomURL
from database_config import DATABASE_URL, fetch_and_save_urls,SessionLocal


engine = create_engine(DATABASE_URL)
session=SessionLocal()

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


fetch_and_save_urls(
    session,
    "https://openphish.com/feed.txt",
    PhishingURL,
    "Phishing URLs fetched and saved successfully"
)

fetch_and_save_urls(
    session,
    "https://www.usom.gov.tr/url-list.txt",
    UsomURL,
    "USOM URLs fetched and saved successfully"
)
