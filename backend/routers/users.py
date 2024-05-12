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
    if user.is_confirmed:   
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        subject_of_email = "Token de acceso"
        body_of_email = f"""Aquí tienes tu token de acceso:

Token -> {access_token}

Token Type -> bearer

Para usarlo en nuestro frontend simplemente pega el Token.

Si quieres usarlo desde python tendrás que crear el siguiente diccionario:

headers = {{"Authentification": "bearer {access_token}}}

y pasarlo como un headers en tus requests
        """
        sender = "miluma082@gmail.com"
        recipients = [user.email]
        password = "aard nizv nivr roro"
        utils.send_email(subject_of_email, body_of_email, sender, recipients, password)
        return {"detail": "¡We have sent you an email with your token!"}

@router.delete("/{id}", response_model=schemas.UserOutput)
def delete_user(id: int, db: Session = Depends(database.get_db), current_user=Depends(utils.get_current_user)):
    if current_user.is_vip:
        # Los vip puedan eliminar a cualquier usuario
        user_to_delete = db.query(models.Users).filter(models.Users.id == id).first()
        if user_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID {id} does not exist.")
        
        db.delete(user_to_delete)
        db.commit()
        return user_to_delete

    # Los NO VIP solo pueden eliminarse así mismos
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only VIP users can deleate other users.")
    
    db.delete(current_user)
    db.commit()
    return current_user

@router.put("/", response_model=schemas.UserOutput)
def verify_user(db: Session = Depends(database.get_db), current_user=Depends(utils.get_current_user)):
    user_to_verify = db.query(models.Users).filter(models.Users.id == current_user.id).first()
    if user_to_verify:
        user_to_verify.is_confirmed = True
        db.commit()
        db.refresh(user_to_verify)
        return user_to_verify
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")