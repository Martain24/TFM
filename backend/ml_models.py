import joblib
import os


logistic_reg_test_model = joblib.load(os.path.join(os.path.dirname(__file__), 'logistic_test_model.sav'))

def try_model(filename):
    try:
        joblib.load(os.path.join(os.path.dirname(__file__), filename))
        return True
    except:
        return False
