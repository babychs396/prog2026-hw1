import pytest

from analyzer import read_text, count_words, make_frequency_dict, make_frequency_table

@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello world", 2),
        ("Мова єднає людей", 3),
        ("П'ять будь-яких слів", 3),
        ("Hello, world!!! 123", 2),
        ("Слово", 1),
        ("", 0),
        ("     ", 0),
    ],
)
def test_count_words(text, expected):
    assert count_words(text) == expected

def test_frequency_dict():
    result = make_frequency_dict("Мова – це код. Мова, МОВА!")
    assert result["мова"] == 3
    assert result["це"] == 1
    assert result["код"] == 1
    assert len(result) == 3

def test_frequency_dict_empty_text():
    assert len(make_frequency_dict("")) == 0

def test_frequency_table():
    frequencies = make_frequency_dict("кіт пес кіт кіт пес миша")
    table = make_frequency_table(frequencies)
    assert len(table) == 3
    assert table["слово"][0] == "кіт"
    assert table["кількість"][0] == 3

def test_read_text_missing_file():
    assert read_text("немає_такого_файлу.txt") is None
