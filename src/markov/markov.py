# -*- coding: utf8 -*-

import re
import string
import codecs
import numpy as np
from collections import Counter, defaultdict


test_string = 'This is sample test string. String is simple. Test string. Is sample. Another one.'

class Markov:

    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))

    def __init__(self, text, n_grams=None):
        """
        text - text to generate Markov chain
        n_grams - array with the list of n-grams to use. Default values is [1, 2]
        """
        if not n_grams:
            n_grams = [1, 2]
        self.n_grams = n_grams
        self.text = text
        self.words = self._text_to_words(self._clear_text(self.text))

        self.word_distr = {}

        for n in self.n_grams:
            word_dict = self._words_to_dict_ngram(self.words, n)
            word_distr = self._dict_to_distr(word_dict)
            for key in word_distr:
                self.word_distr[key] = word_distr[key]

    @classmethod
    def _clear_text(cls, text):
        return cls.punctuation_regex.sub('', text.lower())

    @staticmethod
    def _text_to_words(text):
        return text.split()

    @staticmethod
    def _words_to_dict_ngram(words, n=1):
        word_dict = defaultdict(list)
        for i in range(len(words)-n):
            key = tuple(words[i:i+n])
            next_word = words[i+n]
            word_dict[key].append(next_word)
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

    def _get_next_word(self, key):
        if not (key in self.word_distr and len(self.word_distr[key]) > 0):
            return None
        return np.random.choice(self.word_distr[key].keys(), 1, p=self.word_distr[key].values())[0]

    def generate_bigram(self, text_length=10):
        return self.generate_from_ngram(2, text_length=text_length)

    def generate_from_ngram(self, n, text_length=10):
        word_distr = self.word_distr
        key = word_distr.keys()[np.random.randint(len(word_distr))]
        chosen_words = list(key[:])
        for i in range(text_length - n):
            word = _get_next_word(key)
            if not word:
                break
            chosen_words.append(word)
            key = tuple(chosen_words[-n:])
        return ' '.join(chosen_words)

    def generate(self, text_length=10):
        # Test version for [1, 2] n-grams
        # one_gram_prob = 0.33
        p_distr = [0.3, 0.5, 0.2]

        n = np.random.choice(self.n_grams, 1, p=p_distr)[0]
        word_distr = self.word_distr

        key = word_distr.keys()[np.random.randint(len(word_distr))]
        chosen_words = list(key[:])
        for i in range(text_length - n):
            word = self._get_next_word(key)
            if word is None:
                key = key[1:]
                continue
            chosen_words.append(word)
            n = np.random.choice(self.n_grams, 1, p=p_distr)[0]            
            key = tuple(chosen_words[-n:])
        return ' '.join(chosen_words)


if __name__ == '__main__':
    with open('./../../test_data/test_text.txt', 'r') as f:
        test_string = f.read().decode('UTF-8')

    mark = Markov(test_string, [1, 2, 3])

    with open('./../../test_data/res.txt', 'w+') as f:
        for i in range(20):
            generated = mark.generate(text_length=50)
            f.write(generated.encode('UTF-8'))
            f.write('\n\n=== === ===\n\n')
