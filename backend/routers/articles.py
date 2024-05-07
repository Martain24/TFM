from .. import models, schemas, database, utils, ml_models
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import joblib

router = APIRouter(
    prefix="/articles",  # Ruta base para este enrutador
    tags=["Articles"]    # Etiqueta para agrupar las operaciones relacionadas en la documentación
)

@router.get("/", response_model=List[schemas.Article])
def get_articles(db:Session = Depends(database.get_db), current_user=Depends(utils.get_current_user)):
    articles = db.query(models.Articles).all()
    return articles

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Article)
def create_article(article:schemas.Article, db:Session = Depends(database.get_db),
                   current_user=Depends(utils.get_current_user)):
    filename = db.query(models.Articles).filter(models.Articles.filename_of_model == article.filename_of_model).first()
    if filename != None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="The filename of the model is already in use.")

    if current_user.is_vip == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only vip users can create articles.")
    if not ml_models.try_model(f"{article.filename_of_model}"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The filename provided does not exists or does not contain any model")

    new_article = models.Articles(**article.model_dump())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article
