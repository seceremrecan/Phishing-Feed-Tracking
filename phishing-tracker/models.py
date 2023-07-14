from sqlalchemy import Column, String,Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PhishingURL(Base):
    __tablename__ = "phishing_urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)



class UsomURL(Base):
    __tablename__ = "usom_urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)    
