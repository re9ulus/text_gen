# -*- coding: utf8 -*-

import re
import string
from collections import Counter, defaultdict
import numpy as np
import codecs


test_string = 'This is sample test string. String is simple. Test string. Is sample. Another one.'

class Markov:

    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))

    def __init__(self, text):
        self.text = text
        self.words = self._text_to_words(self._clear_text(self.text))
        self.word_dict = self._words_to_dict_bigram(self.words)
        self.word_distr = self._dict_to_distr(self.word_dict)

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
    def _words_to_dict_bigram(words):
        word_dict = {}
        for i in range(len(words)-2):
            word1, word2, next_word = words[i:i+3]
            key = (word1, word2)
            if key in word_dict:
                word_dict[key].append(next_word)
            else:
                word_dict[key] = [next_word]
        return word_dict

    @staticmethod
    def _words_to_dict_ngram(words, n=2):
        word_dict = defaultdict(list)
        for i in range(len(words)-n):
            key = tuple(words[i:i+n])
            next_word = words[i+n]
            word_dict[key] = next_word
        return word_dict

    @staticmethod
    def _dict_to_distr(word_dict):
        word_distr = {}
        for key in word_dict:
            list_len = len(word_dict[key])
            word_counts = Counter(word_dict[key])
            word_distr[key] = {}
            for target_word in word_counts:
                word_distr[key][target_word] = word_counts[target_word] / float(list_len)
        return word_distr

    def generate(self, text_length=10):
        text = ''
        next_word = self.word_distr.keys()[np.random.randint(len(self.word_distr))]
        text = next_word
        for i in range(text_length):
            next_word = self.get_next_word(key, self.word_distr)
            if not next_word:
                break
            text += ' ' + next_word
        return text

    def generate_bigram(self, text_length=10):
        text = ''
        key = self.word_distr.keys()[np.random.randint(len(self.word_distr))]
        text = ' '.join(key)
        for i in range(text_length - len(key)):
            next_word = self.get_next_word(key, self.word_distr)
            if not next_word:
                break
            text += ' ' + next_word
            key = (key[-1], next_word)
        return text

    def generate_from_ngram(self, text_length=10):
        text = ''
        key = self.word_distr.keys()[np.random.randint(len(self.word_distr))]
        text = ' '.join(key)
        for i in range(text_length - len(key)):
            next_word = self.get_next_word(key, self.word_distr)
            if not next_word:
                break
            text += ' ' + next_word
            key = (key[-1], next_word)
        return text

    def get_next_word(self, key, word_distr):
        if not (key in word_distr and len(word_distr[key]) > 0):
            return None
        return np.random.choice(word_distr[key].keys(), 1, p=word_distr[key].values())[0]


if __name__ == '__main__':
    # with codecs.open('./../../test_data/Voina i mir 1.txt', 'r', 'UTF-8', errors='ignore') as f: # './../../test_data/GoT1.txt'
    #   test_string = f.read()

    with open('./../../test_data/test_text.txt', 'r') as f:
        test_string = f.read().decode('UTF-8')

    mark = Markov(test_string)
    # print mark.word_distr

    with open('./../test_data/res.txt', 'w+') as f:
        for i in range(20):
            generated = mark.generate_bigram(text_length=15)
            f.write(generated.encode('UTF-8'))
            f.write('\n\n=== === ===\n\n')
