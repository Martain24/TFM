import joblib
import os
import pandas as pd
from pydantic import BaseModel
from fastapi import HTTPException, status


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
        input_data[index] = data.model_dump()
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
    return input_data, predictions




####################
########## best_model_fish ##########
####################

class BestModelFish(BaseModel):
    age: int 
    education: str
    marital_status: str 
    income: int 
    kidhome: int 
    teenhome: int 
    year_customer_entered: str 
    recency: int 
    complain: int

def make_prediction_best_model_fish(input_data:dict):
    predictions = {}
    model = joblib.load(os.path.join(os.path.dirname(__file__), "models_files", "best_model_fish.sav"))
    for index in input_data.keys():
        row = pd.Series(input_data[index])
        row.index = [i.lower() for i in row.index]
        row = dict(row)
        try:
            row = BestModelFish(**row)
            input_data[index] = row.model_dump()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Incorrect format of dict")
        model_input = {key: 0 for key in model.feature_names_in_}
        model_input["Age"] = row.age
        model_input["Income"] = row.income
        model_input["Kidhome"] = row.kidhome 
        model_input["Teenhome"] = row.teenhome
        model_input["Recency"] = row.recency 
        model_input["Complain"] = row.complain
        for key in [key for key in model_input.keys() if "Education" in key]:
            possible_value = key.split("_")[1]
            if possible_value.lower() == row.education.lower():
                model_input[key] = True
                input_data[index]["education"] = possible_value
            else:
                model_input[key] = False
        for key in [key for key in model_input.keys() if "Marital_Status" in key]:
            if key.split("_")[2].lower() == row.marital_status.lower():
                model_input[key] = True
                input_data[index]["marital_status"] = key.split('_')[2]
            else:
                model_input[key] = False
        for key in [key for key in model_input.keys() if "Year_Customer_Entered" in key]:
            if key.split("_")[3].lower() == row.year_customer_entered.lower():
                model_input[key] = True
                input_data[index]["year_customer_entered"] = key.split('_')[3]
            else:
                model_input[key] = False
        df_input = pd.DataFrame(model_input, index=[0])[model.feature_names_in_]
        prediction = model.predict(df_input)[0]
        predictions[index] = {f"predicted_MntFishProducts": str(prediction)}
    return input_data, predictions
    
