# WORDLE Solver Virtual Assistant (WSVA) Testbed

Testbed to automate the solving of WORDLE puzzles.

The list of 5-letter words used in the Wordle Solver Virual Assistant is sourced from https://github.com/dwyl/english-words.  The file `data/five-letter-words.txt` is an extract of only five-letter words from the file `words_alpha.txt` in the `english-words` GitHub repository.

Answers to past Wordle puzzles sourced from https://www.rockpapershotgun.com/wordle-past-answers, as of 27Jan2024.

GPT4 LLM is used to solve the puzzles.  Currently manual access to GPT4 via the OpenAI Playground Chat and API access is supported.  Using these parameters:
* temperature=0.1
* max_tokens=4096

## Core Modules

### `src/llm_solver.py`  

Used to test LLM with local WordleJudge Simulator.  Depends on OpenAI GPT4 model via the OpenAI Playground Chat or API.

This Python script is a command-line interface for playing the Wordle game using a Language Model (LLM) to generate guesses. Here's a breakdown of what the script does:

1. **Imports necessary modules**: The script imports several Python standard library modules (`argparse`, `json`, `random`) and two custom modules (`WordListGeneratorLLM`, `OpenAIInterface`, `WordleJudge`).

2. **Defines a list of candidate first words**: The `CANIDATE_FIRST_WORD_LIST` is a list of words that the script can use as the first guess in the Wordle game.

3. **Defines the `main` function**: This function is the main entry point of the script.

   - It first parses command-line arguments using the `argparse` module. The script accepts one required argument `word`, which is the target word for the Wordle game, and one optional argument `--api`, which is a boolean flag indicating whether to use the OpenAI API to generate guesses.

   - It then creates a `WordleJudge` object, a `WordListGeneratorLLM` object, and an `OpenAIInterface` object. The `WordleJudge` object is used to judge the guesses, the `WordListGeneratorLLM` object is used to generate a list of candidate words for the Wordle game, and the `OpenAIInterface` object is used to interact with the OpenAI API.

   - The script then enters a loop where it makes up to 20 attempts to guess the Wordle word. For each attempt, it first selects a word from the candidate word list and then asks the WordleJudge to judge the guess. The WordleJudge returns a string of feedback characters where "g" means the letter is correct and in the correct position, "y" means the letter is correct but in the wrong position, and "." means the letter is not in the word.

   - The script then updates the state of the `WordListGeneratorLLM` object based on the Wordle response and generates a new prompt for the LLM. If the `--api` flag is set, it sends the prompt to the OpenAI API and uses the recommended word from the API response as the next guess. If the `--api` flag is not set, it asks the user to manually enter the next guess.

   - The loop continues until the script has made 20 attempts or there are no more candidate words left.

4. **Runs the `main` function**: If the script is run as a standalone program (i.e., not imported as a module), it calls the `main` function to start the Wordle game.

This script provides a way to play the Wordle game using a Language Model to generate guesses, with the option to use the OpenAI API to generate the guesses. It also provides a way for the user to manually enter guesses and Wordle responses.

#### Sample run with copy/paste of prompt to OpenAI Playground
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

#### Sample run using the OpenAI Chat API to automatically send the prompt and receive the recommendation
```
$ python src/llm_solver.py apple --api
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

If more than one word meets the criteria, select the word that is more common. Provide step-by-step instructions for how you arrived at the selected word. When writing the instructions, do not list words. Return only a json structure with the key 'recommendation' for the recommended word and 'explanation' for your explantion.
List of candidate words:
bitty
ditty
kilty
kitty
milty
mitty
witty
```

#### Response from LLM
```json
{
   "recommendation": "kitty", 
   "explanation": "The word 'kitty' is selected because it is a common English word and it meets the criteria of being a five-letter word. Other words in the list may not be as commonly used or recognized in English."
}
```

