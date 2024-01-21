
from wordle_solver import WordListGeneratorRandom, WordListGeneratorLLM
from wordle_judge import WordleJudge


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

    # Create a WordList object
    word_list = WordListGeneratorLLM("data/five-letter-words.txt")
    word_list.load()

    # create initial guess
    word = "adieu"
    attemp_count = 0
    while attemp_count < 7:
        attemp_count += 1
        if attemp_count < 7:
            print(f'attempt {attemp_count}')
        else:
            print(f'>>>>Failed wordle game: attempt {attemp_count}')

        if attemp_count > 20:
            print(f'>>>>Exceed max attempt: attempt {attemp_count}')
            break

        result = {"correct": [], "present": [], "absent": []}
        result.update(create_correct_result())
        result.update(create_present_result())
        result.update(create_absent_result())
        print(f'The result is {result}')
        
        # Update the word list
        word_list.update_state(result)
        word_list.print_state()
        
        word_list.generate_llm_prompt()
        if word is None:
            print(">>>>No candidate words left")
            break

    print(f"global_state: {word_list.global_state}")
    
if __name__ == "__main__":
    main()