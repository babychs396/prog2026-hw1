import re
from collections import Counter
import pymorphy3

remove_rules = [
    (r"(?<!\bком)(?<=[бвгґджзклмнпстфхцчшщ])([бпвмф])’(?!я[зжлкн])(?=[яюєї])", r"\1",
     "Вилучено апостроф: перед губним інший приголосний"),
    (r"(\b|[бвгдзкптфхцчш])(р)’(?=[яюєї])", r"\1\2",
     "Вилучено апостроф після м’якого р"),
    (r"(бур)’(?=як)", r"\1",
     "Вилучено апостроф у слові буряк"),
]

add_rules = [
    (r"\b(?!зят|зяб|надя)(з|роз|без|від|під|над|об|між|перед|напів|двох)(?=[яюєї])", r"\1’",
     "Апостроф після префікса"),
    (r"(\b|[аеєиіїоуюяр])([бпвмф])(?!юро|юре|юзикл|юджет|юст)(?=[яюєї])", r"\1\2’",
     "Апостроф після губних б, п, в, м, ф"),
    (r"(?<!д)(з|під|с)([вмп])(?=я[зжлкн])", r"\1\2’",
     "Апостроф після префікса перед губним"),
    (r"([вз])(м)(?=ят)", r"\1\2’",
     "Апостроф після префікса перед губним"),
    (r"\b(комп|миш)(?=[яю])", r"\1’",
     "Апостроф в іншомовних словах"),
    (r"(\bбур|пір|двір|гір|\bмар|\bвалер|матір)(?=я(?!к)|ю)", r"\1’",
     "Апостроф після р"),
    (r"(?<=[аеиіоу])(р)(?=є)", r"\1’",
     "Апостроф після р перед є"),
    (r"\b(лук)(?=ян)", r"\1’",
     "Апостроф у слові Лук’ян"),
    (r"([бвгґджзклмнпрстфхцчшщ])(ї)", r"\1’\2",
     "Після приголосного ї пишемо з апострофом"),
]

rus_rules = [
    (r"(?<=[бпвмфр])[ьъ](?=[яюєї])", "’",
     "ь/ъ замість апострофа"),
    (r"\b(з|роз|без|від|під|над|об)[ьъ](?=[яюєї])", r"\1’",
     "ь/ъ замість апострофа після префікса"),
    (r"(р)ь(?!о)", r"\1",
     "Зайвий ь після р"),
    (r"(н)ь(?=[жчшщ]|ськ)", r"\1",
     "Зайвий ь після н"),
    (r"(сер|кур)ьоз", r"\1йоз",
     "ьо замість йо"),
    (r"(?<=[аеєиіїоуюя])ьо", "йо",
     "ьо замість йо після голосного"),
    (r"(?<=[аеєиіїоуюя])ё|\bё", "йо",
     "ё замість йо"),
    (r"ё", "ьо",
     "ё замість ьо"),
    (r"(буль|міль|баталь|павіль|медаль|кань)он", r"\1йон",
     "Пропущений й"),
]


def apply_rules(text, rules, change_log, rule_counter):
    total = 0
    for pattern, replacement, description in rules:
        text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
        if n > 0:
            change_log.append(f"- {description}: {n}")
            rule_counter[description] += n
            total += n
    return text, total


morph = pymorphy3.MorphAnalyzer(lang="uk")


def in_dictionary(word):
    for apostrophe in ["’", "'", "ʼ"]:
        if morph.word_is_known(word.replace("’", apostrophe)):
            return True
    return False


def check_dictionary(text, unified, change_log):
    unknown = []
    n_dict = 0
    for word in re.findall(r"[а-яієїґ]+’[а-яієїґ]+", text, flags=re.IGNORECASE):
        without = word.replace("’", "")
        with_soft = word.replace("’", "ь")
        if word not in text or in_dictionary(word.lower()):
            continue
        elif in_dictionary(without.lower()):
            text = text.replace(word, without)
            n_dict += 1
        elif in_dictionary(with_soft.lower()):
            text = text.replace(word, with_soft)
            n_dict += 1
        elif word not in unified:
            text = text.replace(word, without)
            unknown.append(without)
        else:
            unknown.append(word)
    if n_dict > 0:
        change_log.append(f"- Виправлено апостроф за словником: {n_dict}")
    if unknown:
        change_log.append(f"- Немає у словнику, перевірте вручну (позначено жовтим): {len(unknown)}")
    return text, unknown


def highlight(old_text, new_text, unknown):
    old_parts = re.split(r"(\s+)", old_text)
    new_parts = re.split(r"(\s+)", new_text)
    if len(old_parts) != len(new_parts):
        return [(new_text, None)]
    result = []
    for old, new in zip(old_parts, new_parts):
        label = None
        if old != new:
            label = "виправлено"
        for word in unknown:
            if word in new:
                label = "перевірте"
        result.append((new, label))
    return result


def check_apostrophes(text, check_rus=True):
    if not text or not text.strip():
        return "", [], "Введіть текст для аналізу.", ""
    if not re.search(r"[а-яієїґ]", text, flags=re.IGNORECASE):
        return "", [], "У тексті немає українських літер. Введіть український текст.", ""

    change_log = []
    rule_counter = Counter()

    text, n_symbols = re.subn(r"(?<=[а-яієїґ])['`ʼ‘´](?=[а-яієїґ])", "’", text, flags=re.IGNORECASE)
    if n_symbols > 0:
        change_log.append(f"- Уніфіковано символ апострофа: {n_symbols}")
    unified = text

    n_rus = 0
    if check_rus:
        text, n_rus = apply_rules(text, rus_rules, change_log, rule_counter)
    text, n_removed = apply_rules(text, remove_rules, change_log, rule_counter)
    text, n_added = apply_rules(text, add_rules, change_log, rule_counter)

    text, unknown = check_dictionary(text, unified, change_log)
    highlighted = highlight(unified, text, unknown)

    error_count = 0
    for part, label in highlighted:
        if label == "виправлено":
            error_count += 1

    words = re.findall(r"[а-яієїґ’]+", text.lower())
    total_words = max(1, len(words))
    error_percentage = (error_count / total_words) * 100
    penalty_factor = 2
    score = max(0, int(100 - (error_percentage * penalty_factor)))

    stats_report = "Результати аналізу\n\n"
    stats_report += f"**Оцінка тексту:** {score}/100\n\n"
    stats_report += f"**Виправлено слів:** {error_count}\n\n"
    stats_report += f"**Слів для ручної перевірки :** {len(unknown)}\n\n"
    if check_rus:
        stats_report += f"**Слідів російської орфографії:** {n_rus}\n\n"

    if change_log:
        log_report = "\n".join(change_log)
    else:
        log_report = "*Помилок не знайдено.*"

    return text, highlighted, stats_report, log_report


def process_file(file, check_rus=True):
    if file is None:
        return "", [], "Файл не завантажено.", ""
    if not file.name.lower().endswith(".txt"):
        return "", [], "Підтримуються лише файли .txt.", ""

    try:
        with open(file.name, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file.name, 'r', encoding='cp1251') as f:
            content = f.read()
    except Exception as e:
        return "", [], f"Помилка читання файлу: {e}", ""
    return check_apostrophes(content, check_rus)
