# Así sería si queremos poner el authorization en los docs...


# Importando los módulos necesarios
from .. import models, schemas, database, utils
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Creando un enrutador de API
router = APIRouter(
    prefix="/login",  # Ruta base para este enrutador
    tags=["Login"]    # Etiqueta para agrupar las operaciones relacionadas en la documentación
)

@router.post("/", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Consultando el usuario en la base de datos por su email
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    # Verificando si el usuario existe
    if user == None:
        # Lanzando una excepción HTTP 403 si el usuario no existe
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid email or password")

    # Verificando si la contraseña proporcionada coincide con la contraseña almacenada
    if not utils.verify(plain_user_password=user_credentials.password, hashed_password=user.password):
        # Lanzando una excepción HTTP 403 si la contraseña es incorrecta
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid email or password")
    
    # Creando un token de acceso para el usuario autenticado
    access_token = utils.create_access_token(data_of_user_to_create_access_token={"user_id": user.id})
    # Retornando el token de acceso
    return {"access_token": access_token, "token_type": "bearer"}