from wordle_solver import Solver
from wordle_challenge import Challenge
import csv

def main():

    print("""
    WORDLE Analyzer v1
    """)

    WORDLE_WORDS_FILE = "wordle_words.csv"
    words = []

    with open(WORDLE_WORDS_FILE, 'r') as word_file:
        reader = csv.reader(word_file, delimiter=',')
        for row in reader:
            words.append(row[0])

    total_words = len(words)

    for starting_word in words:

        successes = 0

        for answer in words:

            success = False
            tries = 6

            solver = Solver(starting_word=starting_word, words=words)
            challenge = Challenge(answer=answer, words=words)

            while not challenge.game_over:
                result = challenge.check_answer(solver.current_guess)

                if result == "#####":
                    success = True
                    tries = 6 - challenge.guesses_left
                    challenge.game_over = True

                else:
                    end, _ = solver.process_response(result)
                    if end:
                        challenge.game_over = True

            print(f"{success} in {tries} tries")
            if success:
                successes = successes + 1

        print(f"{starting_word} - {successes}/{total_words}")

if __name__ == "__main__":
    main()
