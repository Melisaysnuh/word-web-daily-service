from utilities.custom_types import WordObj
from utilities.wordmgmt import validate_word

def test_validate_word():


    response1 = validate_word('fortunate')
    assert response1
    assert isinstance(response1, WordObj)

    response2 = validate_word('Sherezade')
    assert response2 == None