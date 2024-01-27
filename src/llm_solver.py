import argparse
import json
import random

from wordle_solver import WordListGeneratorLLM, OpenAIInterface
from wordle_judge import WordleJudge

CANIDATE_FIRST_WORD_LIST = ["adieu", "trace", "crate",]

def main():
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('word', type=str, help='A 5-letter word')
    parser.add_argument('--api', action='store_true', help='A boolean flag for api')

    args = parser.parse_args()

    # Access the arguments
    word = args.word
    api = args.api

    # Ensure the word is 5 letters long
    if len(word) != 5:
        raise argparse.ArgumentTypeError("Word must be 5 letters long")

    print(f"Word: {word}, API: {api}")

    # Create a WordleJudge object
    wordle_game = WordleJudge(word)
 
    # Create a WordList object
    word_list = WordListGeneratorLLM("data/five-letter-words.txt")
    word_list.load()

    # Create an OpenAIInterface object
    openai_interface = OpenAIInterface("/openai/api_key.json")

    # create initial guess
    word = random.choice(CANIDATE_FIRST_WORD_LIST)
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
            word_list.update_state(result)
            word_list.print_state()
            
            generated_prompt = word_list.generate_llm_prompt()
            if api:
                llm_response = json.loads(openai_interface.chat(generated_prompt))
                llm_response_count += 1
                with open(f"data/llm_response_{llm_response_count:03}.json", "w") as f:
                    json.dump(llm_response, f)

                word = llm_response["recommendation"]
            else:
                print("\nCopy and paste the prompt file to OpenAI Playground and enter the recommendation")
                word = input("Enter a word: ")
            if word is None:
                print("\n>>>>No candidate words left")
                break
    
    print(f"global_state: {word_list.global_state}")
    
if __name__ == "__main__":
    main()