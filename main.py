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
        after_id: int = fastapi.params.Query(0, ge=0),
        limit: int = fastapi.params.Query(20, ge=1, le=50), #todo default value 20? maybe not?
        db_session: database.Session = fastapi.Depends(database.get_session)
):
    db_plays: list[alchemy_models.Play] = database.search_plays_by_name(db_session, search_text, after_id, limit)

    response_plays: list[pydentic_models.Play] = []

    # todo uncomment for prod
    for db_play in db_plays:
        response_play = fill_play_properties(db_play)

        response_plays.append(response_play)

    return pydentic_models.CursorPage(plays=response_plays, cursor=response_plays[-1].id if response_plays else None)

# move to separate file
# can do it with router refactoring
def fill_play_properties(db_play: alchemy_models.Play)-> pydentic_models.Play:
    response_play = pydentic_models.Play(id=db_play.id, name=db_play.title)
    # response_play.audio_urls = s3_storage.get_signed_urls(db_play.files, s3_storage.FileKind.AUDIO)
    # response_play.cover_urls = s3_storage.get_signed_urls(db_play.files, s3_storage.FileKind.ORIGINAL)
    # response_play.thumbnail_urls = s3_storage.get_signed_urls(db_play.files, s3_storage.FileKind.THUMBNAIL)

    return response_play

@app.get("/tracks/{track_id}", response_model=pydentic_models.Play)
def get_track_by_id(track_id: int = fastapi.Path(..., ge=0), db_session: database.Session = fastapi.Depends(database.get_session)):
    db_play: alchemy_models.Play = database.search_play_by_id(db_session, track_id)

    if not db_play:
        raise fastapi.HTTPException(status_code=404, detail="Track not found")

    return fill_play_properties(db_play)

# todo works, but test possible only on real server
@app.get("/stream_url/")
def get_streaming_url(signed_url: str):
    return s3_storage.get_proxy_url(signed_url)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)