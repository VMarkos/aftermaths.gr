import re

def counts(filename):
    with open(filename, "r") as file:
        data = file.read()
    lines = list(filter(lambda x : x not in ["", " "], data.split("\n")))
    n_lines = len(lines)
    words = re.split("\s+|^\w", data)
    n_words = len(words)
    n_chars = 0
    for word in words:
        n_chars += len(word)
    return {
        "lines": n_lines,
        "words": n_words,
        "characters": n_chars,
    }