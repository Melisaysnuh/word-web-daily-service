from unittest import mock
from utilities.custom_types import WordObj
from utilities.wordmgmt import return_validated_array


def test_return_validated_array_success():

    words = ['abcdefg', 'Gerry', 'hellion']


    with mock.patch('utilities.wordmgmt.validate_word', side_effect=lambda w: w == 'hellion'):
        result = return_validated_array(words)
        assert result == [WordObj(word='hellion', points=0, isogram=False, definition=None)]

def test_return_validated_array_failure():
    words = ['abcdefg', 'Gerry', 'hellion']


    with mock.patch('utilities.wordmgmt.validate_word', side_effect=lambda w: w == 'iris'):
        result = return_validated_array(words)
        assert result == []