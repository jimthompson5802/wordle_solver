
from wordle_solver import WordListGeneratorRandom, WordListGeneratorLLM
from wordle_judge import WordleJudge

def main():
    # Create a WordleJudge object
    # wordle_game = WordleJudge("apple")
    # wordle_game = WordleJudge("large")
    wordle_game = WordleJudge("zebra")

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