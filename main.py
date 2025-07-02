import uvicorn
from fastapi import FastAPI
import database
import pydentic_models
from s3_storage import generate_signed_url, get_objects

app = FastAPI()


@app.get("/audio/", response_model=list[pydentic_models.PlayRead])
def get_audios(search_text: str):
    # todo add work with s3
    # for each found record get signed url
    # than create combined object for response

    audios = database.search_audios_by_name(search_text)



    for audio in audios:
        files = get_objects(audio.s3_folder_key)

        print(files)

        url = generate_signed_url(files[0]["Key"])

        print(url)
        # return files


@app.get("/test/")
def test():
    return "test response1"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)