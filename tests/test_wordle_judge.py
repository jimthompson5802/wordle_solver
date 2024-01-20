import sys
sys.path.append('./src')

import random

import pytest
from wordle_judge import WordleJudge


def test_judge_guess_correct():
    random.seed(0)
    judge = WordleJudge('apple')
    assert judge.judge_guess('apple') == True

def test_judge_guess_incorrect():
    random.seed(0)
    judge = WordleJudge('apple')
    result = judge.judge_guess('alloy')
    print(result)
    assert result == {"present": ['l'], "correct":  [(0, 'a')], "absent": ['o', 'y']}

def test_judge_guess_case_insensitive():
    random.seed(0)
    judge = WordleJudge('Apple')
    assert judge.judge_guess('APPLE') == True

def test_judge_guess_partial_correct():
    random.seed(0)
    judge = WordleJudge('apple')
    result = judge.judge_guess('ample')
    print(result)
    assert result == {"present": [], "correct":  [(0, 'a'), (2, 'p'), (3, 'l'), (4, 'e')], "absent": ['m']}