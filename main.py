import uvicorn
from fastapi import FastAPI
import database
import pydentic_models


app = FastAPI()


@app.get("/audio/", response_model=list[pydentic_models.PlayRead])
def get_audios(search_text: str):
    # todo add work with s3
    # for each found record get signed url
    # than create combined object for response
    return database.search_audios_by_name(search_text)


@app.get("/test/")
def test():
    return "test response1"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)