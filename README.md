# WORDLE Solver Testbed

Testbed to automate the solving of WORDLE puzzles.

GPT4 LLM is used to solve the puzzles.  Currently manual access to GPT4 via the OpenAI Playground Chat.  Using these parameters:
* temperature=0.1
* max_tokens=4096

## Core Modules
### `src/lll_solver.py`  

Used to test LLM with local WordleJudge Simulator.  Depends on OpenAI GPT4 model via the OpenAI Playground Chat.

#### Sample run manually
```
$ python src/llm_solver.py apple
Word: apple, API: False

Attempt 1 guess is adieu
The result is {'present': [(3, 'e')], 'correct': [(0, 'a')], 'absent': ['d', 'i', 'u']}
global_state: {'present': {(3, 'e')}, 'correct': {(0, 'a')}, 'absent': {'i', 'u', 'd'}}
before_size: 15920, after_size: 476

Copy and paste the following prompt to OpenAI Playground and enter the recommendation
Enter a word: astor

Attempt 2 guess is astor
The result is {'present': [], 'correct': [(0, 'a')], 'absent': ['s', 't', 'o', 'r']}
global_state: {'present': {(3, 'e')}, 'correct': {(0, 'a')}, 'absent': {'i', 'r', 't', 's', 'o', 'd', 'u'}}
before_size: 476, after_size: 101

Copy and paste the following prompt to OpenAI Playground and enter the recommendation
Enter a word: awake

Attempt 3 guess is awake
The result is {'present': [(2, 'a')], 'correct': [(0, 'a'), (4, 'e')], 'absent': ['w', 'k']}
global_state: {'present': {(3, 'e'), (2, 'a')}, 'correct': {(0, 'a'), (4, 'e')}, 'absent': {'k', 'i', 'r', 't', 'w', 's', 'o', 'd', 'u'}}
before_size: 101, after_size: 13

Copy and paste the following prompt to OpenAI Playground and enter the recommendation
Enter a word: apple

Attempt 4 guess is apple
The result is True
global_state: {'present': {(3, 'e'), (2, 'a')}, 'correct': {(0, 'a'), (4, 'e')}, 'absent': {'k', 'i', 'r', 't', 'w', 's', 'o', 'd', 'u'}}
vscode ➜ /workspaces/wordle_solver (main) $ 
```

#### Sample run with LLM
```
$ python src/llm_solver.py apple --api True
Word: apple, API: True

Attempt 1 guess is adieu
The result is {'present': [(3, 'e')], 'correct': [(0, 'a')], 'absent': ['d', 'i', 'u']}
global_state: {'present': {(3, 'e')}, 'correct': {(0, 'a')}, 'absent': {'d', 'u', 'i'}}
before_size: 15920, after_size: 476

Attempt 2 guess is actor
The result is {'present': [], 'correct': [(0, 'a')], 'absent': ['c', 't', 'o', 'r']}
global_state: {'present': {(3, 'e')}, 'correct': {(0, 'a')}, 'absent': {'c', 'd', 'r', 'i', 't', 'u', 'o'}}
before_size: 476, after_size: 137

Attempt 3 guess is apple
The result is True
global_state: {'present': {(3, 'e')}, 'correct': {(0, 'a')}, 'absent': {'c', 'd', 'r', 'i', 't', 'u', 'o'}}
```

#### Example Prompt for LLM
``` 
Solve the puzzle by guessing a five-letter word using these clues.
Words must contain these letters in the following positions: 'a' in the first.
Words must contain these letters with the position restrictions:  'e' should not be in the fourth position.
Words that do not contain these letters:  'c',  'd',  'r',  'i',  't',  'u',  'o'.
If more than one word meets the criteria, select the word that is more common. Provide step-by-step instructions for how you arrived at the selected word. When writing the instructions, do not list words. Return only a json structure with the key 'recommendation' for the recommended word and 'explanation' for your explantion.
List of candidate words:
avena
apple
amass
abase
amang
alans
abamp
alvan
amaas
awane
ambas
amman
algal
ameba
anana
avell
allan
aheap
apeak
aveny
azans
asaph
awave
asana
ankle
```

### `src/llm_solver_nyt.py`

Used to play Wordle on the NYT website.  Depends on OpenAI GPT4 model via the OpenAI Playground Chat.

#### Current Limiations
* Requires manual interaction with the NYT website.
* Requires manual interaction with the OpenAI Playground Chat.
* Sometimes the recommended word is not part of the NYT word list.  Manual work-around is to view the last generated prmopt file and select a word from the list.

### `src/random_solver.py`

Used to test Random Solver with local WordleJudge Simulator.

### `src/wordle_judge.py` 

The provided Python code defines a class `WordleJudge` that is used to judge the guesses in a word guessing game, similar to the game Wordle on NYT.

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

#### `WordListGeneratorLLM`

The `WordListGeneratorLLM` class is a subclass of `WordListGeneratorBase` that generates a list of candidate words for the Wordle game using a Language Model (LLM). It overrides several methods to generate prompts for the LLM based on the current state of the game.

The class has the following methods:

1. `_generate_position_text(position)`: This static method takes a position (an integer) as input and returns a string representing the ordinal form of the position (e.g., "first", "second", etc.).

2. `generate_correct_letter_prompt()`: This method generates a prompt for the user based on the correct letters and their positions. It constructs a string that lists the correct letters and their positions in the word. If there are no correct letters, an empty string is returned.

3. `generate_present_letter_prompt()`: This method generates a prompt for the user based on the present letters and their positions. It constructs a string that lists the present letters and their positions in the word. If there are no present letters, an empty string is returned.

4. `generate_absent_letter_prompt()`: This method generates a prompt for the user based on the absent letters. It constructs a string that lists the absent letters. If there are no absent letters, an empty string is returned.

5. `generate_llm_prompt()`: This method generates a prompt for the LLM based on the current state of the game. It first updates the candidate_words list. If the list is empty, it returns None. Otherwise, it generates prompts for correct, absent, and present letters. It then constructs a list of candidate words. If the list is too long, it randomly samples a subset of the words. The prompts and the list of candidate words are written to a file.

#### `OpenAIInterace`

Class `OpenAIInterface` provides an interface with the OpenAI API. 

The class has two attributes:
1. `api_key_file`: The location of a JSON file containing the API key.
2. `model`: The specific model to use, defaulting to "gpt-4".

The class has two methods:
1. `__init__(self, api_key_file, model="gpt-4")`: This is the constructor method that initializes the `OpenAIInterface` with the API key and the model. It reads the API key from the provided JSON file and initializes an `OpenAI` client with the API key. It also sets the model to use.

2. `chat(self, prompt)`: This method invokes the chat API with a given prompt and returns the contents to the caller. It creates a chat completion with the model, a system message saying "You are a helpful assistant to solve the Wordle puzzle.", and a user message containing the provided prompt. It sets the temperature to 0.1, the maximum number of tokens to 4096, the top_p to 1, and both the frequency penalty and presence penalty to 0. It then returns the content of the first choice from the response.