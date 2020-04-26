import json
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
import pickle

import numpy as np
from tensorflow import keras

import os


class create_model:
    words_library = []
    tags = []
    ignore_words = ["?", "!", ","]

    doc_x = []
    doc_y = []

    def __init__(self):
        self.__readTheIntents()
        self.__preProcessTestAndTrainData()

        self.modelCreation()

    def __readTheIntents(self):
        intent_file = open("../resources/intents.json").read()
        intents_json = json.loads(intent_file)

        for intent in intents_json['intents']:
            tag_name = intent['tag']
            self.tags.append(tag_name)

            for pattern in intent['patterns']:
                words_in_pattern = nltk.word_tokenize(pattern)
                self.words_library.extend(words_in_pattern)

                self.doc_x.append(words_in_pattern)
                self.doc_y.append(tag_name)

        stemmed_words_library = []
        for word in self.words_library:
            if word not in self.ignore_words:
                stemmed_words_library.append(stemmer.stem(word.lower()))

        self.words_library = stemmed_words_library

        print(len(self.words_library))
        self.words_library = sorted(list(set(self.words_library)))
        self.tags = sorted(self.tags)
        print("stemmed words library amount : ", len(self.words_library))

        path = os.getcwd()[:-4] + "generated"

        with open(path + "\words.pkl", 'wb') as f:
            pickle.dump(self.words_library, f)

        with open(path + "\classnames.pkl", 'wb') as f:
            pickle.dump(self.tags, f)

    def __preProcessTestAndTrainData(self):
        processed_x = []
        for pattern in self.doc_x:

            stemmed_pattern = []
            for word in pattern:
                stemmed_pattern.append(stemmer.stem(word.lower()))

            process_result = []
            for word in self.words_library:
                if word in stemmed_pattern:
                    process_result.append(1)
                else:
                    process_result.append(0)

            processed_x.append(process_result)

        self.doc_x = processed_x

        processed_y = []
        for item in self.doc_y:
            result = []
            for tag in self.tags:
                if tag == item:
                    result.append(1)
                else:
                    result.append(0)

            processed_y.append(result)

        self.doc_y = processed_y

    def modelCreation(self):
        training_x = np.array(self.doc_x)
        training_y = np.array(self.doc_y)

        model = keras.Sequential()
        model.add(keras.layers.Dense(128, input_shape=(len(training_x[0]),), activation='relu'))
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.Dense(64, activation='relu'))
        model.add(keras.layers.Dropout(0.5))
        model.add(keras.layers.Dense(len(training_y[0]), activation='softmax'))

        model.summary()

        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this
        # model
        sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # fitting and saving the model
        hist = model.fit(training_x, training_y, epochs=200, batch_size=5, verbose=1)
        model.save(os.getcwd()[:-4] + "generated" + '\chatbot_model.h5', hist)


create_model()
