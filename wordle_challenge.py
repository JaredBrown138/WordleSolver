import csv
import random


class Challenge():
    """Represents a game of wordle"""

    WORDLE_WORDS_FILE = "wordle_words.csv"

    guesses_left = 6
    game_over = False
    answer = None
    words = []

    class NoMoreGuessesException(Exception):
        """What are you doing!?"""

    def __init__(self, answer=None, words=None):

        if words is None:
            self._load_wordle_words()
        else:
            self.words = words

        if answer is None:
            self.answer = random.choice(self.words)
        else:
            self.answer = answer

    def _load_wordle_words(self):
        """Loads words from the wordle words file"""
        with open(self.WORDLE_WORDS_FILE, 'r') as word_file:
            reader = csv.reader(word_file, delimiter=',')
            for row in reader:
                self.words.append(row[0])

    def check_answer(self, guess):
        """Take a guess and return a result string"""

        if self.guesses_left < 1:
            raise self.NoMoreGuessesException()

        result = ""

        answer_letters = [char for char in self.answer]
        answer_letter_positions = [(char, index) for index, char in enumerate(self.answer)]

        for index, char in enumerate(guess):

            if char not in answer_letters:
                result = result + "X"

            elif (char, index) in answer_letter_positions:
                result = result + "#"

            else:
                result = result + "$"

        self.guesses_left = self.guesses_left - 1
        if self.guesses_left < 1:
            self.game_over = True
        return result
