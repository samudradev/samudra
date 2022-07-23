import pytest

from samudra.schemas import AnnotatedText


def test_annotated_text():
    text = "Ini adalah konsep cubaan #tag_1 #tag-2 {lang.en:concept} {lang.en:test} {meta.gol:NAMA}"
    post = AnnotatedText(body=text)
    assert post.content == "Ini adalah konsep cubaan"
    assert post.tags == ['tag 1', 'tag-2']
    assert post.fields['meta'] == {'gol': 'NAMA'}
    assert post.fields['lang'] == {'en': ['concept', 'test']}


def test_annotated_text_w_failure():
    text = "Ini adalah # konsep cubaan #tag_1 #tag-2 {lang.en:concept} {lang.en:test} {meta.gol:NAMA}"
    with pytest.raises(SyntaxError):
        AnnotatedText(body=text).tokenized
