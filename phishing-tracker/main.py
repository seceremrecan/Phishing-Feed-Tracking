from fastapi import FastAPI
import os
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, URL
from database_config import DATABASE_URL, SessionLocal
from Modules import usom,urlhaus,phishtank,openphish,alienvault,alienvault_f21,Github_Daniel_Lopez
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler


engine = create_engine(DATABASE_URL)

session = SessionLocal()

config = configparser.ConfigParser()
config.read("/home/emre/Desktop/phishing-tracker/.env")

# FastAPI application
app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()


@app.on_event("startup")
def startup():
    """
    Creates database tables on application startup.
    """
    Base.metadata.create_all(bind=engine)

    # Zamanlanmış görevleri oluştur
    scheduler.add_job(fetch_and_save_data, "interval", hours=1)


def fetch_and_save_data():
    """
    Fetch and save data from different sources.
    """
    
    # Diğer fetch_and_save fonksiyonları buraya ekleyin
    usom.fetch_and_save_usom_urls(session, os.getenv("USOM_URL", config["urls"]["usom_url"]))
    urlhaus.fetch_and_save_urlhaus_urls(session, os.getenv("URLHAUS_URL", config["urls"]["urlhaus_url"]))
    openphish.fetch_and_save_openphish_urls(session, os.getenv("OpenPhish_URL", config["urls"]["openphish_url"]))
    alienvault.fetch_and_save_alienvault_urls(session,os.getenv("AlienVault_URL", config["urls"]["alienvault_url"]))
    alienvault_f21.fetch_and_save_alienvault_f21_urls(session,os.getenv("AlienVault_F21_URL", config["urls"]["alienvault_f21_url"]))
    Github_Daniel_Lopez.fetch_and_filter_github_daniel_urls(session,os.getenv("Github_Daniel_Lopze_URL", config["urls"]["github_daniel_lopez_url"]))

@app.get("/")
def root():
    """
    Handles the root path.

    Returns:
        dict: Success message.
    """
    return {"message": "GET request successfully processed."}



@app.get("/all_urls")
def get_all_urls():
    """
    Retrieves all URLs from different sources.

    Returns:
        dict: Response containing all URLs from different sources.
    """
    try:
        db = SessionLocal()

        # Get USOM URLs
        usom_urls = db.query(URL).all()

        # Get Phishtank URLs (or other sources)
        phishtank_urls = db.query(URL).all()
        # Get UrlHaus URLs
        urlhaus_urls=db.query(URL).all()

        # Get PhishStats URLs
        #phishstats_urls=db.query(URL).all()
        # Get OpenPhish URLs
        openphish_urls=db.query(URL).all()
        # Add more queries for other sources if needed
        alienvault_urls=db.query(URL).all()
        

        return {
            "usom_urls": [url.url for url in usom_urls],
            "phishtank_urls": [url.url for url in phishtank_urls],  #md5 sorunu var onu çöz 
            "urlhaus_urls":[url.url for url in urlhaus_urls],
            "openphish_urls":[url.url for url in openphish_urls],
            "alienvault_urls": [url.url for url in alienvault_urls],
            # Add more keys and values for other sources if needed
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred"})


usom.fetch_and_save_usom_urls(
    session,
    os.getenv("USOM_URL", config["urls"]["usom_url"])
)
urlhaus.fetch_and_save_urlhaus_urls(
    session,
    os.getenv("URLHAUS_URL", config["urls"]["urlhaus_url"])
)
openphish.fetch_and_save_openphish_urls(
    session,
    os.getenv("OpenPhish_URL", config["urls"]["openphish_url"])
)
alienvault.fetch_and_save_alienvault_urls(
    session,
    os.getenv("AlienVault_URL", config["urls"]["alienvault_url"])
)
alienvault_f21.fetch_and_save_alienvault_f21_urls(
    session,
    os.getenv("AlienVault_F21_URL", config["urls"]["alienvault_f21_url"])
)
Github_Daniel_Lopez.fetch_and_filter_github_daniel_urls(
    session,
    os.getenv("Github_Daniel_Lopez_URL", config["urls"]["github_daniel_lopez_url"])
)


