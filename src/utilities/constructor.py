
import asyncio

from pydantic import BaseModel

from wordmgmt import get_random_isogram, filter_list_by_length, get_unique_letters, return_validated_array
from helpers import get_anagrams, get_center, get_isograms, filter_for_center, WordObj, calculate_word_points
from datetime import datetime


class DayModel(BaseModel):
    daylist_id: str
    center_letter: str;
    isograms: list[str];
    total_points: int;
    letters: list[str];
    valid_words: list[WordObj];

async def construct_day() -> DayModel | None:
    try:
        #start by searching the word list for a random isogram. Our minimum length is 4, and for simplicity, max is 12.
        isogram: str | None = get_random_isogram()
        if isogram:
            main_list: list[str] = filter_list_by_length(4,12)

            letter_list: list[str] = list(isogram)
            unique_letter_array = get_unique_letters(letter_list)
            print(f"unique_letter_array is {unique_letter_array}")
        #we then use some logic + regex to get anagrams of the isogram, and validate them using Webster API
            anagrams = get_anagrams(isogram, main_list)
            valid_anagrams = return_validated_array(anagrams)

            if valid_anagrams:
                center = get_center(valid_anagrams, unique_letter_array)
                print(f"center is {center}")
                if center:
                    valid_anagrams_with_center = filter_for_center(valid_anagrams, center)

                    #now we want to check if there are any other isograms
                    todays_isograms = get_isograms(valid_anagrams_with_center, unique_letter_array)

                    valid_words_final: list[WordObj] = list(map(lambda word: calculate_word_points(word, todays_isograms), valid_anagrams_with_center))
                    print(valid_words_final)

                    # now we will build our DayModel
                    return DayModel(
                        daylist_id=datetime.now().strftime("%Y_%m_%d"),
                        center_letter=center,
                        isograms=todays_isograms,
                        letters=unique_letter_array,
                        valid_words=valid_words_final,
                        total_points = sum(w.points for w in valid_words_final)
                    )

                else: print(f'Error, no center found')
                return None
            else: print(f'Error, no valid anagrams found')
            return None

    except Exception as e:
        print(f'Error in daylist constructor {e}')
        return None

test = asyncio.run(construct_day())
print(test)
