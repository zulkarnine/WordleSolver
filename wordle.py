from words import load_all_words
from enum import Enum

LETTER_COUNT = 5
MAX_ATTEMPT = 10


# Enum for letter verdicts
class LetterVerdict(Enum):
    GREEN = 1
    YELLOW = 2
    GRAY = 3


# Enum for attempt verdict
class AttemptVerdict(Enum):
    WON = 1
    LOST = 2
    FAILED_ATTEMPT = 3
    INVALID_TRY = 4


# Class to simulate playing wordle
class Wordle:
    def __init__(self):
        self.day = 0
        self.five_letter_words = load_all_words(LETTER_COUNT)
        self.attempt = 0
        self.todays_word = self.get_todays_word()
        self.letter_set = set()
        self.reset()

    def get_todays_word(self):
        return self.five_letter_words[self.day % len(self.five_letter_words)]

    # Resets the game
    def reset(self):
        self.attempt = 0
        self.todays_word = self.get_todays_word()
        self.letter_set = set(self.todays_word)

    def next_game(self):
        self.day += 1
        self.reset()

    # Returns true if won
    def guess(self, word):
        if len(word) != LETTER_COUNT:
            print("Give a valid 5 letter word")
            return AttemptVerdict.INVALID_TRY, None

        self.attempt += 1
        if self.attempt > MAX_ATTEMPT:
            print("You've already reached max num of attempts. Try later")
            return AttemptVerdict.LOST, None

        result = []
        for i in range(LETTER_COUNT):
            c = word[i]
            if c == self.todays_word[i]:
                result.append((c, LetterVerdict.GREEN))
            elif c in self.letter_set:
                result.append((c, LetterVerdict.YELLOW))
            else:
                result.append((c, LetterVerdict.GRAY))

        attempt_verdict = AttemptVerdict.WON
        for _, verdict in result:
            if verdict != LetterVerdict.GREEN:
                attempt_verdict = AttemptVerdict.FAILED_ATTEMPT
                break

        print(get_letter_verdicts_colored(result))
        return attempt_verdict, result


def get_letter_verdicts_colored(verdicts):
    if not verdicts:
        return verdicts

    colors = []
    for l, v in verdicts:
        if v == LetterVerdict.GREEN:
            colors.append("🟩️")
        elif v == LetterVerdict.YELLOW:
            colors.append("🟨")
        else:
            colors.append("⬜️")
    return "".join(colors)

def play_single_game(wordle):
    wordle.reset()
    print(wordle.todays_word)
    for i in range(MAX_ATTEMPT):
        guess = input("Guess: ")
        result, letter_verdicts = wordle.guess(guess)
        if result == AttemptVerdict.WON:
            print("Contratz! You've won!")
            return
        # print(letter_verdicts)

    print("Sorry, you've lost the game")


if __name__ == '__main__':
    wordle = Wordle()
    play_single_game(wordle)
