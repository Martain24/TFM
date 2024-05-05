from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, comments, articles, auth, predictions


# Esto es lo que crea las databases que tengamos en models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(comments.router)
app.include_router(articles.router)
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello world"}