#### Sample run using ChatGPT interface by uploading the prompt file
Instead of using OpenAI Playground, loaded the prompt file into ChatGPT. ChatGPT took longer.  Most likely cause is "creative flexibility" in the ChatGPT service.
```
 $ python src/llm_solver.py apple
Word: apple, API: False

Attempt 1 guess is adieu
The result is {'present': [(3, 'e')], 'correct': [(0, 'a')], 'absent': ['d', 'i', 'u']}
global_state: {'present': {(3, 'e')}, 'correct': {(0, 'a')}, 'absent': {'i', 'u', 'd'}}
before_size: 15920, after_size: 476

Copy and paste the prompt file to OpenAI Playground and enter the recommendation
Enter a word: aroph

Attempt 2 guess is aroph
The result is {'present': [(3, 'p')], 'correct': [(0, 'a')], 'absent': ['r', 'o', 'h']}
global_state: {'present': {(3, 'e'), (3, 'p')}, 'correct': {(0, 'a')}, 'absent': {'i', 'o', 'u', 'h', 'r', 'd'}}
before_size: 476, after_size: 186

Copy and paste the prompt file to OpenAI Playground and enter the recommendation
Enter a word: ajaja

Attempt 3 guess is ajaja
The result is {'present': [(2, 'a'), (4, 'a')], 'correct': [(0, 'a')], 'absent': ['j', 'j']}
global_state: {'present': {(3, 'e'), (4, 'a'), (2, 'a'), (3, 'p')}, 'correct': {(0, 'a')}, 'absent': {'j', 'i', 'o', 'u', 'h', 'r', 'd'}}
before_size: 186, after_size: 106

Copy and paste the prompt file to OpenAI Playground and enter the recommendation
Enter a word: angle

Attempt 4 guess is angle
The result is {'present': [], 'correct': [(0, 'a'), (3, 'l'), (4, 'e')], 'absent': ['n', 'g']}
global_state: {'present': {(3, 'e'), (4, 'a'), (2, 'a'), (3, 'p')}, 'correct': {(0, 'a'), (3, 'l'), (4, 'e')}, 'absent': {'j', 'i', 'o', 'u', 'g', 'h', 'r', 'n', 'd'}}
before_size: 106, after_size: 6

Copy and paste the prompt file to OpenAI Playground and enter the recommendation
Enter a word: abele

Attempt 5 guess is abele
The result is {'present': [(2, 'e')], 'correct': [(0, 'a'), (3, 'l'), (4, 'e')], 'absent': ['b']}
global_state: {'present': {(3, 'e'), (3, 'p'), (4, 'a'), (2, 'a'), (2, 'e')}, 'correct': {(0, 'a'), (3, 'l'), (4, 'e')}, 'absent': {'j', 'i', 'o', 'u', 'g', 'h', 'b', 'r', 'n', 'd'}}
before_size: 6, after_size: 4

Copy and paste the prompt file to OpenAI Playground and enter the recommendation
Enter a word: ample

Attempt 6 guess is ample
The result is {'present': [], 'correct': [(0, 'a'), (2, 'p'), (3, 'l'), (4, 'e')], 'absent': ['m']}
global_state: {'present': {(3, 'e'), (3, 'p'), (4, 'a'), (2, 'a'), (2, 'e')}, 'correct': {(0, 'a'), (3, 'l'), (2, 'p'), (4, 'e')}, 'absent': {'j', 'i', 'o', 'u', 'g', 'h', 'b', 'r', 'n', 'd', 'm'}}
before_size: 4, after_size: 1

Copy and paste the prompt file to OpenAI Playground and enter the recommendation
Enter a word: apple

>>>>Exceed wordle game limit: attempt 7 guess is apple
The result is True
global_state: {'present': {(3, 'e'), (3, 'p'), (4, 'a'), (2, 'a'), (2, 'e')}, 'correct': {(0, 'a'), (3, 'l'), (2, 'p'), (4, 'e')}, 'absent': {'j', 'i', 'o', 'u', 'g', 'h', 'b', 'r', 'n', 'd', 'm'}}
```


### `src/llm_solver_nyt.py`

This Python script is a command-line interface for playing the Wordle game using a Language Model (LLM) to generate guesses. Here's a breakdown of what the script does:

1. **Imports necessary modules**: The script imports several Python standard library modules (`argparse`, `json`, `random`, `sys`) and two custom modules (`WordListGeneratorLLM`, `OpenAIInterface`).

