import argparse
import json
import random

from wordle_solver import WordListGeneratorRandom, ExperimentRecorder
from wordle_judge import WordleJudge

CANIDATE_FIRST_WORD_LIST = ["adieu", "trace", "crate",]


def main():
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('word', type=str, help='A 5-letter word')
    parser.add_argument('--exp_fp', type=str, default=None, help='File path to record experiment results')
    parser.add_argument('--first_word', type=str, default=None, help='The first word to use')

    args = parser.parse_args()

    # Access the arguments
    word = args.word
    experiment_fp = args.exp_fp
    first_word = args.first_word

    # Ensure the word is 5 letters long
    if len(word) != 5:
        raise argparse.ArgumentTypeError("Word must be 5 letters long")

    print(f"Word: {word}, experiment_fp: {experiment_fp}, First Word: {first_word}")

    # Create a WordleJudge object
    wordle_game = WordleJudge(word)

    # Create a ExperimentRecorder object
    if experiment_fp:
        experiment_recorder = ExperimentRecorder(experiment_fp)

    # Create a WordList object
    wordle_virtual_assistant = WordListGeneratorRandom("data/five-letter-words.txt")
    wordle_virtual_assistant.load()

    # create initial guess
    if first_word:
        initial_word = word = first_word
    else:
        initial_word = word = random.choice(CANIDATE_FIRST_WORD_LIST)
        
    result = False
    attemp_count = 0
    while not isinstance(result, bool) or not result:
        attemp_count += 1
        if attemp_count < 7:
            print(f'attempt {attemp_count} guess is {word}')
        else:
            print(f'>>>>Failed wordle game: attempt {attemp_count} guess is {word}')

        if attemp_count > 20:
            print(f'>>>>Exceed max attempt: attempt {attemp_count}')
            break

        result = wordle_game.judge_guess(word)
        print(f'The result is {result}')
        if not isinstance(result, bool):
            # Update the word list
            wordle_virtual_assistant.update_state(result)
            wordle_virtual_assistant.print_state()
            
            # Get a random word
            word = wordle_virtual_assistant.get_candidate_word()
            if word is None:
                print(">>>>No candidate words left")
                break
    
    print(f"global_state: {wordle_virtual_assistant.global_state}")
    if experiment_fp:
        experiment_recorder.record("random", initial_word, word, attemp_count)
        experiment_recorder.close()
        
if __name__ == "__main__":
    main()