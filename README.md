# Phishing-Feed-Tracking

This project is designed to track sources that share phishing feeds. It involves researching and identifying sources that share phishing data, followed by storing this information in a database. The project is built using FastAPI and PostgreSQL and is managed with Poetry for dependency management.

## Project Objectives

- Research and identify sources sharing phishing feeds.
  
- Continuously monitor and track these sources for new phishing data.
  
- Store information about these sources in a PostgreSQL database.
  
- Implement this project without the need for a while loop or continuous polling.

## Technologies Used

- Poetry (https://python-poetry.org/docs/)
  
- Docker Compose
  
- FastAPI (https://fastapi.tiangolo.com/)
  
- SQLAlchemy ORM (https://docs.sqlalchemy.org/)
  
- PostgreSQL

## Running the Project

1. Clone this repository: `git clone https://github.com/your-username/phishing-feed-tracker.git`.
2. Start the project using Docker Compose: `docker-compose up --build`.
3. The FastAPI web application should now be running at `http://localhost:8000`.
4. Before you start working on the project, you can use Poetry to install the required Python dependencies: `poetry install`.

## Usage

The project offers the following functionality:

-> Source Tracking: The system continuously monitors and tracks sources sharing phishing feeds, storing relevant information in a PostgreSQL database.

## Database Schema

The database schema includes the following tables:

-> Sources: Stores information about the sources that share phishing data, including source name, URL, and other relevant details.

-> Phishing Feeds: Contains details about the phishing feeds shared by different sources, including feed URL, timestamp, and other metadata.

-> Events: Logs events related to source tracking, allowing you to review the history of source interactions.
