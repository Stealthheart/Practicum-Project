from keras.models import load_model
from tensorflow import convert_to_tensor
import numpy as np

model = None

def initializeModelType(inLang):
    global model
    if inLang == 0:
        model = load_model('hiraganaAI.h5')
    elif inLang == 1:
        model = load_model('katakanaAI.h5')
    else:
        model = load_model('kanjiAI.h5')

def predictAnswer(inImg):
    return np.argmax(model.predict(convert_to_tensor(inImg)), axis=-1)