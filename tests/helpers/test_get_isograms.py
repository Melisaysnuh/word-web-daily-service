from utilities.custom_types import WordObj
from utilities.helpers import get_isograms


# Should receive a list of word objects and a list of letters. Should double check that the words in the word list have the first letter in the list, AND returns only words that are made up of only the words in the letter list.

def test_get_isograms():
    word_list = [
        WordObj(word='imagine'),
        WordObj(word='acacia'),
        WordObj(word='acai'),
        WordObj(word='calorie'),
        WordObj(word='lore'),
        WordObj(word='local')
    ]

    letter_list = ["c", "a", "l", "o", "r", "i", "e"]

    result = get_isograms(word_list, letter_list)
    matched_words = [w.word for w in result]

    assert 'calorie' in matched_words
    assert 'lore' not in matched_words
    assert 'acai' in matched_words
    assert 'acacia' in matched_words
    assert 'imagine' not in matched_words
    assert 'local' in matched_words