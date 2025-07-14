from pydantic import BaseModel

class PlayBase(BaseModel):
    name: str

class PlayRead(PlayBase):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True
