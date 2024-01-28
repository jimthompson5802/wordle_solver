import os
import sys

import numpy as np
import pandas as pd 

# Import the main functions from the random and llm solvers
from random_solver import main as random_solver
from llm_solver import main as llm_solver

# Define constants for the number of words and trials, and the file path for the experiment data
NUM_WORDS = 10
NUM_TRIALS = 10
EXPERIMENT_FP = 'data/experiment.csv'

if __name__ == '__main__':

    # Check if the experiment data file exists
    if os.path.exists(EXPERIMENT_FP):
        # If the file exists, delete it to start a new experiment
        os.remove(EXPERIMENT_FP)

    # Set the random seed to ensure reproducibility of word selection
    np.random.seed(42)

    # Load the list of words to test from a file
    df_words = pd.read_csv('data/f-past-wordle-answers.txt', header=None)
    # Select a random sample of words to test
    test_words_list = df_words.sample(NUM_WORDS)[0].str.lower().to_list()

    # Print the command line arguments
    print(sys.argv)

    # Print the experiment parameters
    print(f"Running experiment for {NUM_WORDS} words and {NUM_TRIALS} trials")

    # Prepare the command line arguments for the random solver
    sys.argv =  ['/workspaces/wordle_solver/src/random_solver.py']

    # Run the random solver for each word in the test list
    for i_word, word in enumerate(test_words_list):
        # Add the word and experiment file path to the command line arguments
        sys.argv.append(word)
        sys.argv.append('--exp_fp')
        sys.argv.append('data/experiment.csv')
        # Run the solver for the specified number of trials
        for i in range(NUM_TRIALS):
            print(f"\nRandom Solver trial {i + 1} for word {word} {i_word + 1} out of {len(test_words_list)} words")
            random_solver()
        # Remove the word and experiment file path from the command line arguments
        sys.argv.pop()
        sys.argv.pop()
        sys.argv.pop()

    # Print the command line arguments
    print(sys.argv)

    # Prepare the command line arguments for the llm solver
    sys.argv =  ['/workspaces/wordle_solver/src/llm_solver.py']

    # Run the llm solver for each word in the test list
    for i_word, word in enumerate(test_words_list):
        # Add the word, API flag, and experiment file path to the command line arguments
        sys.argv.append(word)
        sys.argv.append('--api')
        sys.argv.append('--exp_fp')
        sys.argv.append('data/experiment.csv')
        # Run the solver for the specified number of trials
        for i in range(NUM_TRIALS):
            print(f"\nLLM Solver trial {i + 1} for word {word} {i_word + 1} out of {len(test_words_list)} words")
            llm_solver()
        # Remove the word, API flag, and experiment file path from the command line arguments
        sys.argv.pop()
        sys.argv.pop()
        sys.argv.pop()
        sys.argv.pop()

    # Print the command line arguments
    print(sys.argv)