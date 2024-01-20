class WordleJudge:
    def __init__(self, correct_word):
        self.correct_word = correct_word.lower()

    def judge_guess(self, guess):
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
                        result["present"].append(letter)
                else:
                    result["absent"].append(letter)

            return result

if __name__ == "__main__":
    # Example Usage
    wordle_game = WordleJudge("apple")
    result = wordle_game.judge_guess("alloy")
    print(result)
