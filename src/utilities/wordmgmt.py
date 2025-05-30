import asyncio
import os
import random

import requests
from dotenv import load_dotenv


from utilities.helpers import filter_list_by_length
from utilities.parser import parse_dictionary_response
from utilities.custom_types import  WordObj
load_dotenv()

from utilities.sandbox import invalid

def fetch_list():
    with open("words.txt", "r") as file:
        words = [line.strip() for line in file]
        return words


def get_random_isogram(words: list[str]):
    try:
        long_list = filter_list_by_length(words, 7,7)

        unique_letter_words = [word for word in long_list if len(set(word)) == len(word)]

        if not unique_letter_words:
            raise ValueError("[get_random_isogram] No 7-letter isogram words found.")
        else:
            candidate = random.choice(unique_letter_words)
            result = validate_word(candidate)
            if result:
                return candidate
            else:
                unique_letter_words.remove(candidate)
                remove_invalid_word(candidate)
                get_random_isogram(unique_letter_words)
                raise ValueError("[get_random_isogram] No 7-letter isogram words found.")

    except Exception as e:
        print(f'[get_random_isogram] Exception: {e}')
        raise



def validate_word(candidate: str) -> WordObj | None:
    try:
        url =  os.getenv('WEBSTER_URL')
        key = os.getenv('WEBSTER_API_KEY')

        res = requests.get(f"{url}{candidate}?key={key}")
        if res.status_code != 200:
            print(f"Failed to fetch: {res.status_code}")
            return None
        data  = res.json()
        if isinstance(data, list):
            data = data[0] # type: ignore
        if not isinstance(data, str):
            parsed = parse_dictionary_response(data)  # type: ignore
            print(f"[validate_word] {candidate}'s fl is {parsed.fl}")

            if not parsed:
                print(f"[validate_word] word is not valid")
                return

            if not parsed.meta.offensive and parsed.fl and parsed.fl not in ['abbreviation', 'Latin phrase', 'Spanish phrase']:
                return WordObj(word=candidate, definition=parsed.shortdef)
        print(f"{candidate} not valid at end of [validate_word]")
        return None

    except Exception as e:
        print(f"[validate_word] Error validating '{candidate}': {e}")
        return None



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
    print(words)
    try:
        valid_words: list[WordObj] = []
        for item in words:
            is_valid = validate_word(item)
            if is_valid:
                valid_words.append(WordObj(word=item))
        return valid_words
    except Exception as error:
        print(f"[return_validated_array] Error: {error}");
        raise error

async def main():
    test = return_validated_array(invalid)
    print(test)

if __name__ == "__main__":
    asyncio.run(main())