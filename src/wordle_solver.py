
import json
import os
import random
import re
import pprint

from openai import OpenAI

pp = pprint.PrettyPrinter(indent=4)

class WordListGeneratorBase:
    """
    A base class used to generate a list of candidate words for the Wordle game.

    This class provides methods to load words from a file, update the game state, and update the 
    candidate_words list based on the current game state. The game state includes present, correct, 
    and absent letters and their positions.

    Attributes:
        words_fp (str): The file path to the file containing the words.
        candidate_words (list): A list of candidate words for the Wordle game.
        global_state (dict): A dictionary that stores the current state of the Wordle game.
        dump_file_count (int): The number of times the candidate_words list has been dumped to a file.
    """

    def __init__(self, words_fp):
        self.words_fp = words_fp
        self.candidate_words = []
        self.global_state = {
            "present": set(),
            "correct": set(),
            "absent": set()
        }
        self.dump_file_count = 0

    def is_letter_in_present(self, letter):
        """
        Checks if a letter is in the present list.

        Args:
            letter (str): The letter to check.

        Returns:
            bool: True if the letter is in the present list, False otherwise.
        """
        return letter in [x[1] for x in self.global_state["present"]]
    
    def is_letter_in_correct(self, letter):
        """
        Checks if a letter is in the correct list.

        Args:
            letter (str): The letter to check.

        Returns:
            bool: True if the letter is in the correct list, False otherwise.
        """
        return letter in [x[1] for x in self.global_state["correct"]]

    def load(self):
        """
        Load words from a file into the candidate_words list.

        The file should contain one word per line. The path to the file is stored in the `words_fp` 
        attribute of the class instance. 
        The words are stripped of leading and trailing whitespace before being added to the list.
        """
        with open(self.words_fp, 'r') as file:
            self.candidate_words = [line.strip() for line in file]
    
    def _eliminate_words_with_absent_letters(self):
        """
        Eliminate words from the candidate_words list that contain any of the absent letters.

        This method constructs a regular expression from the absent letters stored in the global_state dictionary and uses it to filter out any words in the candidate_words list that contain any of these letters.
        """
        letter_regex = '[' + ''.join(self.global_state["absent"]) + ']'
        self.candidate_words = [word for word in self.candidate_words if not re.search(letter_regex, word)]

    def _keep_words_with_correct_letters(self):
        """
        Retains only those words in the candidate_words list that have correct letters in the correct positions.

        This method constructs a regular expression pattern from the correct letters and their positions stored in the global_state dictionary. The pattern is then used to filter the candidate_words list, keeping only 
        those words that match the pattern.
        """
        word_pattern = ["." for _ in range(5)]
        for position, letter in self.global_state["correct"]:
            word_pattern[position] = letter
        regex = "^" + ''.join(word_pattern) + "$"
        correct_regex = re.compile(regex)
        self.candidate_words = [word for word in self.candidate_words if correct_regex.match(word)]
        
    def _eliminate_words_with_present_letters(self):
        """
        Eliminates words from the candidate_words list that have any of the present letters in the correct positions.

        This method constructs a regular expression pattern from the present letters and their positions stored in the global_state dictionary. The pattern is then used to filter the candidate_words list, eliminating any 
        words that match the pattern.
        """
        if len(self.global_state["present"]) > 0:
            for position, letter in self.global_state["present"]:
                word_pattern = ["." for _ in range(5)]
                word_pattern[position] = letter
                regex = "^" + ''.join(word_pattern) + "$"
                new_list = []
                for word in self.candidate_words:
                    if not re.search(regex, word):
                        new_list.append(word)

                self.candidate_words = new_list    

    def update_state(self, result):
        """
        Updates the global_state dictionary with the new result.

        This method iterates over each key in the result dictionary and updates the corresponding value in the global_state dictionary.  Keys in the dictionary:
        - "present": A set of tuples containing the letters that are in the word but in the wrong position
        - "correct": A set of tuples containing the letters that are in the word and in the correct position
        - "absent": A set of letters that are not present in the word

        Args:
            result (dict): A dictionary containing the new state to be updated. The keys should match the keys in the global_state dictionary.
        """
        for key in result:
            self.global_state[key].update(result[key])

    def print_state(self):
        print(f"global_state: {self.global_state}")

    def update_candidate_words(self):
        """
        Updates the candidate_words list based on the current global_state.

        This method first eliminates words with absent letters, then eliminates words with present letters in the correct positions, and finally keeps words with correct letters in the correct positions. The size of the candidate_words list before and after the update is printed.

        If dump_candidates is True, the updated candidate_words list is written to a file.

        Args:
            dump_candidates (bool, optional): Whether to write the updated candidate_words list to a file. Defaults to False.
        """

        # Get the size of the candidate_words list before filtering
        before_size = len(self.candidate_words)

        # Filter the candidate_words list to eliminate words with absent letters
        self._eliminate_words_with_absent_letters()

        # Further filter the list to eliminate words with present letters in the incorrect positions
        self._eliminate_words_with_present_letters()

        # Finally, keep only those words that have correct letters in the correct positions
        self._keep_words_with_correct_letters()

        # Get the size of the candidate_words list after filtering
        after_size = len(self.candidate_words)

        # Print the size of the candidate_words list before and after filtering
        print(f"before_size: {before_size}, after_size: {after_size}")


