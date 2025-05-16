import random
import re

class WordObj:
    word = ""
    points = 0
    pangram: False

    def __init__(self, word: str, points = 0, pangram = False):
        self.word = word
        self.points = points
        self.pangram = pangram


def calculate_word_points (word: str, pangrams_list: list):
    print(f'word is {word}')
    if len(word) < 5:
        to_return = WordObj(word, 2, False)
        return to_return
    elif pangrams_list.count(word) > 0:
        to_return = WordObj(word, len(word)  + 7, True)
        return to_return
    else:
        to_return = WordObj(word, len(word))
        return to_return


def filter_for_center (list: list, letter: str):
    to_return= []
    for word in list:
        if letter in word:
            to_return.append(word)
    return to_return


def generate_anagrams (word: str, potentials: list):
    regex = f'^[{word}]+$'
    return [w for w in potentials if re.fullmatch(regex, w)]



def get_center (valid_words: list, letters: str):
    for l in letters:

        filtered_anagrams: list = filter_for_center(valid_words, l)
        print(filtered_anagrams)
        if len(filtered_anagrams) > 20 and len(filtered_anagrams) < 50:
            print(f'found the perfect length, returning {l}')
            return l
    print(f'returning random letter')
    return random.choice(letters)

def get_pangrams(word_list: str, letter_list: list):
    reg1 = f'(?=.*'
    reg2 = f')'
    reg3 = ''.join(letter_list)
    reg_constructor = ''.join([reg1 + l + reg2 for l in letter_list])

    regex = f'^{reg_constructor}[{reg3}]+$'
    pangrams = [word for word in word_list if re.fullmatch(regex, word)]

    return pangrams




