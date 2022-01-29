from wordle import Wordle
from strategy1 import WordleSolver1


def run_new_game(wordle, solver):
    wordle.next_game()
    solver.reset()
    # print(f"Actual word: {wordle.todays_word}")
    result = solver.try_solve(wordle)
    # print(f"result {result} attempts: {wordle.attempt}")
    return result, solver.attempt


if __name__ == '__main__':
    wordle = Wordle()
    solver = WordleSolver1()
    for i in range(len(wordle.all_candidate_words)):
        # print(i)
        # if i % 10 == 0:
        #     print(f"Game: {i}")
        result, attempt = run_new_game(wordle, solver)
        if not result or attempt > 6:
            print(wordle.todays_word, attempt)
        # print()