2. **Defines a list of candidate first words**: The `CANIDATE_FIRST_WORD_LIST` is a list of words that the script can use as the first guess in the Wordle game.

3. **Defines the `main` function**: This function is the main entry point of the script.

   - It first parses command-line arguments using the `argparse` module. The script accepts one optional argument `--api`, which is a boolean flag indicating whether to use the OpenAI API to generate guesses.

   - It then creates a `WordListGeneratorLLM` object and an `OpenAIInterface` object. The `WordListGeneratorLLM` object is used to generate a list of candidate words for the Wordle game, and the `OpenAIInterface` object is used to interact with the OpenAI API.

   - The script then enters a loop where it makes up to 7 attempts to guess the Wordle word. For each attempt, it first selects a word from the candidate word list and then asks the user to enter the Wordle response for that word. The Wordle response is a string of feedback characters where "g" means the letter is correct and in the correct position, "y" means the letter is correct but in the wrong position, and "." means the letter is not in the word.

   - The script then updates the state of the `WordListGeneratorLLM` object based on the Wordle response and generates a new prompt for the LLM. If the `--api` flag is set, it sends the prompt to the OpenAI API and uses the recommended word from the API response as the next guess. If the `--api` flag is not set, it asks the user to manually enter the next guess.

   - The loop continues until the script has made 7 attempts or there are no more candidate words left.

4. **Runs the `main` function**: If the script is run as a standalone program (i.e., not imported as a module), it calls the `main` function to start the Wordle game.

This script provides a way to play the Wordle game using a Language Model to generate guesses, with the option to use the OpenAI API to generate the guesses. It also provides a way for the user to manually enter guesses and Wordle responses.

#### Enter guess:
The user can either accept the recommended word or type in an alterative word.

If the user wants to use the recommened word, they should enter "y" and press the Enter key to this prompt "Use recommended word 'xxxxx'? (y/n)", where "xxxxx" is the recommended word. 

If the want to use an alternative word, they should enter "n" and press the Enter key.  If they enter "n", they'll be prompted to enter the alternative word: "What word should be used?: ".  After entering the alternative word, they'll be prompted to confirm the alternative word is correct: "Is this correct: 'wwwww'? (y/n)", where "wwwww" is the alternative word.  If it is correct, enter "y" and press the Enter key.  If it is not correct, enter "n" and press the Enter key.  If you enter "n", you'll be prompted to re-enter the alternative word.

The enter the results from the NYT website for a guess, the user will be provided this input prompt:

#### Enter wordle response:
When prompted with "Enter wordle response: ", you should enter a 5-letter feedback from Wordle.

Enter "g" for any letter that is correct and in the correct position.

Enter "y" for any letter that is correct but not in the correct position.

Enter a period (.) for a letter that is not in the word.

After entering the five letter response pattern, press the Enter key.  You'll be prompted to confirm the correct response pattern was entered.  If it is correct, enter "y" and press the Enter key.  If it is not correct, enter "n" and press the Enter key.  If you enter "n", you'll be prompted to re-enter the response pattern.

Here are some example responses:

If the correct word is "apple" and you have guessed "apply", you would enter "gggg." (without the quotes) because the first four letters are in the correct position and the last letter 'y' is not in the word.

If the correct word is "apple" and you have guessed "pepla", you would enter "yyygy" (without the quotes) because the first three letters and fifth letter are in the word but in the wrong postion.  The fourth letter is in the correct position.

For example, if the correct word is "apple" and you have guessed "fable", you would enter ".y.gg" (without the quotes) because 'f' and 'b' are not in "apple" and 'l' and 'e' are in the correct postion and 'a' is in the word but in the wrong position.

