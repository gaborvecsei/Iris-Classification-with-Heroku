"""
 *****************************************************
 *
 *              Gabor Vecsei
 * Email:       vecseigabor.x@gmail.com
 * Blog:        https://gaborvecsei.wordpress.com/
 * LinkedIn:    www.linkedin.com/in/vecsei-gabor
 * Github:      https://github.com/gaborvecsei
 *
 *****************************************************/
"""

import time

import keras
import numpy as np
from flask import Flask, jsonify

from utils import ModelLoader, plotPrediction

# Load model in a different thread
modelLoader = ModelLoader("TrainKerasModel/savedModel/model_structure.json", "TrainKerasModel/savedModel/model_weights.h5")
modelLoader.start()

# Iris class label names
LABEL_NAMES = ["setosa", "versicolor", "virginica"]

app = Flask(__name__)


@app.route('/')
def homepage():
    welcomeLabel = """
    <h1>Welcome at Iris classification by Gabor Vecsei!</h1>

    <h4>Keras ver: {0}</h4>
    """.format(keras.__version__)
    return welcomeLabel


@app.route('/isModelLoaded')
def isModelLoaded():
    loaded = False
    if modelLoader.getModel() is not None:
        loaded = True
    return jsonify(is_model_loaded=loaded)


@app.route('/predict/<data>')
def predict(data):
    # Prepare data
    data_list = data.split('-')
    if len(data_list) != 4:
        return jsonify(error="not enough data")

    inputData = np.array([(eval(data_list[0]), eval(data_list[1]), eval(data_list[2]), eval(data_list[3]))],
                         dtype=float)

    # Check if the model is ready for prediction
    if modelLoader.getModel() is None:
        return jsonify(error="model is not loaded yet")

    s = time.clock()
    # Predict probability for classes
    rawPrediction = modelLoader.getModel().predict_proba(inputData, verbose=0)[0]
    # The max prob is the best
    predictionIndex = np.argmax(rawPrediction, axis=0)
    predictionAccuracy = rawPrediction[predictionIndex]
    e = time.clock()
    predictionTime = e - s
    predictionName = LABEL_NAMES[predictionIndex]

    base64BarChartImage = plotPrediction(rawPrediction)

    print "Predicted in {0:.2f} sec".format(predictionTime)

    return jsonify(prediction_index=predictionIndex, prediction_label=predictionName, run_time=predictionTime,
                   accuracy=str(predictionAccuracy), prediction_bar_chart=base64BarChartImage)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
