import argparse

from wordle_solver import WordListGeneratorLLM
from wordle_judge import WordleJudge

def main():
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('word', type=str, help='A 5-letter word')
    parser.add_argument('--api', type=bool, default=False, help='A boolean flag for api')

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

    # create initial guess
    word = "adieu"
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
            word_list.update_state(result)
            word_list.print_state()
            
            word_list.generate_llm_prompt()
            word = input("Enter a word: ")
            if word is None:
                print(">>>>No candidate words left")
                break
    
    print(f"global_state: {word_list.global_state}")
    
if __name__ == "__main__":
    main()