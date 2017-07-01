"""
A simple Python based hangman solver.

One flaw with this program is that it uses letter based frequency analysis, as opposed to
a word based analysis. Hence, it implicitly weights all words as equally likely to appear
in a hangman game -- additional data weighting the actual frequency of words that appear
in the context of a hangman game could be used to improve this model.
"""

from vocabulary import hangman_candidates

##### PT 1: Find the words that might match. #####

# Sort words into dictionary to make searching easier
sorted_words = {}

for word in hangman_candidates:
	sorted_words[len(word)] = sorted_words.get(len(word), []).append(word)

def get_possible_words(input_word, wrong_letters):
	"""Given an input word in the format 'p??ho?' and wrong characters in dct form {'e': True, 'f': True, 'g': True}, 
	returns a list of possible word matches."""

	# Uses only words that have the same length as the word guess
	candidates = sorted_words[len(word_guess)]

	for guess in candidates:

		if not matching_letters(input_word, guess):
			candidates.remove(guess)

		elif not contains_no_wrong_letters(wrong_letters, guess):
			candidates.remove(guess)

	return candidates

# helper functions

def matching_letters(input_word, guess):
	"""Given an input word in form 'p??ho?' of the same length as the candidate guess,
	   returns whether the known letters in the input word match the corresponding indices
	   of the candidate guess"""
	for i in range(len(input_word)):
		if input_word[i] != '?' and input_word[i] != guess[i]:
			return False # If at any point a known letter of the input word deviates from the candidate word, return false
	return True

def contains_no_wrong_letters(wrong_letters, guess):
	"""Given a dictionary of wrong letter guesses, determines whether or not a candidate word 
	contains any letters known to be wrong."""

	guess_chars = set(list(guess)) # iterate only over the unique letters in guess

	for char in guess_chars:
		if char in wrong_letters:
			return False
	return True

# PT 2: Find the optimal words to try.

def get_top_letters(word_guess, possible_words):
	"""Given a word guess, and a list of potential words that match up with this word guess,
	determines which letters to try next. returns list of letter tuples in the format
	(letter, probability of matching), sorted by prob accuracy."""

	potential_letters = {}

	for word in possible_words:

		# list of unique letters not already guessed.
		try_letters = list(set(filter(lambda char: char not in word_guess, word)))

		for char in try_letters:
			potential_letters[char] = potential_letters.get(char, 0) + 1

	letters = sorted(potential_letters.items(), key=lambda letter_tup: letter_tup[1], reverse=True)

	letters_w_probs = [(tup[0], float(tup[1])/len(possible_words)) for tup in letters]

	return letters_w_probs

def run():
	word_guess = raw_input("Enter your hangman guess here. Enter words you know, and use ? for words you don't know. e.g. 'h?e???' ").lower()
	wrong_chars = raw_input("What words have you tried and gotten wrong before? enter with no spaces, e.g. 'acrq' ").lower()

	possible_words = get_possible_words(word_guess, wrong_chars)
	top_letters = get_top_letters(word_guess, possible_words)

	print "Your current guess: {}".format(word_guess)
	
	# Best guesses
	print "\nBest letter guesses:\n"
	for letter in top_letters[:5]: 
		print "{char}: {prob}% probability of match".format(char = letter[0], prob = round(letter[1]*100, 2))

	# Possible words
	print "\nPossible words (total {}):\n".format(len(possible_words))
	for word in possible_words:
		print word

# ----------- TESTING AREA --------------

run()
