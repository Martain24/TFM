# Importando los módulos necesarios
from .. import models, schemas, database, utils
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

# Creando un enrutador de API
router = APIRouter(
    prefix="/users",  # Ruta base para este enrutador
    tags=["Users"]    # Etiqueta para agrupar las operaciones relacionadas en la documentación
)

# Ruta para crear un usuario
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserInput, db: Session = Depends(database.get_db)):
    email = db.query(models.Users).filter(models.Users.email == user.email).first()
    if email!=None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="This email is already registered.")

    # Hashing de la contraseña del usuario antes de guardarla en la base de datos
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Creando un nuevo usuario en la base de datos
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Retornando el nuevo usuario creado
    return new_user

# Ruta para obtener un usuario por su ID
@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id: int, db: Session = Depends(database.get_db)):
    # Consultando el usuario en la base de datos por su ID
    user_to_get = db.query(models.Users).filter(models.Users.id == id).first()

    # Verificando si el usuario existe
    if user_to_get is None:
        # Lanzando una excepción HTTP 404 si el usuario no existe
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with (id = {id}) does not exist")
    
    # Retornando el usuario obtenido
    return user_to_get

@router.post("/login", response_model=schemas.Token)
def login(user_credentials:schemas.UserInput, db: Session = Depends(database.get_db)):
    # Consultando el usuario en la base de datos por su email
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

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

