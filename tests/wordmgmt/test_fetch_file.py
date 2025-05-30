from unittest.mock import mock_open, patch

from utilities.wordmgmt import fetch_list

def test_fetch_list_with_sample_words():
    fake_file_content = "\n".join([
        "apple",
        "banana",
        "cherry",
        "date",
        "elderberry",
        "fig",
        "grape",
        "honeydew",
        "kiwi",
        "lemon",
        "mango",
        "nectarine",
        "orange",
        "papaya",
        "quince",
        "raspberry",
        "strawberry",
        "tangerine",
        "ugli",
        "voavanga"
    ]) + "\n"  # final newline to mimic real file

    expected_words = [
        "apple", "banana", "cherry", "date", "elderberry",
        "fig", "grape", "honeydew", "kiwi", "lemon",
        "mango", "nectarine", "orange", "papaya", "quince",
        "raspberry", "strawberry", "tangerine", "ugli", "voavanga"
    ]

    with patch("builtins.open", mock_open(read_data=fake_file_content)):
        result = fetch_list()

    assert result == expected_words
