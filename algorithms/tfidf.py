import math
from collections import Counter

from algorithms.preprocessing import tokenize


class TFIDFRanker:

    def __init__(self, documents, inverted_index):
        self.documents = documents
        self.index = inverted_index
        self.N = len(documents)

        self.document_lengths = {}
        self.term_frequencies = {}

        self._prepare_documents()

    def _prepare_documents(self):

        for document in self.documents:

            doc_id = document["id"]

            text = document["title"] + " " + document["content"]

            tokens = tokenize(text)

            self.document_lengths[doc_id] = len(tokens)

            self.term_frequencies[doc_id] = Counter(tokens)

    def calculate_tf(self, term, doc_id):

        count = self.term_frequencies[doc_id].get(term, 0)

        total_terms = self.document_lengths[doc_id]

        if total_terms == 0:
            return 0

        return count / total_terms

    def calculate_idf(self, term):

        posting_list = self.index.search_term(term)

        df = len(posting_list)

        if df == 0:
            return 0

        return math.log(self.N / df)

    def calculate_score(self, query_terms, doc_id):

        score = 0

        for query_term in query_terms:

            matched_terms = self.index.search_prefix(query_term)

            for term in matched_terms:

                tf = self.calculate_tf(term, doc_id)

                idf = self.calculate_idf(term)

                score += tf * idf

        return score
    