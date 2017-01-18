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

import numpy as np
from keras.models import model_from_json

print "Loading model..."

with open("savedModel/model_structure.json", "r") as jsonFile:
    loadedModelStructure = jsonFile.read()
model = model_from_json(loadedModelStructure)
model.load_weights("savedModel/model_weights.h5")

print "Model is loaded!"

# Predict using random data
sampleData = np.array([(2.0, 3.2, 5.1, 1.2)], dtype=float)

s = time.clock()
rawPrediction = model.predict_proba(sampleData, verbose=0)[0]
predictionIndex = np.argmax(rawPrediction, axis=0)
predictionAccuracy = rawPrediction[predictionIndex]
e = time.clock()
predictionTime = e - s

print "Prediction: {0}, accuracy: {1}, in {2} sec".format(predictionIndex, predictionAccuracy, predictionTime)
