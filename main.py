from fastapi import FastAPI

app = FastAPI()


# @app.get("/audio/", response_model=list[schemas.AudioRead])
@app.get("/audio/")
def search_audio(title: str):
    return "test response"

