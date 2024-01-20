# WORDLE Solver Testbed

Testbed to automate the solving of WORDLE puzzles.

## contents
### `src/main.py`  

main program to test the solver

### `src/wordle_judge.py` 

The provided Python code defines a class `WordleJudge` that is used to judge the guesses in a word guessing game, similar to the game Wordle.

The `WordleJudge` class has two methods: `__init__` and `judge_guess`.

The `__init__` method is the constructor of the class. It takes one argument, `correct_word`, which is the word that the player is trying to guess. The `correct_word` is converted to lowercase and stored as an instance variable.

The `judge_guess` method is used to judge a player's guess. It takes one argument, `guess`, which is the word that the player has guessed. The `guess` is converted to lowercase for comparison.

If the `guess` is equal to the `correct_word`, the method returns `True`, indicating that the player has guessed the word correctly.

If the `guess` is not equal to the `correct_word`, the method creates a `result` dictionary with three keys: "present", "correct", and "absent". Each key maps to a list that will contain the letters that are present in the `correct_word` but in the wrong position, present and in the correct position, or not present at all, respectively.

The method then iterates over each letter in the `guess` using the `enumerate` function, which provides the index of the letter as well as the letter itself. If the letter is the same as the letter in the `correct_word` at the same position, it is added to the "correct" list in the `result` dictionary. If the letter is in the `correct_word` but not at the same position, it is added to the "present" list, unless it has already been added. If the letter is not in the `correct_word` at all, it is added to the "absent" list.

Finally, the `result` dictionary is returned, providing feedback on the player's guess.

The `if __name__ == "__main__":` block at the end of the script is used to provide an example of how to use the `WordleJudge` class. A `WordleJudge` object is created with the correct word "apple", a guess of "alloy" is judged, and the result is printed to the console.

### `src/wordle_solver.py` 

Class for solvers.  Currently only has a brute force solver is implemented.

This Python script defines two classes: `WordListGeneratorBase` and `WordListGeneratorRandom`. 

#### `WordListGeneratorBase` 
An abstract base class that provides a common interface and some shared functionality for generating a list of candidate words in a word guessing game. 

The `__init__` method initializes the object with a file path to a list of words and sets up some initial state. The `load` method reads the words from the file and stores them in the `candidate_words` list. 

The `_eliminate_words_with_letters` method filters out words that contain any letters in the "absent" set of the global state. It does this by creating a regular expression that matches any of the absent letters and then using a list comprehension to create a new list of words that do not match this regular expression.

The `_generate_regex_for_correct` method generates a regular expression that matches words with the correct letters in the correct positions. It does this by creating a list of "." characters, replacing the ones at the positions of the correct letters with those letters, and then joining the list into a string and adding "^" and "$" to the start and end to match the start and end of the string.

The `update_state` method updates the global state with the result of a guess. It does this by iterating over the keys in the result and updating the corresponding sets in the global state.

The `get_candidate_words` method is an abstract method, meaning it must be implemented by any subclass of `WordListGeneratorBase`.


#### `WordListGeneratorRandom` 
This class overrides the `get_candidate_words` method from the base class. This method is responsible for updating the list of candidate words based on the game's current state and returning a random word from the updated list.

At the start of the method, the size of the current list of candidate words is stored in the `before_size` variable. Then, the `_eliminate_words_with_letters` method is called to remove any words from the list that contain letters known to be absent from the target word. This updated list is stored back in `self.candidate_words`.

Next, the `_generate_regex_for_correct` method is called to generate a regular expression that matches words with the correct letters in the correct positions. This regular expression is used to further filter the list of candidate words, keeping only those words that match the regular expression.

After the list of candidate words has been updated, the size of the list is stored in the `after_size` variable. The sizes before and after the update are printed to the console for debugging purposes.

Finally, if the list of candidate words is empty, the method returns `None`. Otherwise, it returns a random word from the list. This is done using the `random.choice` function from the Python standard library.

The `_eliminate_words_with_letters` and `_generate_regex_for_correct` methods are defined in the `WordListGeneratorBase` class. The `_eliminate_words_with_letters` method creates a regular expression that matches any of the absent letters and uses it to filter out words from the list of candidate words. The `_generate_regex_for_correct` method creates a regular expression that matches words with the correct letters in the correct positions.

