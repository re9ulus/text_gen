# -*- coding: utf8 -*-

import re
import string
from collections import Counter
import numpy as np
import codecs


test_string = 'This is sample test string. String is simple. Test string. Is sample. Another one.'


def clear_text(text):
    #translate(string.maketrans('', ''), string.punctuation) # don't work with cyliric characters
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    return regex.sub('', text.lower())


def text_to_words(text):
    return text.split()


def words_to_dict(words):
    word_dict = {}
    for i in range(len(words)-1):
        word, next_word = words[i], words[i+1]
        if word in word_dict:
            word_dict[word].append(next_word)
        else:
            word_dict[word] = [next_word]
    return word_dict


def dict_to_distr(word_dict):
    word_distr = {}
    for word in word_dict:
        list_len = len(word_dict[word])
        word_counts = Counter(word_dict[word])
        word_distr[word] = {}
        for target_word in word_counts:
            word_distr[word][target_word] = word_counts[target_word] / float(list_len)
    return word_distr


def generate_text(word_distr, text_length=10):
    text = ''
    next_word = word_distr.keys()[np.random.randint(len(word_distr))]
    text = next_word
    for i in range(text_length):
        if not (next_word in word_distr and len(word_distr[next_word]) > 0):
            continue
        next_word = np.random.choice(word_distr[next_word].keys(), 1, p=word_distr[next_word].values())[0]
        text += ' ' + next_word
    return text


if __name__ == '__main__':
    # with codecs.open('./../../test_data/Voina i mir 1.txt', 'r', 'UTF-8', errors='ignore') as f: # './../../test_data/GoT1.txt'
    #   test_string = f.read()

    with open('./../../test_data/Voina i mir 1.txt', 'r') as f:
        test_string = f.read().decode('UTF-8')

    text = clear_text(test_string)
    words = text_to_words(text)
    word_dict = words_to_dict(words)
    word_distr = dict_to_distr(word_dict)
    
    
    with open('res.txt', 'w+') as f:
        for i in range(20):
            generated = generate_text(word_distr, 10)
            f.write(generated.encode('UTF-8'))
            f.write('\n\n=== === ===\n\n')
