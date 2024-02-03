#
# Unless specified in further comments, the following prompt was used in Copilot Chat to generate tests
# select section of code to be tested run following prompt in Copilot Chat
# pompt: "/tests using pytest"
#

# one global modificaiton of generated code was to replace the file name "words.txt" with "data/five-letter-words.txt

import os
import sys
sys.path.append('./src')

import pytest
from unittest.mock import Mock, patch, mock_open

from wordle_solver import (
    WordListGeneratorBase, 
    WordListGeneratorRandom, 
    WordListGeneratorLLM,
    OpenAIInterface,
    ExperimentRecorder,
)

# prompt used to generate this module level fixture
# "pytest module level fixture that creates a file callled "words.txt" containing 
# these five letter words "apple", "water", "zebra" in a temporary directory. 
# The file is created before the tests are run and is deleted at the end of the tests."

WORDS = ["apple", "water", "zebra"]

@pytest.fixture(scope="module", autouse=True)
def word_file(tmp_path_factory):
    # Create a temporary directory
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "words.txt"

    # Write the words to the file
    with open(file_path, "w") as f:
        for word in WORDS:
            f.write(word + "\n")

    # Yield the file path for use in the tests
    yield str(file_path)

    # Remove the file after the tests are done
    os.remove(file_path)


###
# Tests for WordListGeneratorBase
###
def test_is_letter_in_present(word_file):
    word_list_generator = WordListGeneratorBase(word_file)
    word_list_generator.global_state["present"].add((0, 'a'))
    assert word_list_generator.is_letter_in_present('a') == True
    assert word_list_generator.is_letter_in_present('b') == False

def test_is_letter_in_correct(word_file):
    word_list_generator = WordListGeneratorBase(word_file)
    word_list_generator.global_state["correct"].add((0, 'a'))
    assert word_list_generator.is_letter_in_correct('a') == True
    assert word_list_generator.is_letter_in_correct('b') == False

def test_load(word_file):
    word_list_generator = WordListGeneratorBase(word_file)
    word_list_generator.load()
    assert len(word_list_generator.candidate_words) > 0

def test_update_state(word_file):
    word_list_generator = WordListGeneratorBase(word_file)
    result = {
        "present": {(0, 'a')},
        "correct": {(1, 'b')},
        "absent": {'c'}
    }
    word_list_generator.update_state(result)
    assert word_list_generator.global_state == result

def test_update_candidate_words(word_file):
    word_list_generator = WordListGeneratorBase(word_file)
    word_list_generator.load()
    result = {
        "present": {(0, 'a')},
        "correct": {(1, 'b')},
        "absent": {'c'}
    }
    word_list_generator.update_state(result)
    before_size = len(word_list_generator.candidate_words)
    word_list_generator.update_candidate_words()
    after_size = len(word_list_generator.candidate_words)
    assert after_size <= before_size


def test_get_candidate_word(word_file):
    word_list_generator = WordListGeneratorRandom(word_file)
    word_list_generator.load()
    # had to add this section to make the test pass
    result = {
        "present": {(0, 'a')},
        "correct": {(1, 'b')},
        "absent": {'c'}
    }
    word_list_generator.update_state(result)
    # end of section

    word = word_list_generator.get_candidate_word()
    assert word in word_list_generator.candidate_words or word is None


###
# Tests for WordListGeneratorRandom
###
    
# prompt used to generate this fixture
# "pytest fixture to remove file data/candidates_001.txt if it exists before running the test and removes it after the test"
# fixture is unmodified
@pytest.fixture
def setup_and_teardown():
    file_path = 'data/candidates_001.txt'
    
    # Setup: Remove the file if it exists before the test
    if os.path.exists(file_path):
        os.remove(file_path)

    yield  # This is where the testing happens

    # Teardown: Remove the file if it exists after the test
    if os.path.exists(file_path):
        os.remove(file_path)

