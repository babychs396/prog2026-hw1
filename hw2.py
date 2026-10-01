from collections import Counter
import re
 
with open("text.txt", "rt", encoding="utf-8") as file:
    example = file.read()
 
 
def get_words(text: str) -> list:
    return re.findall(r"[^\W\d_]+(?:['’ʼ-][^\W\d_]+)*", text.lower())
 
def get_frequency_dict(text: str) -> dict:
    words = get_words(text)
    counted_words = Counter(words)
    total = len(words)
 
    frequency = {}
    for word, count in counted_words.most_common():
        frequency[word] = round(count / total * 100, 2)
    return frequency
 
def get_shortest_words(text: str) -> list:
    words = get_words(text)
    if not words:
        return []
 
    min_len = min(len(word) for word in words)
    shortest_words = []
    for word in words:
        if len(word) == min_len and word not in shortest_words:
            shortest_words.append(word)
    return shortest_words
 
def get_longest_words(text: str) -> list:
    words = get_words(text)
    if not words:
        return []
    
    max_len = max(len(word) for word in words)
    longest_words = []
    for word in words:
        if len(word) == max_len and word not in longest_words:
            longest_words.append(word)
    return longest_words
 
def count_unique_words(text: str) -> int:
    return len(set(get_words(text)))
 
def count_words(text: str) -> int:
    return len(get_words(text))
 
def get_used_letters(text: str) -> list:
    letters = re.findall(r"[^\W\d_]", text.lower())
    return sorted(set(letters))
 
def get_most_common_letter(text: str) -> str:
    letters = re.findall(r"[^\W\d_]", text.lower())
    counted_letters = Counter(letters)
    return counted_letters.most_common(1)[0][0]
 
print(f"Кількість слів: {count_words(example)}")
print(f"Кількість унікальних слів: {count_unique_words(example)}")
 
print("Частотний словник (перші 10 слів):")
frequency = get_frequency_dict(example)
for word in list(frequency)[:10]:
    print(f"{word}: {frequency[word]}%")
 
print(f"Найкоротші слова: {get_shortest_words(example)}")
print(f"Найдовші слова: {get_longest_words(example)}")
print(f"Використані літери: {get_used_letters(example)}")
print(f"Найчастіша літера: {get_most_common_letter(example)}")
