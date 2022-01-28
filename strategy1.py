from words import load_all_words, get_letter_freq_sorted_list, get_letter_freq_map
from wordle import AttemptVerdict, LetterVerdict, LETTER_COUNT, MAX_ATTEMPT, get_letter_verdicts_colored

DEB = False

# 1st brute force solver
class WordleSolver1:
    def __init__(self):
        self.all_possible_words = load_all_words(LETTER_COUNT)
        self.invalid_letters = set()
        self.untried_letters = set()
        self.candidate_words = []
        self.green_blocks = set()
        self.yellow_blocks = set()
        self.attempt = 0
        self.game_number = -1
        self.reset()

    def reset(self):
        self.invalid_letters.clear()
        self.candidate_words = list(self.all_possible_words)
        self.yellow_blocks.clear()
        self.green_blocks.clear()
        self.attempt = 0
        self.untried_letters = set(chr(ord('a') + i) for i in range(26))
        self.game_number += 1

    def contains_forbidden_letters(self, word):
        for c in word:
            if c in self.invalid_letters:
                return True
        return False

    def pick_a_word(self):
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

            for yb in self.yellow_blocks:
                letter, index = yb
                if word[index] == letter or letter not in word:
                    no_no = True
                    break

            if not no_no:
                new_candidates.append(word)

        self.candidate_words = new_candidates
        if DEB:
            print(f"Remaining Candidate: {len(self.candidate_words)}")
        freq_map = get_letter_freq_map(self.candidate_words)
        guess = sorted(self.candidate_words, key=lambda word: (-len(set(word)), -sum(freq_map[c] for c in word), word))[0]
        if 1 < self.attempt <= MAX_ATTEMPT - 1 and 0 < len(self.green_blocks) < LETTER_COUNT and len(self.candidate_words) != 1:
            letter_freq = get_letter_freq_sorted_list(self.candidate_words)
            # print(letter_freq)
            letters = list(guess)
            freq_start = 0
            for l, i in self.green_blocks:
                while freq_start < len(letter_freq):
                    high_freq_letter = letter_freq[freq_start][0]
                    if high_freq_letter in self.untried_letters and high_freq_letter not in guess:
                        # just try another probabilistic letter in the green box to rule out or keep.
                        letters[i] = letter_freq[freq_start][0]
                        freq_start += 1
                        break
                    freq_start += 1
            modified_guess = "".join(letters)
            if DEB:
                print(f"Actual guess: {guess} but trying: {modified_guess}")
            return modified_guess

        return guess

    def try_solve(self, wordle):
        # print(f"\nGame: {self.game_number}")
        while True:
            self.attempt += 1
            guess = self.pick_a_word()
            for chr in guess:
                self.untried_letters.discard(chr)
            if DEB:
                print(f"Guessing: {guess}")
            result, letter_verdicts = wordle.guess(guess)
            # print(f"Attempt: {attempt} {get_letter_verdicts_color(letter_verdicts)}")
            if DEB:
                print(get_letter_verdicts_colored(letter_verdicts), end="")

            if result == AttemptVerdict.WON:
                return True
            elif result == AttemptVerdict.LOST:
                return False
            elif result == AttemptVerdict.FAILED_ATTEMPT:
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


def get_letter_verdicts_color(verdicts):
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

