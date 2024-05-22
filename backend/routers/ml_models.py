from .. import models, schemas, database, utils
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.saved_ml_models.prediction_service import try_model
import joblib

router = APIRouter(
    prefix="/ml-models",  # Ruta base para este enrutador
    tags=["ML Models"]    # Etiqueta para agrupar las operaciones relacionadas en la documentación
)

@router.get("/", response_model=List[schemas.MlModel])
def get_mlmodels(db:Session = Depends(database.get_db), current_user=Depends(utils.get_current_user)):
    mlmodels = db.query(models.MlModels).all()
    return mlmodels

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MlModel)
def create_mlmodel(ml_model:schemas.MlModel, db:Session = Depends(database.get_db),
                   current_user=Depends(utils.get_current_user)):
    filename = db.query(models.MlModels).filter(models.MlModels.filename_of_model == ml_model.filename_of_model).first()
    if filename != None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="The filename of the model is already in use.")

    if current_user.is_vip == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only vip users can create ml_models.")
    
    if not try_model(filename_of_model=f"{ml_model.filename_of_model}"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="That model has not been created yet inside the backend")

    new_ml_model = models.MlModels(**ml_model.model_dump())
    db.add(new_ml_model)
    db.commit()
    db.refresh(new_ml_model)
    return new_ml_model
