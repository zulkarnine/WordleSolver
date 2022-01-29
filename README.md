# WordleSolver

&copy; Zulkarnine, 2022.

Algorithm to solve [Wordle](https://www.powerlanguage.co.uk/wordle/) 100% of the time within 6 attempts.

- You can go ahead and run `main.py` to run it for all 2315 Wordle words and it solves 100% of them correctly within **6 attempts**.
**Example output:**
```
Ran: 2315 games.
Solved: 2315/2315 = 100.00%
```

- You can also run `solver.py` to get a sense of how it's guessing and what is the `Wordle` game simulation returning. (I.e. the colored blocks)

**Example output:**
```
====================
Game: 1
====================
Remaining Candidate: 2315
Guessing: alert 🟩️⬜️⬜️⬜️⬜️ Remaining Candidate: 20
Guessing: noisy ⬜️⬜️⬜️⬜️⬜️ Remaining Candidate: 1
Guessing: aback 🟩️🟩️🟩️🟩️🟩️ Actual word: aback

====================
Game: 2
====================
Remaining Candidate: 2315
Guessing: alert 🟩️⬜️🟨⬜️⬜️ Remaining Candidate: 20
Guessing: bison 🟨⬜️🟨⬜️⬜️ Remaining Candidate: 2
Guessing: abuse 🟩️🟩️⬜️🟩️🟩️ Remaining Candidate: 1
Guessing: abase 🟩️🟩️🟩️🟩️🟩️ Actual word: abase
```

- Also, if you want to use this solver to play against an actual game you can run the `rewordle.py` and follow the instructions on the prompt. While writing the response follow the following pattern:
```
🟩️⬜️🟨⬜️⬜️ -> gbybb
```

*Disclaimer: There are lots of scope to optimize the solving part and minimize redundant calculations. Any contribution is welcome.*
