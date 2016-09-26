import string
from collections import Counter
import numpy as np

test_string = 'This is sample test string. String is simple. Test string. Is sample. Another one.'


def clear_text(text):
    return text.lower().translate(string.maketrans('', ''), string.punctuation) 


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
	with open('./../../test_data/GoT1.txt', 'r') as f:
		test_string = f.read()
	text = clear_text(test_string)
	words = text_to_words(text)
	word_dict = words_to_dict(words)
	word_distr = dict_to_distr(word_dict)
	
	next_word = word_distr.keys()[np.random.randint(len(word_distr))]
	generated = generate_text(word_distr, 15)
	print generated
