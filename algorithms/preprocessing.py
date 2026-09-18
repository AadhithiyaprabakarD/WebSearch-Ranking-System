import re


# Common English stop words that do not contribute much
# to search relevance.
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "of", "to", "in", "on", "for", "and", "or",
    "with", "by", "from", "this", "that", "these",
    "those", "it", "as", "at", "be", "can"
}


def tokenize(text):
    """
    Convert text into normalized searchable terms.

    Steps:
    1. Convert text to lowercase.
    2. Extract alphabetic words.
    3. Remove stop words.
    """

    text = text.lower()

    words = re.findall(r"[a-z]+", text)

    tokens = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return tokens

if __name__ == "__main__":
    text = "Machine Learning is an exciting field of Artificial Intelligence!"

    print(tokenize(text))