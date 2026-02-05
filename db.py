import os
print("DATABASE_URL seen by container:", os.getenv("DATABASE_URL"))

from sqlalchemy import create_engine, Column, Float, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from datetime import datetime

DATABASE_URL = os.getenv("interchange.proxy.rlwy.net:55500")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class BoatData(Base):
    __tablename__ = "boat_data"

    id = Column(String, primary_key=True)
    time = Column(DateTime, default=datetime.utcnow)
    lat = Column(Float)
    lng = Column(Float)
    sog = Column(Float)
    cog = Column(Float)
    pgns = Column(JSON)

Base.metadata.create_all(engine)