from abc import ABC
import random
import re

class WordListGeneratorBase:
    def __init__(self, words_fp):
        self.words_fp = words_fp
        self.candidate_words = []
        self.global_state = {
            "present": set(),
            "correct": set(),
            "absent": set()
        }
        self.dump_file_count = 0

    def load(self):
        with open(self.words_fp, 'r') as file:
            self.candidate_words = [line.strip() for line in file]

    def _eliminate_words_with_absent_letters(self):
        letter_regex = '[' + ''.join(self.global_state["absent"]) + ']'
        self.candidate_words = [word for word in self.candidate_words if not re.search(letter_regex, word)]

    def _keep_words_with_correct_letters(self):
        word_pattern = ["." for _ in range(5)]
        for position, letter in self.global_state["correct"]:
            word_pattern[position] = letter
        regex = "^" + ''.join(word_pattern) + "$"
        correct_regex = re.compile(regex)
        self.candidate_words = [word for word in self.candidate_words if correct_regex.match(word)]
    
    def _eliminate_words_with_present_letters(self):
        if len(self.global_state["present"]) > 0:
            for position, letter in self.global_state["present"]:
                word_pattern = ["." for _ in range(5)]
                word_pattern[position] = letter
                regex = "^" + ''.join(word_pattern) + "$"
                new_list = []
                for word in self.candidate_words:
                    if not re.search(regex, word):
                        new_list.append(word)
                # self.candidate_words = [word for word in self.candidate_words if not re.search(regex, word)]
                self.candidate_words = new_list
    
    def update_state(self, result):
        for key in result:
            self.global_state[key].update(result[key])

    def print_state(self):
        print(f"global_state: {self.global_state}")

    def update_candidate_words(self, dump_candidates=False):
        before_size = len(self.candidate_words)
        # Update the list of candidate words
        self._eliminate_words_with_absent_letters()

        self._eliminate_words_with_present_letters()

        self._keep_words_with_correct_letters()
        

        # get size after filtering
        after_size = len(self.candidate_words)

        # print before and after size
        print(f"before_size: {before_size}, after_size: {after_size}")

        if dump_candidates:
            self.dump_file_count += 1
            with open(f"data/candidates_{self.dump_file_count:03}.txt", 'w') as file:
                file.write('\n'.join(self.candidate_words))


class WordListGeneratorRandom(WordListGeneratorBase):

    def get_candidate_word(self, dump_candidates=False):
        self.update_candidate_words(dump_candidates=dump_candidates)

        # Return a random word from the list of candidate words
        if len(self.candidate_words) == 0:
            return None
        else:
            return random.choice(self.candidate_words)
        
class WordListGeneratorLLM(WordListGeneratorBase):

    MAX_SIZE = 500

    prompt_template1 = "Select words from a list of words with these criteria. \n"

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


    def generate_correct_letter_prompt(self):
        if len(self.global_state["correct"]) == 0:
            return "There are no correct letters. "
        else:
            return ", ".join(
                [f"'{letter}' in the {self._generate_position_text(position)}"  for position, letter in self.global_state["correct"]]
            )

    def generate_present_letter_prompt(self):
        if len(self.global_state["present"]) == 0:
            return "  "
        else:
            return ", ".join(
                [f" '{letter}'  in the {self._generate_position_text(position)} position " for position, letter in self.global_state["present"]]
            )

    def generate_absent_letter_prompt(self):
        if len(self.global_state["absent"]) == 0:
            return "  "
        else:
            return ", ".join(
                [f" '{letter}'" for letter in self.global_state["absent"]]
            )

    def generate_llm_prompt(self):
        self.update_candidate_words(dump_candidates=False)

        if len(self.candidate_words) == 0:
            return None
        else:
            # generate prompt for LLM
            prompt_correct_letters = self.generate_correct_letter_prompt()
            prompt_absent_letters = self.generate_absent_letter_prompt()
            prompt_present_letters = self.generate_present_letter_prompt()

            if len(self.candidate_words) > self.MAX_SIZE:
                 candidate_word_list = '\n'.join(random.sample(self.candidate_words, 500))
            else:
                candidate_word_list = '\n'.join(self.candidate_words)

            self.dump_file_count += 1
            with open(f"data/prompts_{self.dump_file_count:03}.txt", 'w') as file:
                file.write(
                    self.prompt_template1
                    + "These letters in the correct positions: " 
                    + prompt_correct_letters 
                    + "\n" 
                    + "These letters are not in the word: "
                    + prompt_absent_letters
                    + "\n"
                    + f"These letters are in word but in wrong poistion: {prompt_present_letters}. "
                    + "\n"
                    + "Select a word from the list that solves the puzzle or can be used to eliminate a large number of words\n"
                    + candidate_word_list
                )



