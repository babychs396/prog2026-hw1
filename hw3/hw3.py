# random.random() повертає випадкове дробове число від 0 до 1. 
# random.randint(значення1, значення2) повертає випадкове ціле число від одного значення до другого включно з межами. 
# random.choice([значення1, значення2, значення3]) повертає випадковий елемент будь-якого типу зі списку.

#1
import random

group: list[str] = [
    "Андрій",
    "Богдана",
    "Вікторія",
    "Дмитро",
    "Ірина",
    "Максим",
    "Олена",
    "Софія",
    "Тарас",
    "Юлія",
]

for attempt in range(1, 6):
    student = random.choice(group)
    print(f"Спроба {attempt}: {student}")

#2
import random

group: list[str] = [
    "Андрій",
    "Богдана",
    "Вікторія",
    "Дмитро",
    "Ірина",
    "Максим",
    "Олена",
    "Софія",
    "Тарас",
    "Юлія",
]

selected = random.sample(group, k=3)
print(selected)

#3
import random


def flip_coin() -> str:
    return random.choice(["Орел", "Решка"])


def count_flips(*, times: int) -> dict[str, int]:
    counts = {"Орел": 0, "Решка": 0}

    for _ in range(times):
        counts[flip_coin()] += 1

    return counts


print("Результат підкидання:", flip_coin())

for times in [100, 1000]:
    counts = count_flips(times=times)
    print(f"Підкидань: {times}")

    for side, count in counts.items():
        print(f"  {side}: {count} ({count / times * 100:.1f}%)")