from tensorflow import keras
import os
import numpy as np
import random
import name_recognizer as nr
import prepocessor as pp
import pickle


class ChatBot:
    optional_contexts = ['get_user_name']  # use for get user details
    compulsory_contexts = []

    previous_tag = ''
    target_tag = ''

    temp_response = ''
    pending_entity = ''

    model = None
    words_dictionary = None
    class_names = None
    intents = []
    entity_array = None

    name_recognizer_inst = None

    def __init__(self):
        self.model = self.__get_the_model()
        self.words_dictionary = pp.Preprocessor.get_the_words_dictionary()  # load the essentials
        self.class_names = pp.Preprocessor.get_the_class_names()
        self.intents = pp.Preprocessor.get_the_intents()
        self.entity_array = pp.Preprocessor.get_the_entities()
        self.name_recognizer_inst = nr.NameRecognizer()

    def __get_the_model(self):
        return keras.models.load_model(os.getcwd()[:-4] + "generated/" + 'saved_model/')  # load the saved model

    def __save_the_entity(self, entity_name, value):
        print(type(self.entity_array), entity_name, value)

        for entity in self.entity_array:
            print("entity type : ", type(entity))
            if entity[0] == entity_name:
                print("updating the : ", entity_name)
                entity[1] = value

        print("new entity array : ", self.entity_array)
        path = os.getcwd()[:-4] + "generated"
        with open(path + "\entities.pkl", 'wb') as f:
            pickle.dump(self.entity_array, f)

    def __find_an_entity_value(self, entity_name, pw_name):
        for entity in self.entity_array:
            if entity[0] == entity_name:
                return entity[1]

    def get_the_response(self, input_sentence):
        print("target tag : ", self.target_tag)
        print("previous tag : ", self.previous_tag)

        if self.pending_entity != '':
            print("there is a pending entity")
            if self.pending_entity == 'user_name':
                name = self.name_recognizer_inst.recognizer(input_sentence)
                print("found name : ", name.strip(), len(name.strip()))
                self.__save_the_entity(self.pending_entity, name.strip())
                self.pending_entity = ''
                # save the name

        tag_name = ''
        if self.target_tag == '':
            print("no target tag")

            # preprocessing the user reply
            processed_result = pp.Preprocessor.processing(self.words_dictionary, input_sentence)
            input_np_array = np.array([processed_result])  # convert the input to numpy array [['','','']] 1,27
            # preprocessing the user reply

            res = self.model.predict(input_np_array)  # get the prediction results (numpy array)
            max_possibility_pos = np.argmax(res)  # get the index of highest probability
            tag_name = self.class_names[max_possibility_pos]
        else:
            print("target tag is not empty")
            tag_name = self.target_tag

        print("searching tag name : ", tag_name)

        responses = []
        for intent in self.intents['intents']:
            if tag_name == intent['tag']:
                responses = intent['responses']
                self.previous_tag = tag_name
                self.target_tag = intent['context']
                self.pending_entity = intent['Entity']

                if self.target_tag in self.optional_contexts:
                    print("optional context found")
                    self.temp_response = random.choice(responses) + " "
                    return self.get_the_response('')

                break

        final_response = self.temp_response + random.choice(responses)
        self.temp_response = ''

        words_in_sentence = pp.Preprocessor.tokenize_a_sentence(final_response)

        updated_response = ''
        print(words_in_sentence)
        found_entity_name = ''
        for i, word in enumerate(words_in_sentence):
            if word == '@':
                print("find this : ", words_in_sentence[i + 1])
                print("found a variable : ", words_in_sentence[i + 1])
                entity_name = words_in_sentence[i + 1]
                entity_value = self.__find_an_entity_value(entity_name, 'not important')
                word = entity_value
                found_entity_name = entity_name
                print("entity values : ", word)
            elif word == found_entity_name:
                found_entity_name = ''
                break

            updated_response = updated_response + " " + str(word)

        print("updated sentence : ", updated_response.strip())

        return updated_response.strip()
