import random
import re
from pydantic import BaseModel




class WordObj(BaseModel):
    word: str
    points: int = 0
    isogram: bool = False



def calculate_word_points (word: str, isograms_list: list[str]):
    print(f'word is {word}')
    if len(word) < 5:
        to_return = WordObj(word=word, points=2, isogram=False)
        return to_return
    elif isograms_list.count(word) > 0:
        to_return = WordObj(word=word, points=len(word)  + 7, isogram=True)
        return to_return
    else:
        to_return = WordObj(word=word, points=len(word))
        return to_return


def filter_for_center (to_filter: list[str], letter: str) -> list[str]:
    to_return: list[str] = list()
    for word in to_filter:
        if letter in word:
            to_return.append(word)
    return to_return

def get_anagrams (word: str, potentials: list[str]):
    regex = f'^[{word}]+$'
    return [w for w in potentials if re.fullmatch(regex, w)]



def get_center (valid_words: list[str], letters: list[str]):
    for l in letters:

        filtered_anagrams: list[str] = filter_for_center(valid_words, l)
        print(filtered_anagrams)
        if len(filtered_anagrams) > 20 and len(filtered_anagrams) < 50:
            print(f'found the perfect length, returning {l}')
            return l
    print(f'returning random letter')
    return random.choice(letters)

def get_isograms(word_list: list[str], letter_list: list[str]) -> list[str]:
    reg1 = f'(?=.*'
    reg2 = f')'
    reg3 = ''.join(letter_list)
    reg_constructor = ''.join([reg1 + l + reg2 for l in letter_list])

    regex = f'^{reg_constructor}[{reg3}]+$'
    isograms = [word for word in word_list if re.fullmatch(regex, word)]

    return isograms







