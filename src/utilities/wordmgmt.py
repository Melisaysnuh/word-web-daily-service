import random
import requests




def get_unique_letters(letter_array: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_array: list[str] = []
    for letter in letter_array:
        if letter not in seen:
            seen.add(letter)
            unique_array.append(letter)
    return unique_array

def filter_list_by_length(num1: int, num2: int):
    with open("words.txt", "r") as file:
        words = [line.strip() for line in file]
    return [word for word in words if len(word) >= num1 and len(word) <= num2]

def validate_word(word: str):
    url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
    key = 'c9d049a8-6724-4795-87f9-e091f2940fce'

    res = requests.get(f"{url}{word}?key={key}")
    data = res.json()

    if data and isinstance(data[0], dict):
        meta = data[0].get('meta', {})
        fl = data[0].get('fl', '')

        if not meta.get('offensive', False) and fl not in ['abbreviation', 'Latin phrase', 'Spanish phrase']:
            return True
    return False




def get_random_isogram():
    try:
        long_list = filter_list_by_length(7,7)
        unique_letter_words = [word for word in long_list if len(set(word)) == len(word)]

        if not unique_letter_words:
            raise ValueError("No 7-letter isogram words found.")
        else:
            candidate = random.choice(unique_letter_words)
            result = validate_word(candidate);
            if result:
                return candidate
            else:
                remove_invalid_word(candidate);
                return None

    except Exception as e:
        print(f'Error in get_random_word: {e}')


def remove_invalid_word(word_to_remove: str):
    try:
        with open("words.txt", "r") as file:
            words = [line.strip() for line in file]

        new_words = [word for word in words if word.lower() != word_to_remove.lower()]

        with open("words.txt", 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_words))

    except Exception as error:
        print('Error removing word:', error)
        raise error

def return_validated_array(words: list[str]) -> list[str]:
    try:
        print(f'in v_a function...{len(words)}')
        valid_words: list[str] = []
        for item in words:
            is_valid = validate_word(item)
            if is_valid:
                valid_words.append(item)
        return valid_words
    except Exception as error:
        print(f"Error in return_validated_array: {error}");
        raise error