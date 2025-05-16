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


