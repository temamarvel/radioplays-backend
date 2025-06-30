from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    s3_folder_key = Column(String, nullable=False)