"""
A simple Python based hangman solver.

One flaw with this program is that it uses letter based frequency analysis, as opposed to
a word based analysis. Hence, it implicitly weights all words as equally likely to appear
in a hangman game -- additional data weighting the actual frequency of words that appear
in the context of a hangman game could be used to improve this model.
"""

from vocabulary import hangman_candidates

# PT 1: Find the words that might match.

def get_possible_words(word_guess, wrong_chars):
	"""Given a word in the format 'p??ho?' and wrong characters in format 'ezq', 
	returns a list of possible word matches."""

	candidates = []

	for word in hangman_candidates:

		# (1) find words with same length.
		if len(word) != len(word_guess):
			continue

		# (2) find words with same right characters.
		elif not same_right(word_guess, word):
			continue

		# (3) find words with same wrong characters.
		elif not same_wrong(wrong_chars, word):
			continue

		candidates.append(word)

	return candidates

# helper functions

def same_right(guess, word):
	"""Given a word guess in format 'p??ho?' and a candidate word of the same length, 
	determines whether the word could match up with the guess."""
	for i in range(len(guess)):
		if guess[i] != '?' and guess[i] != word[i]:
			return False # If at any point a known char of the guess deviates from the candidate word, return false
	return True

def same_wrong(wrong_chars, word):
	"""Given a list of wrong characters, determines whether or not a candidate word 
	contains any characters known to be wrong."""
	for char in word:
		if char in wrong_chars:
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
