import argparse
import json
import random
import sys

from wordle_solver import WordListGeneratorLLM, OpenAIInterface

CANIDATE_FIRST_WORD_LIST = ["adieu", "trace", "crate",]

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
    word = random.choice(CANIDATE_FIRST_WORD_LIST)
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

        # Initialize a dictionary to store the result
        result = {"correct": [], "present": [], "absent": []}

        # Initialize a variable to control the input loop
        input_ok = "n"

        # Loop until the user confirms the input is correct
        while input_ok == "n":
            # Ask the user to enter the Wordle response
            wordle_response = input("Enter wordle response: ")
            # Ask the user to confirm the response is correct
            input_ok = input(f"Is this correct: '{wordle_response}'? (y/n)")

        # Loop over each letter in the word and its corresponding feedback
        for i, feedback_pair in enumerate(zip(word, wordle_response)):
            # Unpack the letter and feedback from the pair
            letter, feedback = feedback_pair

            # If the feedback is "g", the letter is correct and in the correct position
            if feedback == "g":
                # Add the position and letter to the "correct" list
                result["correct"].append((i, letter))

            # If the feedback is "y", the letter is correct but in the wrong position
            elif feedback == "y":
                # Add the position and letter to the "present" list
                result["present"].append((i, letter))

            # If the feedback is ".", the letter is not in the word
            elif feedback == ".":
                # Check if the letter is not already in the "correct" or "present" lists
                if (letter not in [x[1] for x in result["correct"]] and 
                    letter not in [x[1] for x in result["present"]] and
                    not word_list.is_letter_in_correct(letter) and
                    not word_list.is_letter_in_present(letter)):
                    # Add the letter to the "absent" list
                    result["absent"].append(letter)
            # If the feedback is anything else, it's unknown and we exit the program
            else:
                print(f"Unknown feedback: {feedback}")
                sys.exit(1)

        # Print the result
        print(f'The result is {result}')

        # Update the state of the word list with the result of the last guess
        word_list.update_state(result)

        # Print the current state of the word list
        word_list.print_state()

        # Generate a new prompt for the language model
        generated_prompt = word_list.generate_llm_prompt()

        # If the API flag is set, use the OpenAI API to get a response
        if api:
            # Send the generated prompt to the OpenAI API and parse the response
            llm_response = json.loads(openai_interface.chat(generated_prompt))

            # Extract the recommended word from the response
            recommended_word = llm_response["recommendation"]

            # Print the recommended word and the list of prompt words
            print(f"WSVA recommendation: '{recommended_word}' from list:\n{word_list.prompt_word_list}")

            # Have user confirm use of the recommended word or enter another word
            input_ok = "n"
            while input_ok == "n":
                input_ok = input(f"\nUse recommended word '{recommended_word}'? (y/n)")

                if input_ok == "y":
                    word = recommended_word
                    break
                else:
                    while input_ok == "n":
                        word = input("What word should be used?: ")

                        # Ask the user to confirm the response is correct
                        input_ok = input(f"Is this correct: '{word}'? (y/n)")

        # If the API flag is not set, ask the user to manually enter a word
        else:
            print("\nCopy and paste the prompt file to OpenAI Playground and enter the recommendation")
            word = input("Enter a word: ")

        # If no word was entered or recommended, abort the game
        if word is None:
            print("\n>>>>No candidate words left aborting...")
            break

        # Print the final state of the word list
        print(f"global_state: {word_list.global_state}")    

if __name__ == "__main__":
    main()