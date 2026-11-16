import json

from wer import wer

reference_file = input("Еталонний текст (файл): ")
hypothesis_file = input("Текст для порівняння (файл): ")

with open(reference_file, encoding="utf-8") as f:
    reference_text = f.read()

with open(hypothesis_file, encoding="utf-8") as f:
    hypothesis_text = f.read()

result = wer(reference_text, hypothesis_text)
print(result)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("Результат збережено у result.json")