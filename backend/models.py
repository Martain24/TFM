from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, JSON
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

# Definición de la clase para la tabla 'users'
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    is_vip = Column(Boolean, nullable=False, server_default="FALSE")
    is_confirmed = Column(Boolean, nullable=False, server_default="FALSE")


# Definición de la clase para la tabla 'articles'
class MlModels(Base):
    __tablename__ = "ml_models"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    short_description = Column(String, nullable=False)
    filename_of_model = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


# Definición de la clase para la tabla 'predictions'
class Predictions(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mlmodel_id = Column(Integer, ForeignKey("ml_models.id", ondelete="CASCADE"), nullable=False)
    prediction_input = Column(JSON, nullable=False)
    prediction_output = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    # Relacionamos con Users y Articles para obtener info más completa al hacer la query
    user = relationship("Users")
    ml_model = relationship("MlModels")

# Definición de la clase para la tabla 'comments'
class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mlmodel_id = Column(Integer, ForeignKey("ml_models.id", ondelete="CASCADE"), nullable=False)

    # Relacionamos con Users y Articles para obtener infor más completa al hacer la query
    user = relationship("Users")
    ml_model = relationship("MlModels")
