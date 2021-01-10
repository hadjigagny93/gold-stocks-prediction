from source import generate_df
from settings import DATA_DIR, MODELS_DIR
import os
import pandas as pd
import numpy as np
import joblib

class Train:
    def __init__(self, start_date=None, end_date=None, source="os", file_path=None):
        self.start_date = start_date
        self.end_date = end_date
        self.source = source
        self.file_path = file_path

    def train(self):
        df = generate_df(start_date_stock=self.start_date, end_date_stock=self.end_date, source=self.source, file_path=self.file_path)
        # naive model -> learning mean & standard deviation of target distribution
        target = df.Close.values
        mean = target.mean()
        std = target.std()
        model_params = {"mean": mean, "std":std}
        path_to_model = os.path.join(MODELS_DIR, "naive_model.pkl")
        joblib.dump(model_params, path_to_model)
        return True
"""
if __name__ == "__main__":
    start_date = "2020-07-23"
    end_date = "2020-12-14"
    file_path = os.path.join(DATA_DIR, "back.txt")
    source = "os"
    train = Train(start_date, end_date, source, file_path)
    print(train.train())
"""
