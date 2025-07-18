from typing import List
from pydantic import BaseModel, conlist


class PlayBase(BaseModel):
    name: str

class PlayRead(PlayBase):
    id: int
    name: str
    audio_urls: conlist(str, min_length=1)
    cover_urls: list[str] = []

    class ConfigDict:
        orm_mode = True
