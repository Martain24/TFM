from .. import models, schemas, database, utils
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from typing import List
from backend.saved_ml_models import prediction_service

router = APIRouter(
    prefix="/predictions",  # Ruta base para este enrutador
    tags=["Predictions"]    # Etiqueta para agrupar las operaciones relacionadas en la documentación
)


@router.post("/{filename_of_model}", response_model=schemas.PredictionOutput)
def obtain_prediction(filename_of_model: str, input_data:dict, current_user=Depends(utils.get_current_user),
                      db:Session = Depends(database.get_db)):

    user_id = current_user.id
    ml_model = db.query(models.MlModels).filter(models.MlModels.filename_of_model == filename_of_model).first()
    if ml_model == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You must create an article of the model before making any predictions")
    prediction = prediction_service.run_prediction(filename_of_model=filename_of_model, input_data=input_data)
    prediction_output = {
        "user_id": user_id,
        "mlmodel_id": ml_model.id,
        "prediction_input": input_data.model_dump(),
        "prediction_output": prediction
    }
    new_prediction = models.Predictions(**prediction_output)
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction


@router.get("/", response_model=List[schemas.PredictionOutput])
def obtain_user_predictions(current_user=Depends(utils.get_current_user),
                            db:Session = Depends(database.get_db)):
    user_predictions = db.query(models.Predictions).filter(models.Predictions.user_id == current_user.id).all()
    return user_predictions
