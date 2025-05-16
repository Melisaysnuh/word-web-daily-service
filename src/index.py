import utilities
mock_letters = ['d', 'r', 'o', 'u', 'g', 'h', 't']

mock_words = 'dough', 'dour', 'drought', 'drug', 'good', 'door'

result = utilities.get_pangrams(mock_words, mock_letters)
print(result)
