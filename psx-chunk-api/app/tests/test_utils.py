from app.utils.utils import jsonListToStringList, validateChunkType, validateInputType


def test_jsonListToStringList():
    assert jsonListToStringList([{"a": 1}, {"b": 2}]) == ['{"a": 1}', '{"b": 2}']

    assert jsonListToStringList([{"a": 1}, {"b": 2}, {"c": 3}]) == [
        '{"a": 1}',
        '{"b": 2}',
        '{"c": 3}',
    ]


def test_validateInputType():
    assert validateInputType("JSON") is True
    assert validateInputType("TEXT") is True
    assert validateInputType("INVALID") is False
    assert validateInputType("ANY") is False
    assert validateInputType("") is False


def test_validateChunkType():
    assert validateChunkType("OBJECT") is True
    assert validateChunkType("TOKENS") is True
    assert validateChunkType("INVALID") is False
    assert validateChunkType("ANY") is False
    assert validateChunkType("") is False
