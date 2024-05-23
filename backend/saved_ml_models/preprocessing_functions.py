import joblib
import os
import pandas as pd
from pydantic import BaseModel


####################
########## logistic_test_model ##########
####################

class LogisticTestModel(BaseModel):
    age: int
    work_experience: float 
    gender: str 
    ever_married: str 
    graduated: str 
    profession: str 
    class Config:
        from_attributes = True

def make_prediction_logistic_test_model(input_data:dict):
    predictions = {}
    for index in input_data.keys():
        data = LogisticTestModel(**input_data[index])
        model = joblib.load(os.path.join(os.path.dirname(__file__), "models_files", "logistic_test_model.sav"))
        model_input = {key: 0 for key in model.feature_names_in_}
        model_input["Age"] = data.age
        model_input["Work_Experience"] = data.work_experience

        if data.gender.lower() == "male":
            model_input[f"Gender_Male"] = True
            model_input[f"Gender_Female"] = False
        else:
            model_input[f"Gender_Male"] = False
            model_input[f"Gender_Female"] = True

        if data.graduated.lower() == "no":
            model_input[f"Graduated_No"] = True
            model_input[f"Graduated_Yes"] = False
        else:
            model_input[f"Graduated_No"] = False
            model_input[f"Graduated_Yes"] = True

        if data.ever_married.lower() == "no":
            model_input[f"Ever_Married_No"] = True
            model_input[f"Ever_Married_Yes"] = False
        else:
            model_input[f"Ever_Married_No"] = False
            model_input[f"Ever_Married_Yes"] = True


        for key in [key for key in model_input.keys() if "Profession" in key]:
            if key.split("_")[1].lower() == data.profession.lower():
                model_input[f"Profession_{data.profession.title()}"] = True
            else:
                model_input[key] = False

        df_input = pd.DataFrame(model_input, index=[0])[model.feature_names_in_]
        prediction = model.predict(df_input)[0]
        predictions[index] = {f"predicted_salary": str(prediction)}
    return predictions




####################
########## name_of_model ##########
####################

class NameOfModel(BaseModel):
    pass 

def make_prediction_name_of_model(input_data:NameOfModel):
    pass