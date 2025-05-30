
from unittest.mock import mock_open, patch

from utilities.wordmgmt import remove_invalid_word

def test_remove_invalid_word_case_insensitive():
    # Initial file content
    fake_file_content = "Apple\nBanana\nCherry\nDate\n"

    # Expected content after removing "banana" (case-insensitive)
    expected_written_content = "Apple\nCherry\nDate"

    m = mock_open(read_data=fake_file_content)

    with patch("builtins.open", m):
        remove_invalid_word("banana")

    # Check that open() was called first for reading, then for writing
    m.assert_any_call("words.txt", "r")
    m.assert_any_call("words.txt", "w", encoding="utf-8")

    # Get the file handle used for writing
    handle = m()
    handle.write.assert_called_once_with(expected_written_content)
