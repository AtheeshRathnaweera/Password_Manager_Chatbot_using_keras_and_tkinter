import json
import pickle
import os
import nltk
import numpy as np
from nltk.stem.lancaster import LancasterStemmer


class Preprocessor:

    @staticmethod
    def get_the_words_dictionary():
        return pickle.load(open(os.getcwd()[:-4] + "generated"+'\words.pkl', 'rb'))

    @staticmethod
    def get_the_class_names():
        return pickle.load(open(os.getcwd()[:-4] + "generated" + '\classnames.pkl', 'rb'))

    @staticmethod
    def get_the_entities():
        return pickle.load(open(os.getcwd()[:-4] + "generated" + '\entities.pkl', 'rb'))

    @staticmethod
    def get_the_intents():
        intent_file = open(os.getcwd()[:-4]+"/resources/intents.json").read()
        return json.loads(intent_file)

    @staticmethod
    def tokenize_a_sentence(sentence):
        return nltk.word_tokenize(sentence)

    @staticmethod
    def processing(words_dict, received_sentence):
        stemmer = LancasterStemmer()
        words_in_sentence = nltk.word_tokenize(received_sentence)

        formatted_words_list = []
        for word in words_in_sentence:
            formatted_words_list.append(stemmer.stem(word.lower()))

        words_in_sentence = formatted_words_list

        process_result = []
        for word in words_dict:
            if word in words_in_sentence:
                process_result.append(1)
            else:
                process_result.append(0)

        return process_result

