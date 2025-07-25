import uvicorn
import fastapi.params
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import database
import pydentic_models
import alchemy_models
import s3_storage


app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)


@app.get("/tracks/", response_model=pydentic_models.CursorPage)
def get_tracks(
        search_text: str | None = fastapi.params.Query(None),
        after_id: int = fastapi.params.Query(0),
        limit: int = fastapi.params.Query(20) #todo default value 20? maybe not?
):
    db_plays: list[alchemy_models.Play] = database.search_audios_by_name(search_text, after_id, limit)

    response_plays: list[pydentic_models.Play] = []

    for db_play in db_plays:
        files = s3_storage.get_objects(db_play.s3_folder_key)

        audio_urls = s3_storage.get_signed_urls(files, ".mp3")

        response_play = pydentic_models.Play(id=db_play.id, name=db_play.name, audio_urls=audio_urls)

        if s3_storage.is_folder_exists(f"{db_play.s3_folder_key}/Covers/Originals"):
            original_covers = (file for file in files if "Originals" in file["Key"])
            original_cover_urls = s3_storage.get_signed_urls(original_covers, ".webp")
            response_play.cover_urls = original_cover_urls

        response_plays.append(response_play)

    return pydentic_models.CursorPage(plays=response_plays, cursor=response_plays[-1].id if response_plays else None)


# todo works, but test possible only on real server
@app.get("/stream_url/")
def get_streaming_url(signed_url: str):
    return s3_storage.get_proxy_url(signed_url)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)