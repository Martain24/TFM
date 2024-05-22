# Importando módulos necesarios
from passlib.context import CryptContext 
from jose import JWTError, jwt 
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import dotenv_values 
import smtplib
from email.mime.text import MIMEText
import joblib
import os

settings = dotenv_values(".env")

# Contexto de cifrado para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para generar el hash de una contraseña
def hash(user_password: str) -> str:
    return pwd_context.hash(user_password)

# Función para verificar una contraseña
def verify(plain_user_password: str, hashed_password: str):
    return pwd_context.verify(plain_user_password, hashed_password)

# Esquema de autenticación OAuth2 para obtener tokens de acceso
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Clave secreta para firmar tokens de acceso
SECRET_KEY = settings["SECRET_KEY"]

# Algoritmo de cifrado utilizado para firmar tokens de acceso
ALGORITHM = settings["ALGORITHM"]

# Duración de los tokens de acceso (en minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings["ACCESS_TOKEN_EXPIRE_MINUTES"])

# Función para crear un token de acceso
def create_access_token(data_of_user_to_create_access_token: dict):
    to_encode = data_of_user_to_create_access_token.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar un token de acceso
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id == None:
            raise credentials_exception 
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        print("hey")
        raise credentials_exception
    return token_data

# Función para obtener el usuario actual a partir del token de acceso
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="No se pudieron validar las credenciales",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.user_id).first()
    return user


def send_registration_email(access_token, recipients):
    body_of_email = f"""¡Hola y bienvenido!

Esto es un correo de bienvenida y de confirmación. Esperamos que nuestra API junto con nuestra web te sean de mucha utilidad.

Aquí tienes tu token de confirmación:

Token -> {access_token}

Token Type -> bearer

Para usarlo en nuestro frontend simplemente pega el Token.

Si quieres usarlo desde python tendrás que crear el siguiente diccionario:

headers = {{"Authentification": "bearer {access_token}}}

y pásalo como u headers en tus requests.
"""
    msg = MIMEText(body_of_email)
    msg['Subject'] = "Token de acceso y bienvenida"
    msg['From'] = "miluma082@gmail.com"
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login("miluma082@gmail.com", settings["EMAIL_PASSWORD"])
       smtp_server.sendmail("miluma082@gmail.com", recipients, msg.as_string())

