import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from colored import Fore, Back, Style

from alchemy_models import Play

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

def search_audios_by_name(search_text: str):
    with Session() as db_session:
        try:
            return db_session.query(Play).filter(Play.name.ilike(f"%{search_text}%")).all()
        except Exception as e:
            print(f"{Fore.red}Error! Something went wrong during query execution: {e}.{Style.reset}")
            raise
