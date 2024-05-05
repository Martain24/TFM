from pydantic import BaseModel, EmailStr
from datetime import datetime

# Definición de la clase Pydantic para la entrada de usuario
class UserInput(BaseModel):
    email: EmailStr   # Correo electrónico del usuario
    password: str     # Contraseña del usuario

# Definición de la clase Pydantic para la salida de usuario
class UserOutput(BaseModel):
    id: int               # Identificador único del usuario
    email: EmailStr       # Correo electrónico del usuario
    created_at: datetime  # Fecha y hora de creación del usuario
    is_vip: bool

    class Config:
        from_attributes = True

# Definición de la clase Pydantic para los artículos
class Article(BaseModel):
    title: str              # Título del artículo
    short_description: str  # Breve descripción del artículo
    model_filename: str

# Definición de la clase Pydantic para la entrada de predicciones
class PredictionInput(BaseModel):
    model_filename: str       # Identificador único del artículo
    prediction_input: dict

# Definición de la clase Pydantic para la salida de predicciones
class PredictionOutput(BaseModel):
    user: UserOutput      # Información del usuario asociado a la predicción
    article: Article      # Información del artículo asociado a la predicción
    prediction_input: str
    prediction_output: str

    class Config:
        from_attributes = True

# Definición de la clase Pydantic para la entrada de comentarios
class CommentInput(BaseModel):
    content: str          # Contenido del comentario
    article_id: int
    

# Definición de la clase Pydantic para la salida de comentarios
class CommentOutput(BaseModel):
    user: UserOutput      # Información del usuario que realizó el comentario
    content: str          # Contenido del comentario
    article: Article      # Información del artículo al que pertenece el comentario
    created_at: datetime  # Fecha y hora de creación del comentario

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    user_id: int







    