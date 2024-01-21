class WordleJudge:
    """
    A class used to judge the guesses in the Wordle game.

    This class provides methods to judge a guess based on the correct word. The judge_guess
     method returns a dictionary that lists the present, correct, and absent letters and their positions.

    Attributes:
        correct_word (str): The correct word in the Wordle game.
    """

    def __init__(self, correct_word):
        """
        Initializes the WordleJudge with the correct word.

        Args:
            correct_word (str): The correct word in the Wordle game.
        """
        self.correct_word = correct_word.lower()

    def judge_guess(self, guess):
        """
        Judges a guess based on the correct word.

        This method compares the guess to the correct word. If the guess is correct, it returns True. Otherwise, it returns a dictionary that lists the present, correct, and absent letters and their positions. The dictionary has the following format:
        - present: A list of tuples that contain the incorrect position and letter found in the word.
        - correct: A list of tuples that contain the position and letter of the correct letters.
        - absent: A list of letters that are absent from the word.

        Args:
            guess (str): The guess to be judged.

        Returns:
            bool or dict: True if the guess is correct. Otherwise, a dictionary that lists the present, correct, and absent letters and their positions.
        """
  
        guess = guess.lower()

        if guess == self.correct_word:
            return True
        else:
            result = {"present": [], "correct": [], "absent": []}

            for i, letter in enumerate(guess):
                if letter == self.correct_word[i]:
                    result["correct"].append((i, letter))
                elif letter in self.correct_word:
                    # Avoid counting the same letter more than once
                    if letter not in result["present"]:
                        result["present"].append((i, letter))
                else:
                    result["absent"].append(letter)

            return result

if __name__ == "__main__":
    # Example Usage
    wordle_game = WordleJudge("apple")
    result = wordle_game.judge_guess("alloy")
    print(result)
