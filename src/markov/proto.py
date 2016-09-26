import string
from collections import Counter

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


if __name__ == '__main__':
	text = clear_text(test_string)
	words = text_to_words(text)
	word_dict = words_to_dict(words)
	word_distr = dict_to_distr(word_dict)
	print word_distr