class WordListGeneratorRandom(WordListGeneratorBase):
    """
    A class used to generate a list of candidate words for the Wordle game.

    This class inherits from the WordListGeneratorBase class and overrides the get_candidate_word method to 
    return a random word from the candidate_words list.

    Attributes:
        candidate_words (list): A list of candidate words for the Wordle game.
        global_state (dict): A dictionary that stores the current state of the Wordle game.
        words_fp (str): The file path to the file containing the words.
        dump_file_count (int): The number of times the candidate_words list has been dumped to a file.
    """

    def get_candidate_word(self):
        """
        Updates the candidate_words list and returns a random word from the list.

        This method first updates the candidate_words list based on the current global_state. If the 
        list is empty after the update, it returns None. Otherwise, it returns a random word from the list.

        If dump_candidates is True, the updated candidate_words list is written to a file.

        Args:
            dump_candidates (bool, optional): Whether to write the updated candidate_words list to a file. Defaults to False.

        Returns:
            str or None: A random word from the candidate_words list, or None if the list is empty.
        """

        self.update_candidate_words()

        # Increment the dump_file_count
        self.dump_file_count += 1
        # Open a new file for writing
        with open(f"data/candidates_{self.dump_file_count:03}.txt", 'w') as file:
            # Write the candidate_words list to the file, one word per line
            file.write('\n'.join(self.candidate_words))

        # Return a random word from the list of candidate words
        if len(self.candidate_words) == 0:
            return None
        else:
            return random.choice(self.candidate_words)
        
class WordListGeneratorLLM(WordListGeneratorBase):
    """
    A class used to generate a list of candidate words for the Wordle game using a Language Model (LLM).

    This class inherits from the WordListGeneratorBase class and overrides several methods to generate prompts 
    for the LLM based on the current state of the game. The prompts include correct, absent, and present letters 
    and their positions. The class also generates a list of candidate words and writes the prompts and the list to a file.

    Attributes:
        MAX_SIZE (int): The maximum size of the candidate_words list.
        candidate_words (list): A list of candidate words for the Wordle game.
        global_state (dict): A dictionary that stores the current state of the Wordle game.
        words_fp (str): The file path to the file containing the words.
        dump_file_count (int): The number of times the candidate_words list has been dumped to a file.
    """

    MAX_SIZE = 25

    def __init__(self, words_fp):
        """
        Initializes the WordListGeneratorLLM with the file path to the words file.

        This method calls the constructor of the base class and initializes the prompt_word_list attribute to an empty string.

        Args:
            words_fp (str): The file path to the file containing the words.
        """

        super().__init__(words_fp)
        self.guessed_word = None

    @staticmethod
    def _generate_position_text(position):
        match position:
            case 0:
                return "first"
            case 1:
                return "second"
            case 2:
                return "third"
            case 3:
                return "fourth"
            case 4:
                return "fifth"
            case _:
                return "unknown"

    # TODO: clean up code
    # def generate_correct_letter_prompt(self):
    #     """
    #     Generates a prompt for the user based on the correct letters and their positions.

    #     This method constructs a string that lists the correct letters and their positions in the word. The 
    #     letters and positions are sorted in ascending order of position. If there are no correct letters, 
    #     an empty string is returned.

    #     Returns:
    #         str: A string that lists the correct letters and their positions, or an empty string 
    #              if there are no correct letters.
    #     """

    #     if len(self.global_state["correct"]) == 0:
    #         prompt_specifics =  ""
    #     else:
    #         tuple_list = list(self.global_state["correct"])
    #         tuple_list.sort(key=lambda x: x[0])
    #         prompt_specifics =  "\n".join(
    #             [f"Words must contain '{letter}' in the {self._generate_position_text(position)} position."  for position, letter in tuple_list]
    #         )
    #     if len(prompt_specifics) == 0:
    #         return ""
    #     else:
    #         return prompt_specifics

    # def generate_present_letter_prompt(self):
    #     """
    #     Generates a prompt for the user based on the present letters and their positions.

    #     This method constructs a string that lists the present letters and their positions in the word. The letters and positions are sorted in ascending order of position. If there are no present letters, an empty string is returned.

    #     Returns:
    #         str: A string that lists the present letters and their positions, or an empty string if there are no present letters.
    #     """

    #     if len(self.global_state["present"]) == 0:
    #         prompt_specifics = ""
    #     else:
    #         tuple_list = list(self.global_state["present"])
    #         tuple_list.sort(key=lambda x: x[0])
    #         prompt_specifics =  "\n".join(
    #             [f"Words must not contain the '{letter}' in the {self._generate_position_text(position)} position." for position, letter in tuple_list]
    #         )

    #     if len(prompt_specifics) == 0:
    #         return ""
    #     else:
    #         return prompt_specifics

    def generate_llm_prompt(self):
        """
        Generates a prompt for the Language Model (LLM) based on the current state of the game.

        This method first updates the candidate_words list. If the list is empty, it returns None. 
        Otherwise, it generates prompts for correct, absent, and present letters. It then constructs 
        a list of candidate words. If the list is too long, it randomly samples a subset of 
        the words. The prompts and the list of candidate words are written to a file.

        Returns:
            str or None: A string that contains the generated prompt, or None if the candidate_words list is empty.
        """

        self.update_candidate_words()

        if len(self.candidate_words) == 0:
            return None
        else:
            # generate prompt for LLM
            # TODO: clean up code
            # prompt_correct_letters = self.generate_correct_letter_prompt()
            # prompt_present_letters = self.generate_present_letter_prompt()

            if len(self.candidate_words) > self.MAX_SIZE:
                # hueristic: if the candidate word list is too long and will exceed the LLM token limit
                 self.prompt_word_list = '\n'.join(sorted(random.sample(self.candidate_words, self.MAX_SIZE)))
            else:
                # otherwise, just the whole list for the prompt
                self.prompt_word_list = '\n'.join(sorted(self.candidate_words))


            generated_prompt = (
                "Solve the puzzle by guessing a five-letter word using these clues.\n"
                # TODO: clean up code
                # + prompt_correct_letters
                # + "\n" + prompt_present_letters 
                + "\nIf more than one word meets the criteria, select the word that is more common. "
                + "Provide step-by-step instructions for how you arrived at the selected word. "
                + "When writing the instructions, do not list words. "
                + "Return only a json structure with the key 'recommendation' for the recommended word "
                + "and 'explanation' for your explantion.\n"
                + "List of candidate words:\n"
                + self.prompt_word_list
            )

            self.dump_file_count += 1
            with open(f"data/prompts_{self.dump_file_count:03}.txt", 'w') as file:
                file.write(f"guessed word: {self.guessed_word}\n")
                pretty_global_state = pp.pformat(self.global_state)
                file.write(f"global_state:\n{pretty_global_state}\n\n")
                file.write(generated_prompt)

            return generated_prompt



