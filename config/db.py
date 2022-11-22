from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.setup import settings

engine = create_engine("postgresql://" + settings.DB_USER + ":" + settings.DB_USER_PASSWORD + "@" + settings.DB_HOST + "/" + settings.DB)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()