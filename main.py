import uvicorn
from fastapi import FastAPI

from database import get_record_from_database

app = FastAPI()


# @app.get("/audio/", response_model=list[schemas.AudioRead])
@app.get("/audio/")
def get_audio(search_text: str):
    records = get_record_from_database(search_text)

    for record in records:
        print(record)

    return get_record_from_database(search_text)


@app.get("/test/")
def test():
    return "test response1"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)