import random
import re

from utilities.types import WordObj




def calculate_word_points (word: WordObj, isograms_list: list[WordObj]):

    if len(word.word) < 5:
        word.points = 2
        return word
    elif isograms_list.count(word) > 0:
        word.points = len(word.word) +7
        word.isogram=True
        return word
    else:
        word.points = len(word.word)
        return word


def filter_for_center (to_filter: list[WordObj], letter: str) -> list[WordObj]:
    for word_object in to_filter:
        if letter not in word_object.word:
            to_filter.remove(word_object)
    return to_filter

def get_anagrams (word: str, potentials: list[str]):
    regex = f'^[{word}]+$'
    return [w for w in potentials if re.fullmatch(regex, w)]



def get_center (valid_words: list[WordObj], letters: list[str]):
    for l in letters:

        filtered_anagrams: list[WordObj] = filter_for_center(valid_words, l)
        if len(filtered_anagrams) > 0 and len(filtered_anagrams) < 60:
            print(f'found the perfect length, returning {l}')
            return l
    print(f'returning random letter')
    return random.choice(letters)

def get_isograms(word_list: list[WordObj], letter_list: list[str]) -> list[WordObj]:
    reg1 = f'(?=.*'
    reg2 = f')'
    reg3 = ''.join(letter_list)
    reg_constructor = ''.join([reg1 + l + reg2 for l in letter_list])

    regex = f'^{reg_constructor}[{reg3}]+$'
    isograms = [word for word in word_list if re.fullmatch(regex, word.word)]

    return isograms







