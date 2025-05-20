
from index import DayModel
from utilities.wordmgmt import get_random_isogram, filter_list_by_length, get_unique_letters, return_validated_array
from utilities.utilities import get_anagrams, get_center, get_isograms, filter_for_center


async def construct_day() -> DayModel | None:
    try:
        #start by searching the word list for a random isogram. Our minimum length is 4, and for simplicity, max is 12.
        isogram: str | None = get_random_isogram()
        if isogram:
            main_list: list[str] = filter_list_by_length(4,12)

            letter_list: list[str]= isogram.split()
            unique_letter_array = get_unique_letters(letter_list)
        #we then use some logic + regex to get anagrams of the isogram, and validate them using Webster API
            anagrams = get_anagrams(isogram, main_list)
            valid_anagrams = return_validated_array(anagrams)

            if valid_anagrams:
                center = get_center(valid_anagrams, unique_letter_array)
                if center:
                    valid_anagrams_with_center = filter_for_center(valid_anagrams, center)

                    #now we want to check if there are any other isograms
                    todays_isograms = get_isograms(valid_anagrams_with_center, unique_letter_array)

                    # now we will build our DayModel
                    return DayModel(
                        daylist_id="fill this out",
                        center_letter=center,
                        isograms=todays_isograms,
                        letters=unique_letter_array,
                        valid_words={},
                        total_points=0
                    )

    except Exception as e:
        print(f'Error in daylist constructor {e}')