# modifed generated 'def test_dump_file_count' to use the fixture
def test_dump_file_count(setup_and_teardown, word_file):

    word_list_generator = WordListGeneratorRandom(word_file)
    word_list_generator.load()

    # had to add this section to make the test pass
    result = {
        "present": {(0, 'a')},
        "correct": {(1, 'b')},
        "absent": {'c'}
    }
    word_list_generator.update_state(result)
    # end of section

    initial_count = word_list_generator.dump_file_count
    word_list_generator.get_candidate_word()
    assert word_list_generator.dump_file_count == initial_count + 1

    # added code to confirm file was really created
    file_path = os.path.join(word_list_generator.dump_file_dir, 'candidates_001.txt')
    assert os.path.exists(file_path)


###
# Tests for WordListGeneratorLLM
###    

def test_generate_llm_prompt():
    # Create a WordListGeneratorLLM instance
    word_list_generator = WordListGeneratorLLM(word_file)

    # Mock the update_candidate_words method to set the candidate_words attribute
    word_list_generator.update_candidate_words = lambda: setattr(word_list_generator, 'candidate_words', ['word1', 'word2', 'word3'])

    # Mock the open function to prevent writing to a file
    # modified to correct naming conflic
    with patch('builtins.open', new_callable=mock_open) as mock_file:
        # Call the generate_llm_prompt method
        prompt = word_list_generator.generate_llm_prompt()
        # Check that the open function was called with the expected arguments
        # relocated tis line here to match up with context variable
        mock_file.assert_called_once_with(
            os.path.join(
                word_list_generator.dump_file_dir,
                'prompts_001.txt', 
            ),
            'w'
        )

    # Check that the prompt is as expected
    expected_prompt = (
        "Solve the puzzle by guessing a five-letter word using these clues.\n"
        + "\nIf more than one word meets the criteria, select the word that is more common. "
        + "Provide step-by-step instructions for how you arrived at the selected word. "
        + "When writing the instructions, do not list words. "
        + "Return only a json structure with the key 'recommendation' for the recommended word "
        + "and 'explanation' for your explantion.\n"
        + "List of candidate words:\n"
        + 'word1\nword2\nword3'
    )
    assert prompt == expected_prompt

    

###
# Tests for OpenAIInterface
###

# took a while to get the right pompt to generate this test
# prompt: /tests using pytest mock OpenAI call and self.openai_client.chat.completions.create call
@patch('wordle_solver.OpenAI')
def test_openai_chat(mock_openai):
    mock_openai.return_value.chat.completions.create.return_value = Mock(choices=[Mock(message=Mock(content='mocked content'))])
    openai_interface = OpenAIInterface('fake-api-key')
    prompt = 'test prompt'
    response = openai_interface.chat(prompt)
    assert response == 'mocked content'
    mock_openai.return_value.chat.completions.create.assert_called_once_with(
        model=openai_interface.model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant to solve the Wordle puzzle."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

###
# Tests for ExperimentRecorder
###

# prompt: /tests using pytest mock all file operations

@patch('os.path.exists', return_value=False)
@patch('builtins.open', new_callable=mock_open)
def test_experiment_recorder_init(mock_file, mock_exists):
    # Create an ExperimentRecorder instance
    recorder = ExperimentRecorder('test.txt')

    # Check that the file was opened for writing
    mock_file.assert_called_once_with('test.txt', 'w')

    # Check that the header was written to the file
    mock_file().write.assert_called_once_with("solver_type,initial_word,word,num_attempts\n")

@patch('builtins.open', new_callable=mock_open)
def test_experiment_recorder_record(mock_file):
    # Create an ExperimentRecorder instance
    recorder = ExperimentRecorder('test.txt')

    # Call the record method
    recorder.record('solver_type', 'initial_word', 'word', 1)

    # Check that the result was written to the file
    mock_file().write.assert_called_with('solver_type,initial_word,word,1\n')

@patch('builtins.open', new_callable=mock_open)
def test_experiment_recorder_close(mock_file):
    # Create an ExperimentRecorder instance
    recorder = ExperimentRecorder('test.txt')

    # Call the close method
    recorder.close()

    # Check that the file was closed
    mock_file().close.assert_called_once()    