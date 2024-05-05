from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
import os

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:contraseña123@localhost/fastapi_db"

# Crea el engine de la base de datos para que pueda ser usada por SQLalchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Genera una clase con la sesión de la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Devuelve una clase que será usada en .models para crear las tablas
Base = declarative_base()

# Función para acceder a la base de datos.
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()