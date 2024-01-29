import argparse
import json
import random

from wordle_solver import WordListGeneratorLLM, OpenAIInterface, ExperimentRecorder
from wordle_judge import WordleJudge

CANIDATE_FIRST_WORD_LIST = ["adieu", "trace", "crate",]

def main():
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('word', type=str, help='A 5-letter word')
    parser.add_argument('--api', action='store_true', help='A boolean flag for api')
    parser.add_argument('--exp_fp', type=str, default=None, help='File path to record experiment results')
    parser.add_argument('--first_word', type=str, default=None, help='The first word to use')

    args = parser.parse_args()

    # Access the arguments
    word = args.word
    api = args.api
    experiment_fp = args.exp_fp
    first_word = args.first_word

    # Ensure the word is 5 letters long
    if len(word) != 5:
        raise argparse.ArgumentTypeError("Word must be 5 letters long")

    print(f"Word: {word}, API: {api}, experiment_fp: {experiment_fp}, First Word: {first_word}")

    # Create a WordleJudge object
    wordle_game = WordleJudge(word)

   # Create a ExperimentRecorder object
    if experiment_fp:
        experiment_recorder = ExperimentRecorder(experiment_fp)

    # Create a WordList object
    wordle_virtual_assistant = WordListGeneratorLLM("data/five-letter-words.txt")
    wordle_virtual_assistant.load()

    # Create an OpenAIInterface object
    openai_interface = OpenAIInterface("/openai/api_key.json")

    # create initial guess
    if first_word:
        initial_word = word = first_word
    else:
        initial_word = word = random.choice(CANIDATE_FIRST_WORD_LIST)
        
    result = False
    attemp_count = 0
    llm_response_count = 0
    while not isinstance(result, bool) or not result:
        attemp_count += 1
        if attemp_count < 7:
            print(f'\nAttempt {attemp_count} guess is {word}')
        else:
            print(f'\n>>>>Exceed wordle game limit: attempt {attemp_count} guess is {word}')

        if attemp_count > 20:
            print(f'\n>>>>Exceed max attempt: attempt {attemp_count} aborting...')
            break

        result = wordle_game.judge_guess(word)
        print(f'The result is {result}')
        if not isinstance(result, bool):
            # Update the word list
            wordle_virtual_assistant.guessed_word = word
            wordle_virtual_assistant.update_state(result)
            wordle_virtual_assistant.print_state()
            
            generated_prompt = wordle_virtual_assistant.generate_llm_prompt()
            if api:
                llm_response = json.loads(openai_interface.chat(generated_prompt))
                llm_response_count += 1
                with open(f'data/llm_response_{llm_response_count:03}.txt', 'w') as f:
                    pretty_json = json.dumps(llm_response, indent=4)
                    f.write(pretty_json)

                word = llm_response["recommendation"]
            else:
                print("\nCopy and paste the prompt file to OpenAI Playground and enter the recommendation")
                word = input("Enter a word: ")
            if word is None:
                print("\n>>>>No candidate words left")
                break
    
    print(f"global_state: {wordle_virtual_assistant.global_state}")
    if experiment_fp:
        experiment_recorder.record("llm", initial_word, word, attemp_count)
        experiment_recorder.close()

if __name__ == "__main__":
    main()