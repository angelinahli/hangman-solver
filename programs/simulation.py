"""
Simulates a game of hangman, by pitting the hangman solver against a series of words.
Uses simulation to generate hangman gameplay analysis on which hangman words are the
most difficult for the solver to guess.
"""

import time
import csv
import numpy as np

from vocabulary import sorted_words
from solver import get_possible_words


##### PT 1: Define helper functions #####

def get_top_letter(input_word, possible_words):
	"""Given an input word guess, and a list of potential words that match up with this word guess,
	   determines optimal next letter to guess."""

	candidate_chars = {}
	for guess in possible_words:
		unguessed_chars = set(filter(lambda char: char not in input_word, guess))

		for c in unguessed_chars:
			candidate_chars[c] = candidate_chars.get(c, 0) + 1

	chars = sorted(candidate_chars.items(), key=lambda letter_tup: letter_tup[1], reverse=True)

	return chars[0][0]


##### PT 2: Automatically use solver to play a game #####

def automatic_hangman(word):
	"""Returns tuple in form:(word, num tries before solving, 
	number of chars guessed wrong, list of wrong chars)"""

	# if the word isn't in my dictionary, add to the dictionary.
	if word not in sorted_words[len(word)]:
		sorted_words[len(word)] += [word]

	input_word_lst = ['?' for char in range(len(word))]
	correct_word_lst = list(word)

	# define initial set of candidate words
	possible_words = get_possible_words(input_word_lst, '', sorted_words[len(word)])

	tries = 0
	wrong_chars = {}
	start_time = time.time()

	while input_word_lst != correct_word_lst:
		tries += 1

		# finds the best next guess
		input_word = ''.join(input_word_lst)
		guess = get_top_letter(input_word, possible_words)

		# replaces values that are correct
		if guess in correct_word_lst:
			guessed_indices = [i for i, val in enumerate(correct_word_lst) if val==guess]
			for i in guessed_indices:
				input_word_lst[i] = guess
		
		# otherwise, adds to the list of wrong chars	
		else:
			wrong_chars[guess] = True

		# narrow possible words to make more efficient
		possible_words = get_possible_words(input_word_lst, wrong_chars, possible_words)

	return word, tries, len(wrong_chars), len(word)


##### PT 3: Run simulator on select sample to generate statistics #####

def hangman_stats(sample):
	hangman_words = sorted([automatic_hangman(word) for word in sample], key=lambda word_lst: word_lst[2], reverse=True)

	print "Hardest hangman words to guess (in order of difficulty): {hard}".format(hard=", ".join([word_lst[0] for word_lst in hangman_words[:5] ]))
	print "Average number of wrong characters needed per guess: {av_wrong}".format(av_wrong=round(np.mean([word_lst[2] for word_lst in hangman_words]), 3))


##### PT 4: Testing #####

if __name__ == '__main__':
	sample = ['apple', 'pear', 'gorilla', 'horse', 'zebra', 'chimpanzee', 'hair', 'nonchalant', 'interesting', 'python', 'horrible', 'tin', 'taunt']
	start = time.time()

	# actions here


	time = time.time() - start
	print "time:", time
	print "avg_time:", time/len(sample)

