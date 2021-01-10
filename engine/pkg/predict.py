import joblib
import numpy as np
import os
from settings import MODELS_DIR

class Predict:
    def __init__(self):
        pass
        
    def predict(self, X):
        # load model -> naive model
        path_to_model = os.path.join(MODELS_DIR, "naive_model.pkl")
        model = joblib.load(path_to_model)
        mean = model.get('mean')
        std = model.get('std')
        return np.random.normal(mean, std, 1)[0]
