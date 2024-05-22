from . import preprocessing_functions


models_map = {
    "logistic_test_model": preprocessing_functions.make_prediction_logistic_test_model,
    "name_of_model": preprocessing_functions.make_prediction_name_of_model
}

def try_model(filename_of_model):
    if filename_of_model not in models_map.keys():
        return False 
    else:
        return True
    

def get_model(filename_of_model):
    model = models_map.get(filename_of_model)
    if model is None:
        raise ValueError("Model not found")
    return model

def run_prediction(filename_of_model, input_data):
    model = get_model(filename_of_model)
    prediction = model(input_data)
    return prediction