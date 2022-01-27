import csv
import random


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

    def _filter_words(self):
        """Filters words in the words list using the evaluation state"""

        potential_words = []

        valid_chars = []
        valid_chars = valid_chars + self.evaluation_state['valid_chars']
        valid_chars = valid_chars + [c for (c, i) in self.evaluation_state['verified_values']]

        # Filter out words with invalid chars
        for word in self.words:
            valid = True
            for index, char in enumerate(word):

                # If the character is invalid and isn't locked in rule out all words with it
                if char in self.evaluation_state['invalid_chars'] and char not in valid_chars:
                    valid = False

                # Rule out if char not in right place
                if char in self.evaluation_state['invalid_chars'] and char in valid_chars:
                    if (char, index) not in self.evaluation_state['verified_values']:
                        valid = False

            if valid:
                potential_words.append(word)

        # Filter out words that don't contain valid chars
        invalid_words = []
        for word in potential_words:
            chars = [c for c in word]
            for char in self.evaluation_state['valid_chars']:
                if char not in chars:
                    invalid_words.append(word)

        potential_words = [p for p in potential_words if p not in invalid_words]

        # Filter for verified chars
        for word in potential_words:
            for verified_char in self.evaluation_state["verified_values"]:
                if word[verified_char[1]] != verified_char[0]:
                    invalid_words.append(word)

        potential_words = [p for p in potential_words if p not in invalid_words]

        # Filter for valid chars, but that we know must be elsewhere
        # (prevents constantly repeating these characters in same index)
        for word in potential_words:
            for verified_not_char in self.evaluation_state["verified_invalid_values"]:
                if word[verified_not_char[1]] == verified_not_char[0]:
                        invalid_words.append(word)

        potential_words = [p for p in potential_words if p not in invalid_words]
        self.words = potential_words

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

        print(f"Matching Words: {len(self.words)}/{self.total_word_count}")

        if len(self.words) == 1:
            self.solve_completed = True
            return (True, self.words[0])

        if len(self.words) < 1:
            self.solve_completed = True
            return (True, "Could not arrive at solution")

        self.current_guess = self.words[0]
        return (False, self.current_guess)
