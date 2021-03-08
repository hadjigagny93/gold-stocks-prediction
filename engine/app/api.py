# By the app side, we need to integrate two main jobs
# train models manually and not (send the to db) .. 
# that previous is not a good pratice
# send models metadata to db for keeping track of 
# them during all the prediction pipelines


from pkg.predict import Predict


from flask import Flask, jsonify, make_response, request
#from ml.predict import predict_pipeline
import numpy as np 

app = Flask(__name__)

# for production env 
# app.config['DEBUG'] = False
# see in wsgi.py file 

@app.route('/score', methods=['POST'])
def score():
    features = request.json['X']
    features = np.array(features)
    score = Predict().predict(features)
    return make_response(jsonify({'score': score}))


if __name__ == '__main__':
    app.run(host='0.0.0.0')