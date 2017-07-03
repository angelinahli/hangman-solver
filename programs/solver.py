"""
A simple Python based hangman solver.

One flaw with this program is that it uses letter based frequency analysis, as opposed to
a word based analysis. Hence, it implicitly weights all words as equally likely to appear
in a hangman game -- additional data weighting the actual frequency of words that appear
in the context of a hangman game could be used to improve this model.
"""

# vocabulary stored in dictionary sorted by length
from vocabulary import sorted_words

##### PT 1: Find the words that might match. #####

def get_possible_words(input_word, wrong_chars, candidate_words):
	"""Given an input word in the format 'p??ho?', wrong characters in 
	dct form {'e': True, 'f': True, 'g': True} and a starting list of
	candidate words, returns a list of possible word matches."""

	new_candidates = []

	for guess in candidate_words:
		if not matching_letters(input_word, guess):
			continue  # implicitly discard if wrong
		if not contains_no_wrong_letters(wrong_chars, guess):
			continue  # implicitly discard if wrong
		new_candidates.append(guess)

	return new_candidates

# helper functions

def matching_letters(input_word, guess):
	"""Given an input word in form 'p??ho?' of the same length as the candidate guess,
	   returns whether the known letters in the input word match the corresponding indices
	   of the candidate guess"""
	for i in range(len(input_word)):
		if input_word[i] != '?' and input_word[i] != guess[i]:
			return False
	return True

def contains_no_wrong_letters(wrong_chars, guess):
	"""Given a dictionary of wrong char guesses, determines whether or not a candidate word 
	contains any letters known to be wrong."""
	guess_chars = set(list(guess)) # iterate only over the unique letters in guess
	for char in guess_chars:
		if char in wrong_chars:
			return False
	return True


##### PT 2: Find the optimal words to try. #####

def get_top_letters(input_word, possible_words):
	"""Given an input word guess, and a list of potential words that match up with this word guess,
	   determines which letters to try next. 
	   Returns list of letter tuples in the format 
	   (letter, probability of matching), sorted by prob accuracy."""

	# all candidates come in lower char form only, so no need to lower again.
	candidate_chars = {}

	for guess in possible_words:
		# set of letters not already guessed.
		# implicitly weights matching 2 letters in a word as having the same value as matching 1
		unguessed_chars = set(filter(lambda char: char not in input_word, guess))

		for c in unguessed_chars:
			candidate_chars[c] = candidate_chars.get(c, 0) + 1

	chars = sorted(candidate_chars.items(), key=lambda letter_tup: letter_tup[1], reverse=True)

	char_probabilities = [ (char_tup[0], float(char_tup[1]) / len(possible_words)) for char_tup in chars]

	return char_probabilities


##### PT 3: Several run options. #####

def print_message(input_word, top_letters, possible_words):
	print "\nYour current guess: {guess}".format(guess=input_word.upper())

	print "\nTop letters to guess next:\n"
	for letter in top_letters[:5]:
		print "{char}: {prob}% probability of match".format(char = letter[0].upper(), prob = round(letter[1]*100, 2))

	print "\nPossible words (total {word_count}):\n".format(word_count = len(possible_words))
	for candidate in possible_words:
		print candidate

def run(input_word, wrong_chars):
	"""input_word = string formatted as 'p??ho?' with '?'s for missing values;
	   wrong_chars = any iterative of wrong_chars 
	   prints top letters to try.
	"""
	# ensure input_word formatting correct
	input_word = input_word.lower()

	# ensure wrong_chars formatting correct
	if not isinstance(wrong_chars, dict):
		wrong_chars = {char: True for char in wrong_chars}

	candidate_words = sorted_words[len(input_word)]
	possible_words = get_possible_words(input_word, wrong_chars, candidate_words)
	top_letters = get_top_letters(input_word, possible_words)

	print_message(input_word, top_letters, possible_words)

def run_interactive():
	input_word = raw_input("Enter your hangman guess here. Enter words you know, and use ? for words you don't know. e.g. 'h?e???' ").lower().strip("'")
	wrong_chars = raw_input("What words have you tried and gotten wrong before? enter with no spaces, e.g. 'acrq' ").lower().strip("'")

	run(input_word, wrong_chars)


##### PT 4: Testing #####

if __name__ == '__main__':
	run_interactive()