"""
Generates data on all the words in my dictionary
Word list used to generate data removed from document to save space

Total run time on 61000+ words: 1.44 hours / 5179.22246504 seconds
    (Most time spent on generating hangman stats)
"""

import time
import csv

from simulation import automatic_hangman

def hangman_stats_doc(sample, filename):
    header = ['word','tries','wrong','len_word','cont_unusual'] + ['cont_' + char for char in 'abcdefghijklmnopqrstuvwxyz']
    
    start_time = time.time() # for printing purposes
    
    all_lines = []
    for i in range(len(sample)):
        word = sample[i]
        line_data = list(automatic_hangman(word)) + [contains_unusual_chars(word)] + contain_all_chars(word)
        all_lines.append(line_data)

        if i % 1000 == 0:
            print "making stats - on line:", i, " time elapsed:", time.time() - start_time, "secs"

    print '\n'

    with open ('{filename}.csv'.format(filename=filename), 'wb') as stats_file:
        stats_writer = csv.writer(stats_file, delimiter=',')

        stats_writer.writerow(header)
        for i in range(len(all_lines)):
            stats_writer.writerow(all_lines[i])

            if i % 1000 == 0:
                print "write to csv - on line", i, " time elapsed:", time.time() - start_time, "secs"

    print "Complete!"

def contains_unusual_chars(word):
    # unusual characters are defined as characters in the last quartile of frequency usage, taken from 
    # https://en.oxforddictionaries.com/explore/which-letters-are-used-most
    unusual_chars = {char: True for char in 'wkvxzjq'}
    word_chars = set(list(word))

    for char in word_chars:
        if char in unusual_chars:
            return 1
    return 0

def contain_all_chars(word):
    """returns list of which chars are in word (in alphabetical order)"""
    word = set(list(word))
    return [char_in_word(word, char) for char in 'abcdefghijklmnopqrstuvwxyz']

def char_in_word(word, char):
    if char in word:
        return 1
    else:
        return 0

