import pickle
import os
import nltk


class preprocessing:

    @staticmethod
    def getTheWordsDictionary():
        return pickle.load(open(os.getcwd()[:-4] + "generated"+'\words.pkl', 'rb'))

    @staticmethod
    def processing(words_dict, received_sentence):
        words_in_sentence = nltk.word_tokenize(received_sentence)

        formatted_words_list = []
        for word in words_in_sentence:
            formatted_words_list.append(word.lower())

        words_in_sentence = formatted_words_list

        process_result = []
        for word in words_dict:
            if word in words_in_sentence:
                process_result.append(1)
            else:
                process_result.append(0)

        return process_result


wordsDict = preprocessing.getTheWordsDictionary()
process_result = preprocessing.processing(wordsDict, "Hello how are you?")
print(process_result)

