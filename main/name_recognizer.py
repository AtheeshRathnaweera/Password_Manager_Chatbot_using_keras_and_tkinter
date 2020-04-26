import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


class NameRecognizer:

    @staticmethod
    def recognizer(sentence):
        error_names = ['Me']
        tokens = nltk.tokenize.word_tokenize(sentence.title())
        pos = nltk.pos_tag(tokens)

        person_name = ''
        for item in pos:
            print(item[1])
            print(type(item))
            if item[1] == 'NNP':
                if item[0] not in error_names:
                    person_name = person_name + " " + item[0]

        print(person_name)
        return person_name
