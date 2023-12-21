import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World!!! Hello"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)  # type: ignore
