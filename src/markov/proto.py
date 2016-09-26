import string

test_string = 'This is sample test string. String is simple. Test string.'


def clear_text(text):
    return text.lower().translate(string.maketrans('', ''), string.punctuation) 


def text_to_words(text):
	return text.split()


def text_to_dict(words):
	word_dict = {}
	for i in range(len(words)-1):
		word, next_word = words[i], words[i+1]
		if word in word_dict:
			word_dict[word].append(next_word)
		else:
			word_dict[word] = [next_word]
	return word_dict
