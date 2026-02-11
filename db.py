import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "njord")
DB_USER = os.getenv("DB_USER", "njord")
DB_PASSWORD = os.getenv("DB_PASSWORD", "njordpass")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()