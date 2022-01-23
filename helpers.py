
import csv


def get_potential_words():
    """Returns a list of words"""

    wordle_words = []
    wordle_words_file = "wordle_words.csv"

    with open(wordle_words_file, 'r') as w_file:
        reader = csv.reader(w_file, delimiter=',')
        for row in reader:
            wordle_words.append(row[0])

    return wordle_words
