from pydantic import BaseModel

class PlayBase(BaseModel):
    name: str

class PlayRead(PlayBase):
    id: int
    s3_folder_key: str

    class Config:
        orm_mode = True
