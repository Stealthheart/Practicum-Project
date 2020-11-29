from keras.preprocessing import image
import numpy as np
import aiLogic as ai

def initializeAIModel(inLang):
    ai.initializeModelType(inLang)

def predictAnswer():
    testImg = image.load_img("image.png", color_mode='grayscale')
    testImg = image.img_to_array(testImg)
    testImg = np.expand_dims(testImg, axis=0)
    return ai.predictAnswer(testImg)[0]