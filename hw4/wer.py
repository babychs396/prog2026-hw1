import re

def get_words(text):
    return re.findall(r"[\w'’-]+", text.lower())

def wer(reference_text, hypothesis_text):
    reference_words = get_words(reference_text)
    hypothesis_words = get_words(hypothesis_text)

    table = []
    for i in range(len(reference_words) + 1):
        table.append([0] * (len(hypothesis_words) + 1))

    for i in range(len(reference_words) + 1):
        table[i][0] = i
    for j in range(len(hypothesis_words) + 1):
        table[0][j] = j

    for i in range(1, len(reference_words) + 1):
        for j in range(1, len(hypothesis_words) + 1):
            if reference_words[i - 1] == hypothesis_words[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = min(table[i - 1][j - 1], table[i - 1][j], table[i][j - 1]) + 1

    substitutions = 0
    deletions = 0
    insertions = 0
    i = len(reference_words)
    j = len(hypothesis_words)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and reference_words[i - 1] == hypothesis_words[j - 1]:
            i = i - 1
            j = j - 1
        elif i > 0 and j > 0 and table[i][j] == table[i - 1][j - 1] + 1:
            substitutions = substitutions + 1
            i = i - 1
            j = j - 1
        elif i > 0 and table[i][j] == table[i - 1][j] + 1:
            deletions = deletions + 1
            i = i - 1
        else:
            insertions = insertions + 1
            j = j - 1

    N = len(reference_words)

    return {
        "WER": (substitutions + deletions + insertions) / N,
        "S": substitutions,
        "D": deletions,
        "I": insertions,
        "N": N,
    }