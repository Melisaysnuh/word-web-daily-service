import pytest

from utilities.helpers import filter_list_by_length

@pytest.fixture
def word_list ():
        return ["a", "aa", "aaa", "aaaa", "aaaaa"]


# should receive a word list of strings, and 2 numbers, and return only words with length between those two numbers



def test_filter_list_by_length_basic(word_list): # type: ignore
        result = filter_list_by_length(word_list, 1,3) # type: ignore
        assert len(result) == 3
        assert result == ["a", "aa", "aaa"]
        assert isinstance(result[0], str)


