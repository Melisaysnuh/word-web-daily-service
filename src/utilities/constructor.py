
from utilities.custom_types import DayModel
from utilities.wordmgmt import get_random_isogram, filter_list_by_length, get_unique_letters, return_validated_array
from utilities.helpers import get_anagrams, get_center, get_isograms, filter_for_center,  calculate_word_points
from datetime import datetime
import asyncio


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

        # once we have anagrams, we gt the center and filter only anagrams containing center letter
            if valid_anagrams:
                center = get_center(valid_anagrams, unique_letter_array)
                print(f"center is {center}")
                if center:
                    print(f"[construct_day]: Center is {center} .")
                    valid_anagrams_with_center = filter_for_center(valid_anagrams, center)
                    todays_isograms = get_isograms(valid_anagrams_with_center, unique_letter_array)
                    for i, item in enumerate(valid_anagrams_with_center):
                        valid_anagrams_with_center[i] = calculate_word_points(item, todays_isograms)

                    for item in valid_anagrams_with_center:
                        item = calculate_word_points(item, todays_isograms)

                    print(f"[construct_day]: Returning {len(valid_anagrams_with_center)} words today.")

                    # now we will build our DayModel
                    return DayModel(
                        daylist_id=datetime.now().strftime("%Y_%m_%d"),
                        centerLetter=center,
                        isograms=todays_isograms,
                        letters=unique_letter_array,
                        validWords=valid_anagrams_with_center,
                        total_points = sum(w.points for w in valid_anagrams_with_center)
                    )

                else: print(f'Error, no center found')
                return None
            else: print(f'Error, no valid anagrams found')
            return None

    except Exception as e:
        print(f'Error in daylist constructor {e}')
        return None



async def main():
    test = await construct_day()
    print(test)

if __name__ == "__main__":
    asyncio.run(main())