import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise RuntimeError("Set the DATABASE_URL environment variable before starting the API.")

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