#### Example run
```text
$ python src/llm_solver_nyt.py  --api
API: True

attempt 1 word is trace
Enter wordle response: ..g.g
Is this correct: '..g.g'? (y/n)y
The result is {'correct': [(2, 'a'), (4, 'e')], 'present': [], 'absent': ['t', 'r', 'c']}
global_state: {'present': set(), 'correct': {(4, 'e'), (2, 'a')}, 'absent': {'c', 'r', 't'}}
before_size: 15920, after_size: 108
WSVA recommendation: 'blame' from list:
abase
abaze
avale
blame
djave
emane
flake
glave
glaze
heave
image
leave
osage
phage
plage
shake
shave
slade
slane
smaze
spave
suave
swage
ukase
weave

Use recommended word 'blame'? (y/n)y

attempt 2 word is blame
Enter wordle response: ..g.g
Is this correct: '..g.g'? (y/n)y
The result is {'correct': [(2, 'a'), (4, 'e')], 'present': [], 'absent': ['b', 'l', 'm']}
global_state: {'present': set(), 'correct': {(4, 'e'), (2, 'a')}, 'absent': {'l', 'b', 't', 'c', 'm', 'r'}}
before_size: 108, after_size: 61
WSVA recommendation: 'spade' from list:
adage
adawe
deave
diane
duane
faade
goave
heave
huave
keawe
knape
oxane
peage
phage
phane
quave
shane
shave
soave
spade
spake
spave
suave
vyase
weave

Use recommended word 'spade'? (y/n)y

attempt 3 word is spade
Enter wordle response: g.g.g
Is this correct: 'g.g.g'? (y/n)y
The result is {'correct': [(0, 's'), (2, 'a'), (4, 'e')], 'present': [], 'absent': ['p', 'd']}
global_state: {'present': set(), 'correct': {(4, 'e'), (0, 's'), (2, 'a')}, 'absent': {'p', 'l', 'b', 't', 'c', 'm', 'r', 'd'}}
before_size: 61, after_size: 8
WSVA recommendation: 'shake' from list:
seave
shake
shane
shave
snake
soave
suave
swage

Use recommended word 'shake'? (y/n)y

attempt 4 word is shake
Enter wordle response: g.ggg
Is this correct: 'g.ggg'? (y/n)y
The result is {'correct': [(0, 's'), (2, 'a'), (3, 'k'), (4, 'e')], 'present': [], 'absent': ['h']}
global_state: {'present': set(), 'correct': {(3, 'k'), (4, 'e'), (0, 's'), (2, 'a')}, 'absent': {'p', 'l', 'b', 't', 'c', 'm', 'h', 'r', 'd'}}
before_size: 8, after_size: 1
WSVA recommendation: 'snake' from list:
snake

Use recommended word 'snake'? (y/n)y

attempt 5 word is snake
Enter wordle response: ggggg
Is this correct: 'ggggg'? (y/n)y

>>>>Success wordle game, correctly guessed snake in 5 attempts
global_state: {'present': set(), 'correct': {(3, 'k'), (4, 'e'), (0, 's'), (2, 'a')}, 'absent': {'p', 'l', 'b', 't', 'c', 'm', 'h', 'r', 'd'}}
```


#### Current Limiations
* Requires manual interaction with the NYT website.
* Requires manual interaction with the OpenAI Playground Chat if not using the `--api` option.
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

The selected class is `WordListGeneratorBase` in Python. It's a base class used to generate a list of candidate words for the Wordle game. Here's a breakdown of its methods and attributes:

**Attributes:**

- `words_fp`: The file path to the file containing the words.
- `candidate_words`: A list of candidate words for the Wordle game.
- `global_state`: A dictionary that stores the current state of the Wordle game. It includes "present", "correct", and "absent" letters and their positions.
- `dump_file_count`: The number of times the `candidate_words` list has been dumped to a file.

**Methods:**

- `__init__(self, words_fp)`: Initializes the class with a file path to load words from.

- `is_letter_in_present(self, letter)`: Checks if a letter is in the "present" list.

- `is_letter_in_correct(self, letter)`: Checks if a letter is in the "correct" list.

- `load(self)`: Loads words from a file into the `candidate_words` list.

- `_eliminate_words_with_absent_letters(self)`: Eliminates words from the `candidate_words` list that contain any of the "absent" letters.

- `_keep_words_with_correct_letters(self)`: Retains only those words in the `candidate_words` list that have "correct" letters in the correct positions.

- `_eliminate_words_with_present_letters(self)`: Eliminates words from the `candidate_words` list that have any of the "present" letters in the correct positions.

