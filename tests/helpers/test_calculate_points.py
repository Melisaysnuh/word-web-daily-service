import pytest
from utilities.helpers import calculate_word_points
from utilities.custom_types import WordObj



@pytest.fixture
def isogram_list ():
    # The isograms_list contains one WordObj with word 'charging'
    return [WordObj(word='charging', points=0, isogram=False, definition=['dummy'])]

def test_calculate_word_points_short_word(isogram_list): # type: ignore
    word = WordObj(word='hare', points=0, isogram=False, definition=['dummy'])
    result = calculate_word_points(word, isogram_list) # type: ignore
    assert result.points == 2
    assert isinstance(result, WordObj)

def test_calculate_word_points_normal_word(isogram_list): # type: ignore
    word = WordObj(word='harem', points=0, isogram=False, definition=['dummy'])
    result = calculate_word_points(word, isogram_list) # type: ignore
    assert result.points == 5
    assert isinstance(result, WordObj)

def test_calculate_word_points_isogram_word(isogram_list): # type: ignore
    word = WordObj(word='charging', points=0, isogram=False, definition=['dummy'])
    result = calculate_word_points(word, isogram_list) # type: ignore
    assert result.points == len('charging') + 7
    assert result.isogram is True
    assert isinstance(result, WordObj)

def test_calculate_word_points_handles_invalid_input(isogram_list): # type: ignore
    with pytest.raises(AttributeError):
        # Passing an invalid type, like a string instead of WordObj
        calculate_word_points('not_a_word_obj', isogram_list) # type: ignore

    with pytest.raises(Exception):
        # Passing None
        calculate_word_points(None, isogram_list) # type: ignore