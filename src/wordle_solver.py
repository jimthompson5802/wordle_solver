from abc import ABC, abstractmethod
import random
import re
import os

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

    def _eliminate_words_with_letters(self):
        letter_regex = '[' + ''.join(self.global_state["absent"]) + ']'
        return [word for word in self.candidate_words if not re.search(letter_regex, word)]

    def _generate_regex_for_correct(self):
        word_pattern = ["." for _ in range(5)]
        for position, letter in self.global_state["correct"]:
            word_pattern[position] = letter
        regex = "^" + ''.join(word_pattern) + "$"
        return re.compile(regex)
    
    def update_state(self, result):
        for key in result:
            self.global_state[key].update(result[key])

    def print_state(self):
        print(f"global_state: {self.global_state}")

    @abstractmethod
    def get_candidate_words(self):
        raise NotImplementedError


class WordListGeneratorRandom(WordListGeneratorBase):

    def get_candidate_words(self, dump_candidates=False):
        before_size = len(self.candidate_words)
        # Update the list of candidate words
        self.candidate_words = self._eliminate_words_with_letters()

        # Generate regex for correct guesses
        correct_regex = self._generate_regex_for_correct()

        # Filter candidate 
        # words based on correct guesses
        self.candidate_words = [word for word in self.candidate_words if correct_regex.match(word)]

        # get size after filtering
        after_size = len(self.candidate_words)

        # print before and after size
        print(f"before_size: {before_size}, after_size: {after_size}")

        if dump_candidates:
            self.dump_file_count += 1
            with open(f"data/candidates_{self.dump_file_count:03}.txt", 'w') as file:
                file.write('\n'.join(self.candidate_words))

        # Return a random word from the list of candidate words
        if len(self.candidate_words) == 0:
            return None
        else:
            return random.choice(self.candidate_words)