class OpenAIInterface:
    """
    A class used to interface with the OpenAI API.

    This class provides a method to invoke the chat API with a given prompt and return the contents to the caller.

    Attributes:
        api_key_file (str): The location of a JSON file with the API key.
        model (str): The specific model to use.
    """

    def __init__(self, api_key, model="gpt-4"):
        """
        Initializes the OpenAIInterface with the API key and the model.

        This method reads the API key from the provided JSON file and initializes an OpenAI client with the API key. 
        It also sets the model to use.

        Args:
            api_key (str): API key string
            model (str, optional): The specific model to use. Defaults to "gpt-4".
        """

        self.openai_client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, prompt):
        """
        Invokes the chat API with a given prompt and returns the contents to the caller.

        Args:
            prompt (str): The prompt to use.

        Returns:
            dict: The contents returned by the chat API.
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant to solve the Wordle puzzle."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4096,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            raise    

class ExperimentRecorder:
    """
    A class used to record the results of an experiment.

    This class provides methods to record the results of an experiment to a file.

    Attributes:
        fp (str): The file path to the file to write the results to.
    """

    def __init__(self, fp=None):
        """
        Initializes the ExperimentRecorder with the file path to the file to write the results to.

        This method opens the file for writing.

        Args:
            fp (str): The file path to the file to write the results to.
        """

        self.fp = fp
        if self.fp:
            # test if the file exists
            if not os.path.exists(self.fp):
                # if the file doesn't exist, create it and write the header
                self.file = open(fp, 'w')
                self.file.write("solver_type,initial_word,word,num_attempts\n")
            else:
                # if the file exists, append to it
                self.file = open(fp, 'a')


    def record(self, solver_type, initial_word, word, num_attempts):
        """
        Records the result of an experiment to a file.

        This method writes the result to the file, followed by a newline.

        Args:
            result (dict): The result to record.
        """
        if self.fp:
            self.file.write(solver_type + "," + initial_word + "," + word + "," + str(num_attempts) + "\n")

    def close(self):
        """
        Closes the file.
        """
        if self.fp:
            self.file.close()
