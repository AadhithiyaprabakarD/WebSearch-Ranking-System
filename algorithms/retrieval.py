class RetrievalAlgorithms:

    @staticmethod
    def naive_intersection(list_a, list_b):
        """
        Find common document IDs using nested loops.

        Complexity:
        O(n * m)
        """

        result = []

        for doc_a, tf_a in list_a:
            for doc_b, tf_b in list_b:

                if doc_a == doc_b:
                    result.append(
                        (doc_a, tf_a, tf_b)
                    )

        return result

    @staticmethod
    def two_pointer_intersection(list_a, list_b):
        """
        Find common document IDs using two-pointer traversal.

        The posting lists must be sorted by document ID.

        Complexity:
        O(n + m)
        """

        result = []

        i = 0
        j = 0

        while i < len(list_a) and j < len(list_b):

            doc_a, tf_a = list_a[i]
            doc_b, tf_b = list_b[j]

            if doc_a == doc_b:

                result.append(
                    (doc_a, tf_a, tf_b)
                )

                i += 1
                j += 1

            elif doc_a < doc_b:

                i += 1

            else:

                j += 1

        return result


if __name__ == "__main__":

    import json
    import os

    from inverted_index import InvertedIndex
    from preprocessing import tokenize

    # Find project root
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    data_path = os.path.join(
        project_root,
        "data",
        "documents.json"
    )

    # Load documents
    with open(
        data_path,
        "r",
        encoding="utf-8"
    ) as file:

        documents = json.load(file)

    # Build inverted index
    index = InvertedIndex()
    index.build(documents)

    # User query
    query = "machine learning"

    # Preprocess query
    query_terms = tokenize(query)

    print("Query:", query)
    print("Processed query:", query_terms)

    # Retrieve posting lists
    first_term = query_terms[0]
    second_term = query_terms[1]

    list_a = index.search_term(first_term)
    list_b = index.search_term(second_term)

    print("\nPosting list:", first_term)
    print(list_a)

    print("\nPosting list:", second_term)
    print(list_b)

    # Two-pointer intersection
    results = RetrievalAlgorithms.two_pointer_intersection(
        list_a,
        list_b
    )

    print("\nDocuments matching BOTH terms:")
    print(results)