import os
import random
import requests
from dotenv import load_dotenv

from utilities.custom_types import WordObj
load_dotenv()




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

def validate_word(candidate: str) -> WordObj | None:
    try:
        url =  os.getenv('WEBSTER_URL')
        key = os.getenv('WEBSTER_API_KEY')

        res = requests.get(f"{url}{candidate}?key={key}")
        data = res.json()
        print(f"[validate_word] data is {data}")

        if not data or not isinstance(data[0], dict):
            print(f"[validate_word] '{candidate}' is not valid or only returned suggestions.")
            return

        shortdefs = data[0].get("shortdef", []) | new_data[0].get("shortdef", []) # type: ignore
        meta = data[0].get("meta", {})
        fl = data[0].get("fl", "")

        if not meta.get("offensive", False) and fl not in ['abbreviation', 'Latin phrase', 'Spanish phrase']:
            return WordObj(word=candidate, definition=shortdefs) # type: ignore

        return None

    except Exception as e:
        print(f"[validate_word] Error validating '{candidate}': {e}")
        return None


def get_random_isogram():
    try:
        long_list = filter_list_by_length(7,7)

        unique_letter_words = [word for word in long_list if len(set(word)) == len(word)]

        if not unique_letter_words:
            raise ValueError("[get_random_isogram] No 7-letter isogram words found.")
        else:
            candidate = random.choice(unique_letter_words)
            result = validate_word(candidate)
            if result:
                return candidate
            else:
                remove_invalid_word(candidate)
                return None

    except Exception as e:
        print(f'[get_random_isogram] Exception: {e}')


def remove_invalid_word(word_to_remove: str):
    try:
        with open("words.txt", "r") as file:
            words = [line.strip() for line in file]

        new_words = [word for word in words if word.lower() != word_to_remove.lower()]

        with open("words.txt", 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_words))

    except Exception as error:
        print('[remove_invalid_word] Error removing word:', error)
        raise error

def return_validated_array(words: list[str]) -> list[WordObj]:
    try:
        valid_words: list[WordObj] = []
        for item in words:
            is_valid = validate_word(item)
            if is_valid:
                valid_words.append(is_valid)
        return valid_words
    except Exception as error:
        print(f"[return_validated_array] Error: {error}");
        raise error

test = validate_word('retiree')
print(test)