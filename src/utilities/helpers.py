import random
import re

from utilities.custom_types import WordObj



def filter_list_by_length(words: list[str], num1: int, num2: int):
    if (not num1 or not num2):
        return words
    return [word for word in words if len(word) >= num1 and len(word) <= num2]

def calculate_word_points (word: WordObj, isograms_list: list[WordObj]):

    if len(word.word) < 5:
        word.points = 2
        return word
    elif isograms_list.count(word) > 0:
        new_points=len(word.word) + 7
        word.points=new_points
        word.isogram=True
        print(f"points are: {word.points}")
        return word
    else:
        word.points = len(word.word)
        return word


def filter_for_center (to_filter: list[WordObj], letter: str) -> list[WordObj]:
    for word_object in to_filter:
        if letter not in word_object.word:
            to_filter.remove(word_object)
    return to_filter

def get_anagrams (word: str, potentials: list[str]) -> list[str]:
    if len(word) > 0 and len(potentials) > 0:
        low_word = word.lower()
        regex = f'^[{low_word}]+$'
        return [w.lower() for w in potentials if re.fullmatch(regex, w.lower())]
    else:
        return [] # type: ignore



def get_center (valid_words: list[WordObj], letters: list[str]):
    for l in letters:
        filtered_anagrams: list[WordObj] = filter_for_center(valid_words, l)
        if len(filtered_anagrams) > 0 and len(filtered_anagrams) < 60:
            print(f'found the perfect length, returning {l}')
            return l
    print(f'returning random letter')
    return random.choice(letters)

def get_unique_letters(letter_array: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_array: list[str] = []
    for letter in letter_array:
        if letter not in seen:
            seen.add(letter)
            unique_array.append(letter)
    return unique_array

def get_isograms(word_list: list[WordObj], letter_list: list[str]) -> list[WordObj]:
    first_letter = letter_list[0]
    allowed_letters = ''.join(letter_list)

    # * REGEX LOGIC
    # ? Should already be filtered for C, regex might be redundant
    # 1. (?=.*c) → must include at least one 'c'
    # 2. ^[calorie]+$ → only allowed letters
    regex = f'^(?=.*{first_letter})[{allowed_letters}]+$'
    print(f"regex is {regex}")

    isograms = [
        word for word in word_list
        if re.fullmatch(regex, word.word.lower())
    ]

    return isograms






