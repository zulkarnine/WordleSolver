from wordle import Wordle
from solver import WordleSolver


def run_new_game(wordle, solver):
    wordle.next_game()
    solver.reset()
    # print(f"Actual word: {wordle.todays_word}")
    result = solver.solve(wordle)
    # print(f"result {result} attempts: {wordle.attempt}")
    return result, solver.attempt


def run_benchmark():
    wordle = Wordle()
    solver = WordleSolver()
    failed_attempts = []
    total_games = wordle.max_word_count()
    for i in range(total_games):
        if i % 100 == 0:
            print(f"Progress: ran {i} games")
        result, attempt = run_new_game(wordle, solver)
        if not result:
            fail = (wordle.todays_word, solver.game_number, solver.attempt, solver.tries[:])
            print(fail)
            failed_attempts.append(fail)
    print(f"Ran: {total_games} games.")
    print(
        f"Solved: {total_games - len(failed_attempts)}/{total_games} = {((total_games - len(failed_attempts)) * 100 / total_games):.02f}%")

    print("\nDetails:")
    for fail in failed_attempts:
        print(fail)


if __name__ == '__main__':
    run_benchmark()
