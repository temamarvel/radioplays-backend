import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, selectinload
from colored import Fore, Back, Style
import alchemy_models

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

connection_string = f"postgresql://{DB_USER}:@{DB_HOST}/{DB_NAME}"
engine = create_engine(connection_string)
# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

print("DB engine created")


def get_session():
    db_session = Session()
    try:
        yield db_session
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()


def search_plays_by_name(db_session: Session, search_text: str | None, after_id: int, limit: int):
    try:
        query = db_session.query(alchemy_models.Play)
        if search_text:
            query = query.filter(alchemy_models.Play.name.ilike(f"%{search_text}%"))
        if after_id:
            query = query.filter(alchemy_models.Play.id > after_id)
        query = query.order_by(alchemy_models.Play.id).limit(limit)
        query = query.options(selectinload(alchemy_models.Play.files))
        return query.all()
    except Exception as e:
        print(f"{Fore.red}Error! Something went wrong during query execution: {e}.{Style.reset}")
        raise

def search_play_by_id(db_session: Session, play_id: int):
    try:
        query = db_session.query(alchemy_models.Play).filter(alchemy_models.Play.id == play_id)
        return query.first()
    except Exception as e:
        print(f"{Fore.red}Error! Something went wrong during query execution: {e}.{Style.reset}")
        raise