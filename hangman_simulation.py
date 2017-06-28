"""barebones hangman simulator.
NOTE: only works for single words that are within my dictionary.

goal: test every word on hangman, automatically play the best 
letter possible, and see what the hit rate is for each word before 
you've guessed it."""

import time
import numpy as np

from vocabulary import hangman_candidates

# Automatic guesser

wd_lengths = {}

for word in hangman_candidates:
	if len(word) not in wd_lengths:
		wds_lengths[len(word)] = []
	wd_lengths[len(word)].append(word)

def get_possible_words(word_guess, wrong_chars):
	"""Given a word in the format 'p??ho?' and an iterable of wrong characters, 
	returns a list of possible word matches."""
	
	candidates = []
	
	for word in wd_lengths[len(word_guess)]:

		# (1) find words with same right characters.
		elif not same_right(word_guess, word):
			continue

		# (2) find words with same wrong characters.
		elif not same_wrong(wrong_chars, word):
			continue

		candidates.append(word)
candidates
	return 

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

def get_top_guess(word_guess, possible_words):
	"""Given a word guess, and a list of potential words that match up with this word guess,
	determines which letter to try next."""

	potential_letters = {}

	for word in possible_words:
		# list of unique letters not already guessed.
		try_letters = list(set(filter(lambda char: char not in word_guess, word)))
		for char in try_letters:
			potential_letters[char] = potential_letters.get(char, 0) + 1

	letters = sorted(potential_letters.items(), key=lambda letter_tup: letter_tup[1], reverse=True)

	# the only times this should incur an index error are if I've already guessed the word or if the word isn't in hangman_candidates. Solved for both situations.
	return letters[0][0]

# Automatic player

def automatic_hangman(word):
	"""Returns tuple in form:(num tries before solving, 
	number of wrong chars, list of wrong chars)"""

	# if the word isn't in my dictionary, no reason to even try because you'll infinitely recur.
	if word not in hangman_candidates:
		hangman_candidates.append(word)

	word_check = ['?' for char in range(len(word))]
	word_correct = list(word)

	# set starting vals
	tries = 0
	wrong_chars = []
	guess = ''

	while word_correct != word_check:
		tries += 1

		# finds the best next guess
		word_guess = "".join(word_check)
		possible_words = get_possible_words(word_guess, wrong_chars)
		guess = get_top_guess(word_guess, possible_words)

		# replaces things that are right/wrong
		indices = [i for i, val in enumerate(word) if val == guess]
		if len(indices) == 0:
			wrong_chars.append(guess)
		else:
			for i in indices:
				word_check[i] = guess

	return word, tries, len(wrong_chars), wrong_chars

def hangman_stats(sample):
	hangman_words = sorted([automatic_hangman(word) for word in sample], key=lambda word_lst: word_lst[2], reverse=True)

	print "Hardest hangman words to guess (in order of difficulty): {hard}".format(hard=", ".join([word_lst[0] for word_lst in hangman_words[:5] ]))
	print "Average number of wrong characters needed per guess: {av_wrong}".format(av_wrong=round(np.mean([word_lst[2] for word_lst in hangman_words]), 3))

# ---------- Testing area ----------

start = time.time()
automatic_hangman('jazz')
print time.time() - start