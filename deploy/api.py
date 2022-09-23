"""
api.py
~~~~~~

This module defines a simple REST API for a Machine Learning (ML) model.
"""

from os import environ

from joblib import load
from flask import abort, Flask, jsonify, make_response, request, render_template
from pandas import DataFrame
import numpy as np

service_name = environ['SERVICE_NAME']
version = environ['API_VERSION']
model = load('model.joblib')
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    #int_features = [float(x) for x in request.form.values()]
    #print(int_features)
    #features = [np.array(int_features)]
    #print(features)

    features = {
        'Pclass': float(request.form['Pclass']),
        'Age': float(request.form['Age']),
        'Sex': str(request.form['Sex']),
        'SibSp': float(request.form['SibSp']),
        'Parch': float(request.form['Parch']),
        'Fare': float(request.form['Fare']),
        'Embarked': str(request.form['Embarked']),

    }

    print(features)

    prediction = model.predict(DataFrame([features]))
    output = prediction
                                        
    if output == 1:
        return render_template('index.html', prediction_text='You survived!')
    else:
        return render_template('index.html', prediction_text='You DIE! :(')


@app.route(f'/{service_name}/v{version}/predict_api', methods=['POST'])
def predict_api():
    """TODO"""
    try:
        features = DataFrame(request.json)
        print(features)
        prediction = model.predict(features).tolist()
        return make_response(jsonify({'prediction': prediction}))
    except ValueError:
        raise RuntimeError('Features are not in the correct format.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
