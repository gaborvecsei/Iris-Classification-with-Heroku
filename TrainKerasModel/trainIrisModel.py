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

import numpy as np
import pandas as pd
from keras.layers import Dropout, Dense
from keras.models import Sequential

# Prepare data

IRIS_TRAINING = "data/iris_training.csv"
IRIS_TEST = "data/iris_test.csv"

training_set = pd.read_csv(IRIS_TRAINING, header=0)
test_set = pd.read_csv(IRIS_TEST, header=0)

data_train = training_set.values
train_data = data_train[0::, 0:4]

data_test = test_set.values
test_data = data_test[0::, 0:4]

label_data = data_train[0::, 4].astype(int)
label_test = data_test[0::, 4].astype(int)


def oneHotEncode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels, n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode


label_data = oneHotEncode(label_data)
label_test = oneHotEncode(label_test)

# Creating the model

model = Sequential()
model.add(Dense(64, input_dim=4, init='uniform', activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model

nb_epoch = 100
batch_size = 10

print "Training started..."

model.fit(train_data, label_data, batch_size=batch_size, nb_epoch=nb_epoch, validation_split=0.25, verbose=1,
          shuffle=True)

evaluateScore = model.evaluate(test_data, label_test)
print "{0}: %{1:.2f}".format(model.metrics_names[1], evaluateScore[1] * 100)

# Save trained model

print "Saving model..."
modelJson = model.to_json()
with open("savedModel/model_structure.json", "w") as json_file:
    json_file.write(modelJson)
model.save_weights("savedModel/model_weights.h5")
model.save('savedModel/model_trained.h5')
print "Model saved!"
