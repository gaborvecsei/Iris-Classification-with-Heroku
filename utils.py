import base64
import cStringIO
import threading
import time

import seaborn as sns
from keras.models import model_from_json


class ModelLoader(threading.Thread):
    """
    Loads pre-trained model
    """

    def __init__(self, modelStructurePath, modelWeightsPath):
        """

        :param modelStructurePath: path to the model's json file
        :param modelWeightsPath:  path to the model's weights (.h5) file
        """

        super(ModelLoader, self).__init__()
        self.model = None
        self.modelStructurePath = modelStructurePath
        self.modelWeightsPath = modelWeightsPath

    def getModel(self):
        if self.model is None:
            return None
        else:
            return self.model

    def loadModel(self):
        """
        Loads model from the model structure and model weights file
        :return: trained model
        """

        print "Model loading started..."
        s = time.clock()
        with open(self.modelStructurePath, "r") as jsonFile:
            loadedModelStructure = jsonFile.read()
        self.model = model_from_json(loadedModelStructure)
        self.model.load_weights(self.modelWeightsPath)
        e = time.clock()
        print "Model is Loaded: {0}; in {1:.2f} seconds".format(self.model, (e - s))

    def run(self):
        super(ModelLoader, self).run()
        self.loadModel()


def plotPrediction(pred):
    """
    Plots the prediction than encodes it to base64
    :param pred: prediction accuracies
    :return: base64 encoded image as string
    """

    labels = ['setosa', 'versicolor', 'virginica']
    sns.set_context(rc={"figure.figsize": (5, 5)})
    with sns.color_palette("RdBu_r", 3):
        ax = sns.barplot(x=labels, y=pred)
    ax.set(ylim=(0, 1))

    # Base64 encode the plot
    stringIObytes = cStringIO.StringIO()
    sns.plt.savefig(stringIObytes, format='jpg')
    sns.plt.show()
    stringIObytes.seek(0)
    base64data = base64.b64encode(stringIObytes.read())
    return base64data
