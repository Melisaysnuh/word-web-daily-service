import pytest
from utilities.custom_types import WordObj
from utilities.helpers import filter_for_center

@pytest.fixture
def word_list ():
        return [WordObj(word='imagine', points=0, isogram=False, definition=['dummy']), WordObj(word='imagination', points=0, isogram=False, definition=['dummy']), WordObj(word='imaginatorium', points=0, isogram=False, definition=['dummy'])]


# should handle reciving an empty to_filter
# should handle receiving an empty letter


def test_filter_for_center_basic(word_list): # type: ignore
        letter = "o"
        result = filter_for_center(word_list, letter) # type: ignore
        assert len(result) > 0
        assert result == [
        WordObj(word='imagination', points=0, isogram=False, definition=['dummy']), WordObj(word='imaginatorium', points=0, isogram=False, definition=['dummy']),]
        assert isinstance(result[0], WordObj)

def test_filter_for_center_bad_input_handling(word_list): # type: ignore
        bad_word_list = []


        assert filter_for_center(bad_word_list, "a") == [] # type: ignore

        assert filter_for_center(word_list, "") == word_list # type: ignore
