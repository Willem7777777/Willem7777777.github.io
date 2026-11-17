# Java

Two programming assignments from the first-year Java course at TU Delft. Both are console games.

- `SwansDucksgame3.java`: a Bulls-and-Cows style guessing game. The program draws a random 4-digit number with all different digits (a helper method `hasDupes` checks the digits one by one), validates every guess, and reports how many digits are in the right place (Swans) and in the wrong place (Ducks).
- `Speedrun.java`: a two-player dice game where the first to reach 100 points wins. A nested `Player` class keeps the score and decides what happens in a turn: roll, add to the turn total, ask whether to continue (`Y`/`N`), and stop when the turn total would reach 100. Written together with a study partner; the comments explain the turn logic.

Run with `javac Speedrun.java && java Speedrun`.

## What I learned

- **Control flow.** `while` and `do-while` loops for game rounds, and loops that keep asking until the input is valid.
- **Reading input safely.** Using `Scanner` and checking the answer before using it, so a wrong key does not break the game.
- **Randomness.** Generating random numbers with `Random`, including how to draw a number that must have unique digits.
- **Structuring code.** Splitting behaviour into methods and a small class with its own state (the player's score) instead of one long `main`.
- **Working with someone else's code.** Explaining the logic in comments so my study partner and I could both follow and change it.
