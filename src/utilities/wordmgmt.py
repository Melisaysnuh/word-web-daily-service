import asyncio
import os
import random
from typing import Any, Dict
import requests
from dotenv import load_dotenv

from utilities.custom_types import Definition, Hwi, Meta, WordObj, DictionaryResponse
load_dotenv()

from utilities.sandbox import invalid

def fetch_list():
    with open("words.txt", "r") as file:
        words = [line.strip() for line in file]
        return words


def filter_list_by_length(words: list[str], num1: int, num2: int):
    return [word for word in words if len(word) >= num1 and len(word) <= num2]

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
                remove_invalid_word(candidate)
                return None

    except Exception as e:
        print(f'[get_random_isogram] Exception: {e}')


def get_unique_letters(letter_array: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_array: list[str] = []
    for letter in letter_array:
        if letter not in seen:
            seen.add(letter)
            unique_array.append(letter)
    return unique_array



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
            parsed = parse_dictionary_response(data) # type: ignore
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

def parse_dictionary_response(data: Dict[str, Any]) -> DictionaryResponse:
    meta = Meta(
        id=data['meta']['id'],
        uuid=data['meta']['uuid'],
        sort=int(data['meta']['sort']),
        src=data['meta']['src'],
        section=data['meta']['section'],
        stems=data['meta']['stems'],
        offensive=data['meta']['offensive']
    )
    hwi = Hwi(hw=data['hwi']['hw'])
    shortdef = data.get('shortdef', [])
    date = data.get('date', '')

    # Extract nested definition text
    definitions: list[Definition] = []
    for def_block in data.get('def', []):
        for sseq_group in def_block.get('sseq', []):
            for sense_group in sseq_group:
                if sense_group[0] == 'sense':
                    sense_data = sense_group[1]
                    for dt_entry in sense_data.get('dt', []):
                        if dt_entry[0] == 'text':
                            text = dt_entry[1].replace('{bc}', '').strip()
                            definitions.append(Definition(text=text))

    fl: str = data.get('fl')
    if not fl:
        cxs = data.get('cxs')
        print(f"[parsing_dictionary_response] cxs is {cxs}")
        if cxs and isinstance(cxs, list):
            fl = ', '.join(cxs) # type: ignore
        else:
            fl = 'unknown'

    return DictionaryResponse(
        meta=meta,
        hwi=hwi,
        fl = fl,
        shortdef=shortdef,
        date=date,
        definitions=definitions
    )



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
                valid_words.append(is_valid)
        return valid_words
    except Exception as error:
        print(f"[return_validated_array] Error: {error}");
        raise error

async def main():
    test = return_validated_array(invalid)
    print(test)

if __name__ == "__main__":
    asyncio.run(main())