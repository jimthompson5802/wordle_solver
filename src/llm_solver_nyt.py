import argparse
import json

from wordle_solver import WordListGeneratorLLM, OpenAIInterface


def create_correct_result():
    word = input("Enter correct letter pattern: ")
    result = {"correct": []}
    for i, letter in enumerate(word):
        if letter != '.':
            result["correct"].append((i, letter))
    return result

def create_present_result():
    word = input("Enter present letter pattern: ")
    result = {"present": []}
    for i, letter in enumerate(word):
        if letter != '.':
            result["present"].append((i, letter))
    return result

def create_absent_result():
    word = input("Enter absent letter pattern: ")
    result = {"absent": []}
    for letter in word:
        result["absent"].append(letter)
    return result

def main():
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('--api', action='store_true', help='A boolean flag for api')

    args = parser.parse_args()

    # Access the arguments
    api = args.api

    print(f"API: {api}")

    # Create a WordList object
    word_list = WordListGeneratorLLM("data/five-letter-words.txt")
    word_list.load()

    # Create an OpenAIInterface object
    openai_interface = OpenAIInterface("/openai/api_key.json")


    # create initial guess
    word = "adieu"
    attemp_count = 0
    while attemp_count < 7:
        attemp_count += 1
        if attemp_count < 7:
            print(f'\nattempt {attemp_count} word is {word}')
        else:
            print(f'\n>>>>Failed wordle game: attempt {attemp_count} ')

        if attemp_count > 20:
            print(f'\n>>>>Exceed max attempt: attempt {attemp_count} aborting...')
            break

        result = {"correct": [], "present": [], "absent": []}
        result.update(create_correct_result())
        result.update(create_present_result())
        result.update(create_absent_result())
        print(f'The result is {result}')
        
        # Update the word list
        word_list.update_state(result)
        word_list.print_state()
        generated_prompt = word_list.generate_llm_prompt()
        if api:
            llm_response = json.loads(openai_interface.chat(generated_prompt))
            word = llm_response["recommendation"]
        else:
            print("\nCopy and paste the prompt file to OpenAI Playground and enter the recommendation")
            word = input("Enter a word: ")

        if word is None:
            print("\n>>>>No candidate words left aborting...")
            break

    print(f"global_state: {word_list.global_state}")
    
if __name__ == "__main__":
    main()