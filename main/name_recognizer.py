import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


class NameRecognizer:
    error_names = ['Me']
    tagset = ['NNP', 'FW', 'NN', 'JJ']  # tag set that can possibly identify names in priority order

    def recognizer(self, sentence):
        tokens = nltk.tokenize.word_tokenize(sentence.title())
        pos = nltk.pos_tag(tokens)

        person_name = ''
        for tag in self.tagset:
            person_name = self.__find_the_name(pos, tag)
            if person_name != '':
                return person_name

        return person_name

    def __find_the_name(self, pos, tag_name):
        person_name = ''
        for item in pos:
            print(item)
            print(item[1])
            print(type(item))
            if item[1] == tag_name:
                if item[0] not in self.error_names:
                    person_name = person_name + " " + item[0]
        return person_name
