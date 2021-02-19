import pickle
import json
from flask import Flask, request
import numpy as np
from os import path
from data import pipeline, model
import heroku.database as db

SAVED_MODEL_PATH = "data/predict.pkl"
SAVED_DATA_PATH = "data/data.csv"


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
db.create_table()
print('connected and table created')

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
    return "<h1>Motor price predictor</h1>" \
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

    # except (ValueError, RuntimeError, TypeError, NameError, ZeroDivisionError):
    #     return f'{json.dumps({"error": "PREDICTION FAILED"}), 400}'
    except:
        return json.dumps({"error": "PREDICTION FAILED"}), 400

    db.insert_into_table(
        json.dumps({"input": input_params}),
        json.dumps({"Predicted price": prediction[0]})
    )

    return json.dumps({"predicted_class": int(prediction[0])})


@app.route("/retrieve", methods=["GET"])
def retrieve() -> str:
    """
    Selects last 10 records from the request-response database
    :return: last 10 requests and responses.
    """
    return json.dumps({"retrieved records": db.select_from_table()})
