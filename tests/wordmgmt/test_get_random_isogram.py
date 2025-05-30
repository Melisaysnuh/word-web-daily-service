import pytest
from unittest import mock
from utilities.wordmgmt import get_random_isogram


def test_get_random_isogram_success():
    # Provide a mocked list of words where one is a valid isogram
    words = ['abcdefg', 'ggggggg', 'abcdefg']  # Only 'abcdefg' is valid

    # Mock validate_word to return True only for 'abcdefg'
    with mock.patch('utilities.wordmgmt.validate_word', side_effect=lambda w: w == 'abcdefg'):
        result = get_random_isogram(words)
        assert result == 'abcdefg'

def test_get_random_isogram_failure():
    # Provide a mocked list of words where none validate
    words = ['abcdefg', 'bcdefga', 'cdefgab']

    # Mock validate_word to always return False
    with mock.patch('utilities.wordmgmt.validate_word', return_value=None):
        # Also mock remove_invalid_word so we don't touch the file
        with mock.patch('utilities.wordmgmt.remove_invalid_word'):
            with pytest.raises(ValueError, match='No 7-letter isogram words found.'):
                get_random_isogram(words)


def test_get_random_isogram_no_isograms():
    # Provide a mocked list with no 7-letter words or no isograms
    words = ['aaaaaaa', 'bbbbbbb', 'ccccccc']  # all have repeating letters

    # Even though validate_word isn’t called, we can still patch it safely
    with mock.patch('utilities.wordmgmt.validate_word'):
        with pytest.raises(ValueError, match='No 7-letter isogram words found.'):
            get_random_isogram(words)
