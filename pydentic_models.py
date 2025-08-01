from pydantic import BaseModel, conlist


class PlayBase(BaseModel):
    name: str

class Play(PlayBase):
    id: int
    name: str
    # audio_urls: conlist(str, min_length=1)
    audio_urls: list[str] = [] #todo ONLY for testing. In prod MUST be 1
    cover_urls: list[str] = []
    thumbnail_urls: list[str] = []

    class ConfigDict:
        orm_mode = True

class CursorPage(BaseModel):
    plays: list[Play]
    cursor: int | None