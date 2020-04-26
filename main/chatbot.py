from tensorflow import keras
import os
import numpy as np
import random
import name_recognizer as nr
import prepocessor as pp
import pickle


class ChatBot:
    optional_contexts = ['get_user_name']
    compulsory_contexts = []

    previous_context = ''
    temp_response = ''
    pending_entity = ''

    model = None
    class_names = None
    intents = []
    entity_array = None

    def __init__(self):
        self.model = self.__get_the_model()
        self.class_names = pp.Preprocessor.get_the_class_names()
        self.intents = pp.Preprocessor.get_the_intents()
        self.entity_array = pp.Preprocessor.get_the_entities()

    def __get_the_model(self):
        return keras.models.load_model(os.getcwd()[:-4] + "generated/" + 'saved_model/')  # load the saved model

    def __save_the_entity(self, entity_name, value):
        print(type(self.entity_array))

        for entity in self.entity_array:
            print(entity)
            if entity[0] == entity_name:
                print("updating the : ", entity_name)
                entity[1] = value

        print("new entity array : ",self.entity_array)
        path = os.getcwd()[:-4] + "generated"
        with open(path + "\entities.pkl", 'wb') as f:
            pickle.dump(self.entity_array, f)

    def __find_an_entity_value(self, entity_name, pw_name):
        for entity in self.entity_array:
            if entity[0] == entity_name:
                return entity[1]

    @classmethod
    def get_the_response(cls, input_sentence):
        print("class var : ", cls.previous_context)
        input_np_array = np.array([input_sentence])  # convert the input to numpy array [['','','']] 1,27

        if cls.pending_entity != '':
            print("there is a pending entity")
            if cls.pending_entity == 'name':
                name = nr.NameRecognizer.recognizer(input_sentence)
                print("found name : ", name)
                cls.__save_the_entity(cls.pending_entity, name)
                # save the name

        tag_name = ''
        if cls.previous_context == '':
            print("previous context is empty")
            res = cls.model.predict(input_np_array)  # get the prediction results (numpy array)
            max_possibility_pos = np.argmax(res)  # get the index of highest probability
            tag_name = cls.class_names[max_possibility_pos]
        else:
            print("previous context is not empty")
            tag_name = cls.previous_context

        print("searching tag name : ", tag_name)

        responses = []
        for intent in cls.intents['intents']:
            if tag_name == intent['tag']:
                responses = intent['responses']
                cls.previous_context = intent['context']
                cls.pending_entity = intent['Entity']

                if cls.previous_context in cls.optional_contexts:
                    print("optional context found")
                    cls.temp_response = random.choice(responses)+" "
                    return cls.get_the_response('')

                break

        print("temporary saved response : ", cls.temp_response, random.choice(responses))
        final_response = cls.temp_response + str(random.choice(responses))
        cls.temp_response = ''

        words_in_sentence = pp.Preprocessor.tokenize_a_sentence(final_response)

        updated_response = ''
        for word in words_in_sentence:
            if word[0] == '@':
                print("found a variable : ", word[1:])
                entity_value = cls.__find_an_entity_value(word[1:], 'not important')
                word = entity_value
            updated_response = updated_response +" "+word

        print("updated sentence : ", updated_response)

        return updated_response
