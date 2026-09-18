from collections import defaultdict, Counter
from bisect import bisect_left

from algorithms.preprocessing import tokenize


class InvertedIndex:

    def __init__(self):
        self.index = defaultdict(list)
        self.document_count = 0
        self.sorted_terms = []

    def build(self, documents):
        self.document_count = len(documents)

        for document in documents:
            doc_id = document["id"]

            text = document["title"] + " " + document["content"]
            tokens = tokenize(text)

            term_frequency = Counter(tokens)

            for term, frequency in term_frequency.items():
                self.index[term].append((doc_id, frequency))

        # Keep posting lists sorted by document ID
        for term in self.index:
            self.index[term].sort(key=lambda item: item[0])

        # Sorted vocabulary is useful for prefix searching
        self.sorted_terms = sorted(self.index.keys())

    def search_term(self, term):
        term = term.lower()
        return self.index.get(term, [])

    def search_prefix(self, prefix):
        """
        Find all vocabulary terms that start with the given prefix.

        Example:
            prefix = "net"

        could return:
            ["network", "networks"]
        """

        prefix = prefix.lower().strip()

        if not prefix:
            return []

        # Find the first possible position using binary search
        start = bisect_left(self.sorted_terms, prefix)

        matching_terms = []

        # Scan forward only while terms have the requested prefix
        for i in range(start, len(self.sorted_terms)):
            term = self.sorted_terms[i]

            if term.startswith(prefix):
                matching_terms.append(term)
            else:
                # Once alphabetical ordering moves beyond the prefix,
                # no later terms can match.
                if term > prefix:
                    break

        return matching_terms

    def vocabulary_size(self):
        return len(self.index)


if __name__ == "__main__":

    import json
    import os

    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    data_path = os.path.join(
        project_root,
        "data",
        "documents.json"
    )

    with open(data_path, "r", encoding="utf-8") as file:
        documents = json.load(file)

    inverted_index = InvertedIndex()
    inverted_index.build(documents)

    print("Documents indexed:", inverted_index.document_count)
    print("Unique terms:", inverted_index.vocabulary_size())

    print("\nPrefix search tests:")

    for prefix in ["ne", "neur", "net", "learn"]:
        print(f"{prefix} -> {inverted_index.search_prefix(prefix)}")