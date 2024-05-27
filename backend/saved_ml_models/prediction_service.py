from . import preprocessing_functions


models_map = {
    "logistic_test_model": preprocessing_functions.make_prediction_logistic_test_model,
    "best_model_fish": preprocessing_functions.make_prediction_best_model_quantity,
    "best_model_fruits": preprocessing_functions.make_prediction_best_model_quantity,
    "best_model_meat": preprocessing_functions.make_prediction_best_model_quantity,
    "best_model_sweet": preprocessing_functions.make_prediction_best_model_quantity,
    "best_model_wines": preprocessing_functions.make_prediction_best_model_quantity
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
    prediction = model(input_data, filename_of_model=filename_of_model)
    return prediction