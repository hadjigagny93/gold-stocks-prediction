
import datetime
from .models import *
import requests


class Forecast:

    def __init__(self, base_url):
        self.current_date = datetime.date.today()
        self.base_url = base_url


    def get_predictions(self):
        # get daily aggregated data news_header
        str_date = datetime.datetime.strftime(self.current_date, '%Y-%m-%d')
        features = Stock.objects.filter(date=str_date).values('news')[::1][0]['news']
        # post requests to retrieve predictions and models metadata
        #ml_endpoint_url = "http://0.0.0.0:5000/score"
        #features = self.get_features()
        #if not isinstance(features, str):
        #    raise ValueError('Bad data format')
        predictions = requests.post(
            self.base_url, 
            json={
                "X":features
                }
            ).json().get('score')
        print(predictions)



    def push_data_on_db(self):
        pass

