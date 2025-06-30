import pytest
from unittest import mock
from utilities.wordmgmt import get_random_isogram


def test_get_random_isogram_success():

    words = ['abcdefg', 'ggggggg', 'abcdefg']  # Only 'abcdefg' is valid


    with mock.patch('utilities.wordmgmt.validate_word', side_effect=lambda w: w == 'abcdefg'):
        result = get_random_isogram(words)
        assert result == 'abcdefg'

def test_get_random_isogram_failure():

    words = ['abcdefg', 'bcdefga', 'cdefgab']


    with mock.patch('utilities.wordmgmt.validate_word', return_value=None):

        with mock.patch('utilities.wordmgmt.remove_invalid_word'):
            with pytest.raises(ValueError, match='No validated 7-letter isogram words found.'):
                return get_random_isogram(words)


def test_get_random_isogram_no_isograms():

    words = ['aaaaaaa', 'bbbbbbb', 'ccccccc']  # all have repeating letters


    with mock.patch('utilities.wordmgmt.validate_word'):
        with pytest.raises(ValueError, match='No validated 7-letter isogram words found.'):
            return get_random_isogram(words)
