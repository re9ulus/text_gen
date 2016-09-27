# -*- coding: utf8 -*-

import re
import string
from collections import Counter
import numpy as np
import codecs


test_string = 'This is sample test string. String is simple. Test string. Is sample. Another one.'

class Markov:

    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))

    def __init__(self, text):
        self.text = text
        self.words = self._text_to_words(self._clear_text(self.text))
        self.word_distr = self._dict_to_distr(self._words_to_dict(self.words))

    @classmethod
    def _clear_text(cls, text):
        #translate(string.maketrans('', ''), string.punctuation) # don't work with cyliric characters
        return cls.punctuation_regex.sub('', text.lower())

    @staticmethod
    def _text_to_words(text):
        return text.split()

    @staticmethod
    def _words_to_dict(words):
        word_dict = {}
        for i in range(len(words)-1):
            word, next_word = words[i], words[i+1]
            if word in word_dict:
                word_dict[word].append(next_word)
            else:
                word_dict[word] = [next_word]
        return word_dict

    @staticmethod
    def _dict_to_distr(word_dict):
        word_distr = {}
        for word in word_dict:
            list_len = len(word_dict[word])
            word_counts = Counter(word_dict[word])
            word_distr[word] = {}
            for target_word in word_counts:
                word_distr[word][target_word] = word_counts[target_word] / float(list_len)
        return word_distr


    def generate(self, text_length=10):
        text = ''
        next_word = self.word_distr.keys()[np.random.randint(len(self.word_distr))]
        text = next_word
        for i in range(text_length):
            if not (next_word in self.word_distr and len(self.word_distr[next_word]) > 0):
                break
            next_word = np.random.choice(self.word_distr[next_word].keys(), 1, p=self.word_distr[next_word].values())[0]
            text += ' ' + next_word
        return text


if __name__ == '__main__':
    # with codecs.open('./../../test_data/Voina i mir 1.txt', 'r', 'UTF-8', errors='ignore') as f: # './../../test_data/GoT1.txt'
    #   test_string = f.read()

    with open('./../../test_data/test_text.txt', 'r') as f:
        test_string = f.read().decode('UTF-8')

    mark = Markov(test_string)
    
    with open('res.txt', 'w+') as f:
        for i in range(20):
            generated = mark.generate()
            f.write(generated.encode('UTF-8'))
            f.write('\n\n=== === ===\n\n')
