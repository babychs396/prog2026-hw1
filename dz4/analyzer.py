import pandas
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer


def read_text(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("Помилка: файл", file_name, "не знайдено.")
        return None
    except UnicodeDecodeError:
        print("Помилка: файл", file_name, "не в кодуванні UTF-8.")
        return None
    return text


def get_words(text):
    tokenizer = RegexpTokenizer(r"[a-zа-яіїєґ]+(?:['’-][a-zа-яіїєґ]+)*")
    words = tokenizer.tokenize(text.lower())
    return words


def count_words(text):
    words = get_words(text)
    return len(words)


def make_frequency_dict(text):
    words = get_words(text)
    frequencies = FreqDist(words)
    return frequencies


def make_frequency_table(frequencies):
    table = pandas.DataFrame(frequencies.most_common(), columns=["слово", "кількість"])
    return table


def main():
    file_name = "text.txt"
    text = read_text(file_name)

    if text is None:
        return

    if text.strip() == "":
        print("Файл порожній")
        return

    print("Кількість слів:", count_words(text))

    frequencies = make_frequency_dict(text)
    print("Кількість різних слів:", len(frequencies))

    table = make_frequency_table(frequencies)
    print("10 найуживаніших слів:")
    print(table.head(10))

    table.to_csv("frequencies.csv", index=False, encoding="utf-8-sig")
    print("Повна таблиця частотності збережена у файл frequencies.csv")

if __name__ == "__main__":
    main()