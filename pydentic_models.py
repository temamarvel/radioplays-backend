from typing import List
from pydantic import BaseModel

class PlayBase(BaseModel):
    name: str

class PlayRead(PlayBase):
    id: int
    name: str
    url: str
    cover_urls: List[str] = []

    class ConfigDict:
        orm_mode = True
