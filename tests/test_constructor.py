import pytest
from unittest import mock
from utilities.custom_types import WordObj, DayModel
from utilities.constructor import construct_day

@pytest.mark.asyncio
async def test_construct_day_success():
    # Sample data for mocks
    fake_word_list = ["calorie", "loricae", "rocaille", "caller", "cellar"]
    fake_isogram = "calorie"
    fake_anagrams = ["calorie", "loricae", "rocaille", "caller"]
    fake_valid_anagrams = [
        WordObj(word="calorie", points=0, isogram=True),
        WordObj(word="loricae", points=0, isogram=True),
        WordObj(word="rocaille", points=10, isogram=True),
        WordObj(word="caller", points=0, isogram=False),
    ]
    fake_center = "c"
    fake_letters = ["c", "a", "l", "o", "r", "i", "e"]
    fake_filtered_anagrams = fake_valid_anagrams
    fake_isograms = [WordObj(word="calorie", points=0, isogram=True), WordObj(word="loricae", points=0, isogram=True)]

    # Patch all dependencies
    with mock.patch("utilities.constructor.fetch_list", return_value=fake_word_list), \
         mock.patch("utilities.constructor.filter_list_by_length", return_value=fake_word_list), \
         mock.patch("utilities.constructor.get_random_isogram", return_value=fake_isogram), \
         mock.patch("utilities.constructor.get_anagrams", return_value=fake_anagrams), \
         mock.patch("utilities.constructor.return_validated_array", return_value=fake_valid_anagrams), \
         mock.patch("utilities.constructor.get_center", return_value=fake_center), \
         mock.patch("utilities.constructor.get_unique_letters", return_value=fake_letters.copy()), \
         mock.patch("utilities.constructor.filter_for_center", return_value=fake_filtered_anagrams), \
         mock.patch("utilities.constructor.get_isograms", return_value=fake_isograms), \
         mock.patch("utilities.constructor.calculate_word_points", side_effect=lambda word, iso: word):

        result = await construct_day()

        # Assertions
        assert isinstance(result, DayModel)
        assert result.centerLetter == "c"
        assert result.letters[0] == "c"
        assert "a" in result.letters
        assert isinstance(result.validWords, list)
        assert all(isinstance(w, WordObj) for w in result.validWords)
        assert result.total_points == sum(w.points for w in result.validWords)
