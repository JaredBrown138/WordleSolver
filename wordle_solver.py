import csv
import random
import time

class Solver():
    """Represents a solving instance. This includes the data
    and methods need to solve a Wordle problem"""

    WORDLE_WORDS_FILE = "wordle_words.csv"
    VALID_RESPONSE_CHARS = ['$', 'X', '#']

    words = []
    total_word_count = 0
    current_guess = None
    solve_completed = False
    verbose_printing = False

    evaluation_state = {
        "invalid_chars": [],
        "valid_chars": [],
        "verified_values": [],
        "verified_invalid_values": []
    }

    def __init__(self, verbose_printing=False, starting_word=None, words=None):

        if words is None:
            self._load_wordle_words()
        else:
            self.words = words

        self.total_word_count = len(self.words)

        if starting_word is None:
            self.current_guess = random.choice(self.words)
        else:
            self.current_guess = starting_word

        self.verbose_printing = verbose_printing

    def _load_wordle_words(self):
        """Loads words from the wordle words file"""
        with open(self.WORDLE_WORDS_FILE, 'r') as word_file:
            reader = csv.reader(word_file, delimiter=',')
            for row in reader:
                self.words.append(row[0])

    def _update_evaluation_state(self, response):

        for index, char in enumerate(response):

            if char == 'X':
                self.evaluation_state["invalid_chars"].append(self.current_guess[index])
                self.evaluation_state["verified_invalid_values"].append((self.current_guess[index], index))

            elif char == '$':
                self.evaluation_state["valid_chars"].append(self.current_guess[index])
                # Note position of this char. We can ignore words that have this char in the same
                # index!
                self.evaluation_state["verified_invalid_values"].append((self.current_guess[index], index))

            elif char == '#':
                self.evaluation_state["verified_values"].append((self.current_guess[index], index))

            # removed invalid chars if they were actually found in a specific spot
            verified_chars = [c for c, i in self.evaluation_state["verified_values"]]
            self.evaluation_state["invalid_chars"] = [c for c in self.evaluation_state["invalid_chars"] if c not in verified_chars]

    def _contains_valid_letter(self, word, valid_chars):
        for char in valid_chars:
            if char not in word:
                return False
        return True

    def _contains_invalid_letter(self, word, invalid_chars):
        for char in invalid_chars:
            if char in word:
                return True
        return False

    def _contains_valid_char_pos(self, word, char_pos_list):
        word_char_pos_list = [(c, i) for i, c in enumerate(word)]
        for char_pos in char_pos_list:
            if char_pos not in word_char_pos_list:
                return False
        return True

    def _filter_words(self):

        # start = time.time()

        potential_words = []

        valid_chars = []
        valid_chars = valid_chars + self.evaluation_state['valid_chars']
        valid_chars = valid_chars + [c for (c, i) in self.evaluation_state['verified_values']]

        # We might have a so called invalid character (grey) even if that letter
        # is locked in (green) somewhere else in the word, in that case ignore it.
        # the lock in takes precedent.
        invalid_chars = [char for char in self.evaluation_state['invalid_chars'] if char not in valid_chars]

        potential_words = [word for word in self.words if self._contains_valid_letter(word, valid_chars)]
        potential_words = [word for word in potential_words if self._contains_valid_char_pos(word, self.evaluation_state['verified_values'])]
        potential_words = [word for word in potential_words if not self._contains_invalid_letter(word, invalid_chars)]
        # TODO: Add back in rule out known bad positions

        self.words = potential_words

        # print(f"Filter took {time.time() - start} seconds")

    def process_response(self, response):
        """Evaluate the response string and start filtering
        based on the response feedback"""

        if len(response) != 5:
            return (False, f"Response should contain 5 characters!")

        for char in response:
            if char not in self.VALID_RESPONSE_CHARS:
                return (False, f"Response contains invalid character: {char}")

        self._update_evaluation_state(response)
        self._filter_words()

        # print(f"Matching Words: {len(self.words)}/{self.total_word_count}")

        if len(self.words) == 1:
            self.solve_completed = True
            return (True, self.words[0])

        if len(self.words) < 1:
            self.solve_completed = True
            return (True, "Could not arrive at solution")

        self.current_guess = self.words[0]
        return (False, self.current_guess)
