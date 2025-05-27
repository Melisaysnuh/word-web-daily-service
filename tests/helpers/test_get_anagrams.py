from utilities.helpers import get_anagrams  # adjust as needed

def test_get_anagrams_basic():
    word = "stop"
    potentials = ["pots", "spot", "tops", "opts", "post", "stop", "psto", "hello", "top", "stopper"]
    expected = ["pots", "spot", "tops", "opts", "post", "stop", "psto", "top"]
    # "stopper" and "hello" contain letters outside 'stop' set and should be excluded

    result = get_anagrams(word, potentials)
    assert sorted(result) == sorted(expected)

def test_get_anagrams_empty_potentials():
    assert get_anagrams("word", []) == []

def test_get_anagrams_empty_word():
    assert get_anagrams("", ["a", ""]) == []

def test_get_anagrams_no_matches():
    assert get_anagrams("abc", ["def", "ghi"]) == []

def test_get_anagrams_case_sensitive():
    word = "Stop"
    potentials = ["pots", "Spot", "STOP"]
    expected = ["pots", "spot", "stop"]
    assert get_anagrams(word, potentials) == expected
