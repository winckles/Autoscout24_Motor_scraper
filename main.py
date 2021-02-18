import pickle
import json
from flask import Flask, request
import numpy as np
import model
from os import path
import pipeline

SAVED_MODEL_PATH = "predict.pkl"
SAVED_DATA_PATH = "data.csv"


def check_data() -> str:
    if path.exists(SAVED_DATA_PATH):
        print('data exists')
    else:
        print('data does not exist, scraping data')
        pipeline.pipeline()
    return "Data check done"


def check_model() -> str:
    if path.exists(SAVED_MODEL_PATH):
        print('model exists')
    else:
        print('Model does not exist, training model')
        model.train_model()
    return "Model check done"


check_data()
check_model()
classifier = pickle.load(open(SAVED_MODEL_PATH, "rb"))
app = Flask(__name__)


def __process_input(request_data: str) -> np.array:
    """
    This processing function takes request data and transforms it to the expected format
    :param request_data: api request.data
    :return: np.array
    """
    return np.asarray([json.loads(request_data)["inputs"]])


@app.route("/")
def home_view():
    """
    This function returns the home view when starting the app
    :return: html
    """
    return "<h1>Flask app with heroku</h1>" \
           "<br>" \
           "<h2>Add '/predict to the url to make a prediction!'</h2>"


@app.route("/predict", methods=["POST"])
def predict() -> str:
    """
    This function takes POST request and returns a prediction of the house price
    :return: JSON type prediction
    """
    input_params = __process_input(request.data)
    try:
        prediction = classifier.predict(input_params)
    except (ValueError, RuntimeError, TypeError, NameError, ZeroDivisionError):
        return f'{json.dumps({"error": "PREDICTION FAILED"}), 400}'

    return json.dumps({"predicted_class": int(prediction[0])})
