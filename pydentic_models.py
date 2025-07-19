from pydantic import BaseModel, conlist
import fastapi


class PlayBase(BaseModel):
    name: str

class PlayRead(PlayBase):
    id: int
    name: str
    audio_urls: conlist(str, min_length=1)
    cover_urls: list[str] = []
    streaming_urls: list[fastapi.responses.StreamingResponse]

    class ConfigDict:
        orm_mode = True
