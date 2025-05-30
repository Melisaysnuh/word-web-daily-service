import pytest

from utilities.helpers import get_unique_letters

@pytest.fixture
def letter_list ():
        return ["a", "a", "b", "c", "d", "d", "d"]


# should strip repeat letters



def test_get_unique_letters(letter_list): # type: ignore
        result = get_unique_letters(letter_list) # type: ignore
        assert len(result) == 4
        assert result == ["a", "b", "c", "d"]
        assert isinstance(result[0], str)