- `update_state(self, result)`: Updates the `global_state` dictionary with the new result.

- `print_state(self)`: Prints the current `global_state`.

- `update_candidate_words(self, dump_candidates=False)`: Updates the `candidate_words` list based on the current `global_state`. If `dump_candidates` is `True`, the updated `candidate_words` list is written to a file.

This class provides a base functionality for generating and updating a list of candidate words based on the current game state. It can be extended by other classes to provide different strategies for generating candidate words.

#### `WordListGeneratorRandom` 

The selected class is `WordListGeneratorRandom` in Python. It's a class used to generate a list of candidate words for the Wordle game. This class inherits from the `WordListGeneratorBase` class and overrides the `get_candidate_word` method to return a random word from the `candidate_words` list.

Here's a breakdown of its attributes and methods:

**Attributes:**

- `candidate_words (list)`: A list of candidate words for the Wordle game. This list is updated based on the current game state and is used to select the next word to guess in the game.

- `global_state (dict)`: A dictionary that stores the current state of the Wordle game. This state includes information about the letters that are present, correct, and absent in the current word.

- `words_fp (str)`: The file path to the file containing the words. This file is used to load the initial list of candidate words.

- `dump_file_count (int)`: The number of times the `candidate_words` list has been dumped to a file. This is used for debugging and analysis purposes.

**Methods:**

- `get_candidate_word(self, dump_candidates=False)`: This method first updates the `candidate_words` list based on the current `global_state`. If the list is empty after the update, it returns `None`. Otherwise, it returns a random word from the list. If `dump_candidates` is `True`, the updated `candidate_words` list is written to a file. This method provides the main functionality of the class, which is to select the next word to guess in the Wordle game.

This class provides a strategy for generating and updating a list of candidate words based on the current game state. It randomly selects a word from the list of candidate words, providing a simple and random strategy for guessing the next word in the Wordle game.

#### `WordListGeneratorLLM`

The selected class is `WordListGeneratorLLM` in Python. It's a class used to generate a list of candidate words for the Wordle game using a Language Model (LLM). Here's a breakdown of its methods and attributes:

**Attributes:**

- `MAX_SIZE (int)`: The maximum size of the candidate_words list.
- `candidate_words (list)`: A list of candidate words for the Wordle game.
- `global_state (dict)`: A dictionary that stores the current state of the Wordle game.
- `words_fp (str)`: The file path to the file containing the words.
- `dump_file_count (int)`: The number of times the candidate_words list has been dumped to a file.

**Methods:**

- `_generate_position_text(position)`: A static method that returns a string representation of a given position.

- `generate_llm_prompt()`: This method first updates the candidate_words list. If the list is empty, it returns None. Otherwise, it generates prompts for correct, absent, and present letters. It then constructs a list of candidate words. If the list is too long, it randomly samples a subset of the words. The prompts and the list of candidate words are written to a file.

Example prompt:
```
Solve the puzzle by guessing a five-letter word using these clues.

If more than one word meets the criteria, select the word that is more common. Provide step-by-step instructions for how you arrived at the selected word. When writing the instructions, do not list words. Return only a json structure with the key 'recommendation' for the recommended word and 'explanation' for your explantion.
List of candidate words:
benjy
bensh
fease
feaze
fezzy
gease
gnash
heave
henge
hewgh
kebby
kesse
knave
njave
seave
seavy
sense
shaky
skaff
snash
swash
weave
webby
whase
yezzy
```

Example JSON output
```
{
   "recommendation": "weave", 
   "explanation": "The word 'weave' is selected because it is a common English word and it meets the criteria of being a five-letter word. Other words in the list may not be as commonly used or recognized in English."
}
```

This class provides a strategy for generating and updating a list of candidate words based on the current game state using a Language Model (LLM). It can be used as part of a larger system that includes other classes like `WordListGeneratorRandom`, which generates candidate words randomly.

#### `OpenAIInterace`

Class `OpenAIInterface` provides an interface with the OpenAI API. 

The class has two attributes:
1. `api_key_file`: The location of a JSON file containing the API key.
2. `model`: The specific model to use, defaulting to "gpt-4".

