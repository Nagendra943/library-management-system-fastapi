from sqlalchemy import create_engine
#connectivity to FAstApi app to Mysql database
from sqlalchemy.orm import sessionmaker, declarative_base
#sessionmaker creates db session #base class for all database models

#DATABASE_URL = "mysql+pymysql://root:nagendra%4012@localhost:3306/library_db"
DATABASE_URL = "mysql://avnadmin:AVNS_KQO1d1hzqTLMEUo3Y9V@nagendra18-nagendra316341-fastapi.g.aivencloud.com:19846/defaultdb?ssl-mode=REQUIRED"

engine = create_engine(DATABASE_URL)
#Engine is responsible for cerating a connection between fastapi and mysql db
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()

