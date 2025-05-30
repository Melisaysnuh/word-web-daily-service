import pytest
from utilities.custom_types import WordObj
from utilities.helpers import get_center

@pytest.fixture
def word_list ():
        return [WordObj(word='imagine', points=0, isogram=False, definition=['dummy']), WordObj(word='imagination', points=0, isogram=False, definition=['dummy']), WordObj(word='imaginatorium', points=0, isogram=False, definition=['dummy'])]

@pytest.fixture
def letter_list():
        return ['i', 'm', 'a']



# should receive a list of word objects, and a letter, and should call the filter for center between 1-7 times but no more.
# if the length of the filtered anagrams is less than 60, it should return that letter. if the lists are all too long, it should return a random letter
# should always return a letter
# should handle empty word lists




def test_get_center_basic(word_list, letter_list): # type: ignore
        result = get_center(word_list, letter_list) # type: ignore
        assert len(result) > 0
        assert result == 'i'

def test_get_center_bad_input_handling(word_list, letter_list): # type: ignore
        bad_word_list = []


        result=get_center(bad_word_list, letter_list)# type: ignore
        assert len(result) > 0