The class has two methods:
1. `__init__(self, api_key_file, model="gpt-4")`: This is the constructor method that initializes the `OpenAIInterface` with the API key and the model. It reads the API key from the provided JSON file and initializes an `OpenAI` client with the API key. It also sets the model to use.

2. `chat(self, prompt)`: This method invokes the chat API with a given prompt and returns the contents to the caller. It creates a chat completion with the model, a system message saying "You are a helpful assistant to solve the Wordle puzzle.", and a user message containing the provided prompt. It sets the temperature to 0.1, the maximum number of tokens to 4096, the top_p to 1, and both the frequency penalty and presence penalty to 0. It then returns the content of the first choice from the response.

## Observations:

### Hallucination
Example of LLM hallucinating on the explanation.  

**Prompt**:
``` 
Solve the puzzle by guessing a five-letter word using these clues.

If more than one word meets the criteria, select the word that is more common. Provide step-by-step instructions for how you arrived at the selected word. When writing the instructions, do not list words. Return only a json structure with the key 'recommendation' for the recommended word and 'explanation' for your explantion.
List of candidate words:
biddy
butin
didus
dungs
filly
flogs
flook
gibby
gully
gusty
hondo
immun
josip
jotty
judos
lusts
mommy
nobut
nould
numud
shots
sifts
sugis
undid
uninn
```

**LLM Response**:

```json
{
   "recommendation": "gusty", 
   "explanation": "The first step is to eliminate words that have repeating letters, as Wordle only uses words with unique letters. This eliminates 'biddy', 'didus', 'filly', 'flogs', 'gibby', 'mommy', 'nobut', 'nould', 'numud', 'shots', 'sifts', 'sugis', and 'undid'. The next step is to eliminate words that contain less common letters, such as 'j', 'z', 'x', 'q', and 'v'. This eliminates 'josip' and 'jotty'. The remaining words are 'butin', 'dungs', 'flook', 'gully', 'gusty', 'hondo', 'judos', 'lusts', and 'uninn'. Among these, 'gusty' is the most common word, making it the best guess."
}
```
Repeated letters are allowed in Wordle.


### Inconsistent LLM explanations

```json
{
   "recommendation": "shake", 
   "explanation": "The first step is to eliminate words that have uncommon letters or combinations. 'Seave', 'soave', 'suave', and 'swage' are eliminated because 'ea', 'oa', 'ua', and 'wa' are less common in English words. 'Shane' and 'snake' are eliminated because 'ane' and 'ake' are less common endings than 'ake'. This leaves 'shake' and 'shave'. 'Shake' is chosen because it is a more common word than 'shave'."
}
```

The reason for eliminating 'ake' is inconsistent.

### Over-prompting


```text
Solve the puzzle by guessing a five-letter word using these clues.
Remove words from consideration that contain these letters:  'c',  'u',  'h',  'n',  's',  'd',  
'i',  'p',  'l',  't'.
Words must contain these letters in the following positions: 'e' in the second, 'a' in the fifth.
Words must contain these letters with the position restrictions:  'a' must not be in the first position,  
'e' must not be in the third position,  'r' must not be in the third position,  
'a' must not be in the third position,  'e' must not be in the fourth position.
If more than one word meets the criteria, select the word that is more common. Provide step-by-step 
instructions for how you arrived at the selected word. When writing the instructions, do not list words. 
Return only a json structure with the key 'recommendation' for the recommended word and 'explanation' 
for your explantion.
List of candidate words:
bemba
gemma
regga
regma
zebra
```

These instructions were already taken care of by regex filtering of the source word list.
```text
Remove words from consideration that contain these letters:  'c',  'u',  'h',  'n',  's',  'd',  
'i',  'p',  'l',  't'.
Words must contain these letters in the following positions: 'e' in the second, 'a' in the fifth.
Words must contain these letters with the position restrictions:  'a' must not be in the first position,  
'e' must not be in the third position,  'r' must not be in the third position,  
'a' must not be in the third position,  'e' must not be in the fourth position.
```

Afer removing the extraneous instructions the quality of recommended word appears to be improved.  More testing is needed to quantify this, e.g., compared to random guessing.

