from config.db import Session
from config.db import engine

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()