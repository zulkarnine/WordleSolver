from words import load_all_words, get_letter_freq_sorted_list, get_letter_freq_map, get_all_wordle_words
from wordle import AttemptVerdict, LetterVerdict, LETTER_COUNT, MAX_ATTEMPT, get_letter_verdicts_colored, Wordle
from itertools import permutations
from collections import Counter

DEB = False

# 1st brute force solver
class WordleSolver1:
    def __init__(self):
        self.all_possible_words = set(get_all_wordle_words()) # set(load_all_words(LETTER_COUNT))
        self.invalid_letters = set()
        self.untried_letters = set()
        self.candidate_words = []
        self.green_blocks = set()
        self.yellow_blocks = set()
        self.attempt = 0
        self.game_number = -1
        self.tries = []
        self.reset()

    def reset(self):
        self.invalid_letters.clear()
        self.candidate_words = list(self.all_possible_words)
        self.yellow_blocks.clear()
        self.green_blocks.clear()
        self.attempt = 0
        self.untried_letters = set(chr(ord('a') + i) for i in range(26))
        self.game_number += 1
        self.tries.clear()

    def contains_forbidden_letters(self, word):
        for c in word:
            if c in self.invalid_letters:
                return True
        return False

    def get_untried_letter_probability(self):
        counter = Counter()
        for word in self.candidate_words:
            for c in word:
                if c in self.untried_letters:
                    counter[c] += 1
        return sorted(counter.items(), key=lambda item: (-item[1], item[0]))

    def get_green_letter_substituted_valid_word(self, actual_word):
        replacing_indexes = [index for _, index in self.green_blocks]
        if not replacing_indexes:
            return actual_word

        letters = list(actual_word)
        untried_letters = self.get_untried_letter_probability()
        candidate_untried_letters = [letter for letter, _ in untried_letters]
        perm = permutations(candidate_untried_letters, len(replacing_indexes))
        for p in perm:
            for i in range(len(replacing_indexes)):
                letters[replacing_indexes[i]] = p[i]
            possible_word = "".join(letters)
            if possible_word in self.all_possible_words:
                return possible_word
        # Couldn't find a suitable word to explore
        return actual_word

    def filter_out_invalid_words(self):
        new_candidates = []
        for word in self.candidate_words:
            if self.contains_forbidden_letters(word):
                continue

            no_no = False
            for gb in self.green_blocks:
                letter, index = gb
                if word[index] != letter:
                    no_no = True
                    break

            if no_no:
                continue

            for yb in self.yellow_blocks:
                letter, index = yb
                if word[index] == letter or letter not in word:
                    no_no = True
                    break

            if not no_no:
                new_candidates.append(word)

        self.candidate_words = new_candidates

    def make_educated_guess(self):
        untried_letters = dict(self.get_untried_letter_probability())
        if len(untried_letters) > 1 and self.attempt <= MAX_ATTEMPT - 2:
            word_with_score = []
            word_list = self.all_possible_words #if (self.attempt <= MAX_ATTEMPT - 2 and len(untried_letters) >= LETTER_COUNT) else self.candidate_words
            for word in word_list:
                score = 0
                letters = set(word)
                for c in letters:
                    if c in untried_letters:
                        score += untried_letters[c]
                word_with_score.append((word, score))
            ranked_words = sorted(word_with_score,
                                  key=lambda item: (-item[1], item[0]))
            guess = ranked_words[0][0]
        else:
            freq_map = get_letter_freq_map(self.candidate_words)
            guess = sorted(self.candidate_words, key=lambda word: (-len(set(word)), -sum(freq_map[c] for c in word), word))[0]
        return guess

    def maybe_substitute_green_letters(self, guess):
        # if 1 < self.attempt <= MAX_ATTEMPT - 2 and 0 < len(self.green_blocks) < LETTER_COUNT and len(self.candidate_words) != 1:
        #     new_word = self.get_green_letter_substituted_valid_word(guess)
        #
        #     if DEB and guess != new_word:
        #         print(f"Actual guess: {guess} but trying: {new_word}")
        #     return new_word
        return guess

    def pick_a_word(self):
        self.filter_out_invalid_words()

        if len(self.candidate_words) == 0:
            print("Game's word doesn't exist in our dictionary.")
            exit(1)

        if DEB:
            print(f"Remaining Candidate: {len(self.candidate_words)}")

        if len(self.candidate_words) == 1:
            return self.candidate_words[0]

        guess = self.make_educated_guess()
        return self.maybe_substitute_green_letters(guess)

    def try_solve(self, wordle):
        # print(f"\nGame: {self.game_number}")
        while True:
            self.attempt += 1
            guess = self.pick_a_word()
            if DEB:
                print(f"Guessing: {guess}")
            result, letter_verdicts = wordle.guess(guess)
            self.tries.append(guess)
            # print(f"Attempt: {attempt} {get_letter_verdicts_color(letter_verdicts)}")
            if DEB:
                print(get_letter_verdicts_colored(letter_verdicts), end="")

            if result == AttemptVerdict.WON:
                return True
            elif result == AttemptVerdict.LOST:
                return False
            elif result == AttemptVerdict.FAILED_ATTEMPT:
                for chr in guess:
                    self.untried_letters.discard(chr)
                for i in range(len(letter_verdicts)):
                    letter, verdict = letter_verdicts[i]
                    if verdict == LetterVerdict.GRAY:
                        self.invalid_letters.add(letter)
                    elif verdict == LetterVerdict.GREEN:
                        self.green_blocks.add((letter, i))
                        if (letter, i) in self.yellow_blocks:
                            self.yellow_blocks.remove((letter, i))
                    elif verdict == LetterVerdict.YELLOW:
                        self.yellow_blocks.add((letter, i))
                    else:
                        exit(1)
            elif result == AttemptVerdict.INVALID_WORD:
                self.attempt -= 1
                self.candidate_words.remove(guess)
                self.all_possible_words.remove(guess)


if __name__ == '__main__':
    wordle = Wordle()
    solver = WordleSolver1()
    DEB = True
    for i in range(5):
        wordle.reset()
        solver.reset()
        solver.try_solve(wordle)

