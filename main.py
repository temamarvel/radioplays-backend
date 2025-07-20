import os.path

import uvicorn
from fastapi import FastAPI

import database
import pydentic_models
import alchemy_models
import s3_storage

app = FastAPI()


@app.get("/audio/", response_model=list[pydentic_models.PlayRead])
def get_audios(search_text: str):
    audios: list[alchemy_models.Play] = database.search_audios_by_name(search_text)

    response = []

    for audio in audios:
        files = s3_storage.get_objects(audio.s3_folder_key)

        audio_urls = s3_storage.get_signed_urls(files, ".mp3")

        response_object = pydentic_models.PlayRead(id=audio.id, name=audio.name, audio_urls=audio_urls)

        if s3_storage.is_folder_exists(f"{audio.s3_folder_key}/Covers/Originals"):
            original_covers = (f for f in files if "Originals" in f["Key"])
            original_cover_urls = s3_storage.get_signed_urls(original_covers, ".webp")
            response_object.cover_urls = original_cover_urls

        response.append(response_object)

    return response

# todo works, but test possible only on real server
@app.get("/stream_url/")
def get_streaming_url(signed_url: str):
    return s3_storage.get_proxy_url(signed_url)


@app.get("/test/")
def test():
    return "test response1"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)