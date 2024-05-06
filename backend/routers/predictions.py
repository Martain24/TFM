from .. import models, schemas, database, utils, schemas_models, ml_models
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from typing import List

router = APIRouter(
    prefix="/predictions",  # Ruta base para este enrutador
    tags=["Predictions"]    # Etiqueta para agrupar las operaciones relacionadas en la documentación
)


@router.post("/logistic_test_model", response_model=schemas.PredictionOutput)
def obtain_prediction(input:schemas_models.LogisticTest, current_user=Depends(utils.get_current_user),
                      db:Session = Depends(database.get_db)):
    model = ml_models.logistic_reg_test_model
    model_input = {key: 0 for key in model.feature_names_in_}
    model_input["Age"] = input.age
    model_input["Work_Experience"] = input.work_experience

    if input.gender.lower() == "male":
        model_input[f"Gender_Male"] = True
        model_input[f"Gender_Female"] = False
    else:
        model_input[f"Gender_Male"] = False
        model_input[f"Gender_Female"] = True

    if input.graduated.lower() == "no":
        model_input[f"Graduated_No"] = True
        model_input[f"Graduated_Yes"] = False
    else:
        model_input[f"Graduated_No"] = False
        model_input[f"Graduated_Yes"] = True

    if input.ever_married.lower() == "no":
        model_input[f"Ever_Married_No"] = True
        model_input[f"Ever_Married_Yes"] = False
    else:
        model_input[f"Ever_Married_No"] = False
        model_input[f"Ever_Married_Yes"] = True


    for key in [key for key in model_input.keys() if "Profession" in key]:
        if key.split("_")[1].lower() == input.profession.lower():
            model_input[f"Profession_{input.profession.title()}"] = True
        else:
            model_input[key] = False

    df_input = pd.DataFrame(model_input, index=[0])[model.feature_names_in_]
    prediction = model.predict(df_input)[0]

    user_id = current_user.id
    article = db.query(models.Articles).filter(models.Articles.model_filename == "logistic_test_model.sav").first()
    if article == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You must create an article of the model before the predictions")
    article_id = article.id
    prediction_output = {
        "user_id": user_id,
        "article_id": article_id,
        "prediction_input": model_input,
        "prediction_output": {"predicted_salary": str(prediction)}
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
