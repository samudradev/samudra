from samudra.tools.tokenizer import tokenize


def test_tokenize():
    TEXT = """
    Ini adalah konsep. #tag-1 #tag_2 {en:house}
    """
    response = tokenize(TEXT)
    assert response['text'] == ['Ini adalah konsep.']
    assert response['tag'] == ['#tag-1', '#tag_2']
    assert response['annotation'] == ['{en:house}']
