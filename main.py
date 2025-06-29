from fastapi import FastAPI

app = FastAPI()


# @app.get("/audio/", response_model=list[schemas.AudioRead])
@app.get("/audio/")
def get_audio(title: str):
    return "test response"


@app.get("/test/")
def test():
    return "test response1"
