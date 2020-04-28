from tensorflow import keras
import os
import numpy as np
import random
import name_recognizer as nr
import prepocessor as pp
import pickle


class ChatBot:
    previous_tag = ''
    target_tag = ''

    temp_response = ''

    model = None
    words_dictionary = None
    class_names = None
    intents = []
    entity_array = None

    optional_contexts = []
    compulsory_contexts = []

    name_recognizer_inst = None

    current_context_group = ''
    current_context_group_type = ''

    pending_entity = ''
    pending_entity_title = ''

    temp_compulsory_entity_values = []

    def __init__(self):
        self.model = self.__get_the_model()
        self.words_dictionary = pp.Preprocessor.get_the_words_dictionary()  # load the essentials
        self.class_names = pp.Preprocessor.get_the_class_names()
        self.intents = pp.Preprocessor.get_the_intents()
        self.entity_array = pp.Preprocessor.get_the_entities()
        self.name_recognizer_inst = nr.NameRecognizer()
        self.__create_the_contexts()

    def __create_the_contexts(self):
        contexts_array = pp.Preprocessor.get_the_contexts()

        for item in contexts_array:
            print(item)
            if item[0] == 'optional':
                self.optional_contexts = item[1]
            elif item[0] == 'compulsory':
                self.compulsory_contexts = item[1]

        print('optional context : ', self.optional_contexts)
        print('compulsory context : ', self.compulsory_contexts)

    def __get_the_model(self):
        return keras.models.load_model(os.getcwd()[:-4] + "generated/" + 'saved_model/')  # load the saved model

    def __save_compulsory_entities(self, entity_title, values_list):
        for entity in self.entity_array:
            if entity[0] == entity_title:
                print("found entity title : ", entity_title)
                entity[1].append(np.array(values_list, dtype='object'))
                break

        print('new entity array ', self.entity_array)

        path = os.getcwd()[:-4] + "generated"
        with open(path + "\entities.pkl", 'wb') as f:
            pickle.dump(self.entity_array, f)

    def __save_optional_entities(self, entity_title, entity_name, value):
        for entity in self.entity_array:
            if entity[0] == entity_title:
                print("found entity title : ", entity_title)
                entity[1].append(np.array([entity_name, value], dtype='object'))
                break

        print('new entity array ', self.entity_array)
        path = os.getcwd()[:-4] + "generated"
        with open(path + "\entities.pkl", 'wb') as f:
            pickle.dump(self.entity_array, f)

        self.optional_contexts.remove(self.current_context_group)
        pp.Preprocessor.update_optional_contexts(self.optional_contexts, self.compulsory_contexts)

    def __find_an_entity_value(self, entity_name, pw_name):
        print("entities : ", self.entity_array)
        for entity in self.entity_array:
            print("entity : ", entity)
            for entry in entity[1]:
                print("entry : ", entry)
                if entry[0] == entity_name:
                    print("entity found")
                    return entry[1]

        return ''

    def get_the_response(self, input_sentence):
        print("target tag : ", self.target_tag)

        if self.pending_entity != '':
            print("there is a pending entity")
            if self.current_context_group_type == 'compulsory':
                self.temp_compulsory_entity_values.append(input_sentence.replace('\n', ''))

                if len(self.temp_compulsory_entity_values) == 2:
                    self.__save_compulsory_entities(self.pending_entity_title, self.temp_compulsory_entity_values)
                    self.temp_compulsory_entity_values = []

            elif self.current_context_group_type == 'optional':
                value = self.name_recognizer_inst.recognizer(input_sentence)
                self.__save_optional_entities(self.pending_entity_title, self.pending_entity, value)

        tag_name = ''
        if self.current_context_group == '':
            print("no current context group")

            # preprocessing the user reply
            processed_result = pp.Preprocessor.processing(self.words_dictionary, input_sentence)
            input_np_array = np.array([processed_result])  # convert the input to numpy array [['','','']] 1,27
            # preprocessing the user reply

            res = self.model.predict(input_np_array)  # get the prediction results (numpy array)
            max_possibility_pos = np.argmax(res)  # get the index of highest probability
            tag_name = self.class_names[max_possibility_pos]
        else:
            print("following a context group")
            tag_name = self.target_tag

        print("searching context name : ", tag_name)

        responses = []
        for intent in self.intents['intents']:
            if tag_name == intent['tag']:
                responses = intent['responses']
                self.target_tag = intent['context']

                self.pending_entity = intent['entity']
                self.pending_entity_title = intent['entity_title']

                context_group = intent['context_group']

                if self.current_context_group == '':
                    print('current context group is null')
                    print("op : ", self.optional_contexts, " comp : ",self.compulsory_contexts)
                    if context_group in self.optional_contexts or context_group in self.compulsory_contexts:
                        print("new context group is in optional or compulsory contexts arrays")
                        self.temp_response = random.choice(responses) + " "
                        self.current_context_group = context_group
                        self.current_context_group_type = intent['context_group_type']
                        return self.get_the_response('')
                else:
                    print('current context group is not null')
                    if self.target_tag == '':
                        print('target context is null')
                        self.current_context_group = ''
                        self.current_context_group_type = ''
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
                continue

            updated_response = updated_response + " " + word

        print("updated sentence : ", updated_response.strip())

        return updated_response.strip()
