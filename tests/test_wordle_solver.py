import sys
sys.path.append('./src')

import pytest
from wordle_solver import WordListGeneratorBase, WordListGeneratorRandom

def test_load_words():
    generator = WordListGeneratorBase('data/five-letter-words.txt')
    generator.load()
    assert len(generator.candidate_words) > 0

def test_eliminate_words_with_letters():
    generator = WordListGeneratorBase('data/five-letter-words.txt')
    generator.load()
    generator.global_state["absent"].add('a')
    generator.candidate_words = generator._eliminate_words_with_absent_letters()
    assert all('a' not in word for word in generator.candidate_words)

def test_generate_regex_for_correct():
    generator = WordListGeneratorBase('data/five-letter-words.txt')
    generator.global_state["correct"].add((0, 'a'))
    regex = generator._generate_regex_for_correct()
    assert regex.match('apple')
    assert not regex.match('pear')

def test_update_state():
    generator = WordListGeneratorBase('data/five-letter-words.txt')
    generator.update_state({"present": {'a'}, "correct": {(0, 'a')}, "absent": {'b'}})
    assert generator.global_state == {"present": {'a'}, "correct": {(0, 'a')}, "absent": {'b'}}

def test_get_candidate_words():
    generator = WordListGeneratorRandom('data/five-letter-words.txt')
    generator.load()

    before_size = len(generator.candidate_words)

    # get first word in list as test word
    word_to_test = generator.candidate_words[0]

    # setup globabl state to reflect test word
    generator.global_state["correct"].add((0, word_to_test[0]))
    generator.global_state["present"].add(word_to_test[1])
    generator.global_state["absent"].add('b')

    # make sure test word is still in the list after filtering
    word = generator.get_candidate_words()
    assert word in generator.candidate_words

    # make sure the list is smaller after filtering
    assert len(generator.candidate_words) < before_size
   