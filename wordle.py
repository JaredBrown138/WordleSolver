from wordle_solver import Solver


def main():

    print("""
    WORDLE SOLVER v1

    X = Not In Word
    $ = In Word, Wrong Position
    # = Right Position

    """)

    solver = Solver(verbose_printing=True)
    # total_valid_words = len(solver.words)
    print(solver.current_guess)

    while not solver.solve_completed:
        response = input("")
        print(solver.process_response(response))


if __name__ == "__main__":
    main()
