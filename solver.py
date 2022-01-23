import random
from helpers import get_potential_words


def evaluate_response(last_word, response):
    """Loops through response and sorts valid, invalid, and
    verified characters"""

    evaluation_object = {
        "invalid_chars": [],
        "valid_chars": [],
        "verified_values": [],
        "verified_invalid_values": []
    }

    for index, char in enumerate(response):

        if char == 'X':
            evaluation_object["invalid_chars"].append(last_word[index])
            evaluation_object["verified_invalid_values"].append((last_word[index], index))

        elif char == '$':
            evaluation_object["valid_chars"].append(last_word[index])
            # Note position of this char. We can ignore words that have this char in the same
            # index!
            evaluation_object["verified_invalid_values"].append((last_word[index], index))

        elif char == '#':
            evaluation_object["verified_values"].append((last_word[index], index))

    # removed invalid chars if they were actually found in a specific spot
    verified_chars = [c for c, i in evaluation_object["verified_values"]]
    evaluation_object["invalid_chars"] = [c for c in evaluation_object["invalid_chars"] if c not in verified_chars]

    return evaluation_object


def filter_words(response_eval, words):
    """Whittles down the word list based on
    the games feedback"""

    potential_words = []

    valid_chars = []
    valid_chars = valid_chars + response_eval['valid_chars']
    valid_chars = valid_chars + [c for (c, i) in response_eval['verified_values']]

    # Filter out words with invalid chars
    for word in words:
        valid = True
        for index, char in enumerate(word):

            # If the character is invalid and isn't locked in rule out all words with it
            if char in response_eval['invalid_chars'] and char not in valid_chars:
                valid = False

            # Rule out if char not in right place
            if char in response_eval['invalid_chars'] and char in valid_chars:
                if (char, index) not in response_eval['verified_values']:
                    valid = False

        if valid:
            potential_words.append(word)

    # Filter out words that don't contain valid chars
    invalid_words = []
    for word in potential_words:
        chars = [c for c in word]
        for char in response_eval['valid_chars']:
            if char not in chars:
                invalid_words.append(word)

    potential_words = [p for p in potential_words if p not in invalid_words]

    # Filter for verified chars
    for word in potential_words:
        for verified_char in response_eval["verified_values"]:
            if word[verified_char[1]] != verified_char[0]:
                invalid_words.append(word)

    potential_words = [p for p in potential_words if p not in invalid_words]

    # Filter for valid chars, but that we know must be elsewhere
    # (prevents constantly repeating these characters in same index)
    for word in potential_words:
        for verified_not_char in response_eval["verified_invalid_values"]:
           if word[verified_not_char[1]] == verified_not_char[0]:
                invalid_words.append(word)

    potential_words = [p for p in potential_words if p not in invalid_words]

    return potential_words


def main():

    print("""
    WORDLE SOLVER v1

    X = Not In Word
    $ = In Word, Wrong Position
    # = Right Position

    """)

    complete = False

    words = get_potential_words()
    total_valid_words = len(words)
    word = random.choice(words)

    while not complete:

        print(word)
        response = input("")

        response_eval = evaluate_response(word, response)
        print(response_eval)
        words = filter_words(response_eval, words)

        if len(words) == 1:
            print(f"Answer: {word}")
            complete = True

        elif len(words) < 1:
            print("Answer could not be found")
            complete = True

        else:
            print(f"Matching Words: {len(words)}/{total_valid_words}")

            # Just get the first word for now
            word = words[0]


if __name__ == "__main__":
    main()
