import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
#connectivity to FAstApi app to Mysql database
from sqlalchemy.orm import sessionmaker, declarative_base
#sessionmaker creates db session #base class for all database models

#load environment variabls from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
#Engine is responsible for cerating a connection between fastapi and mysql db
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()
#provides a base class for models of sql table
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()