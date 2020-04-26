from tensorflow import keras
import os
import numpy as np
import random


class ChatBot:

    @staticmethod
    def get_the_model():
        return keras.models.load_model(os.getcwd()[:-4] + "generated/" + 'saved_model/')

    @staticmethod
    def get_the_response(class_names, responses, model, input_sentence):
        input_np_array = np.array([input_sentence])
        res = model.predict(input_np_array)
        max_posibility_pos = np.argmax(res)  # get the index of highest probability
        print("tag name : ", class_names[max_posibility_pos])
        tag_responses = responses[max_posibility_pos]  # get the responses

        return random.choice(tag_responses)  # select a random response and return
