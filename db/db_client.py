import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

HOST = os.getenv("DB_MOVIES_HOST")
PORT = os.getenv("DB_MOVIES_PORT")
DB_NAME = os.getenv("DB_MOVIES_NAME")
USERNAME = os.getenv("DB_MOVIES_USERNAME")
PASSWORD = os.getenv("DB_MOVIES_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}",
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    return SessionLocal()