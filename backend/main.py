import os
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import ml_models, users, comments, auth, predictions

import joblib

# Ruta al archivo .sav
modelo_ml_path = os.path.join(os.path.dirname(__file__), 'logistic_test_model.sav')

# Esto es lo que crea las databases que tengamos en models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(comments.router)
app.include_router(ml_models.router)
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(auth.router)


@app.get("/")
def root():
    # Intenta cargar el modelo de machine learning
    try:
        modelo_ml = joblib.load(modelo_ml_path)
        # Hacer algo con el modelo si se cargó correctamente
        return {"message": "Hello world", "modelo_ml": str(modelo_ml)}
    except FileNotFoundError:
        return {"error": "Modelo de machine learning no encontrado"}
