import bisect
import time


class SearchAlgorithms:

    @staticmethod
    def linear_search(terms, target):
        """
        Search for a term using linear search.

        Time Complexity:
        O(V)
        """

        for index, term in enumerate(terms):
            if term == target:
                return index

        return -1

    @staticmethod
    def binary_search(terms, target):
        """
        Search for a term using binary search.

        The list must already be sorted.

        Time Complexity:
        O(log V)
        """

        left = 0
        right = len(terms) - 1

        while left <= right:

            mid = (left + right) // 2

            if terms[mid] == target:
                return mid

            elif terms[mid] < target:
                left = mid + 1

            else:
                right = mid - 1

        return -1

    @staticmethod
    def hash_search(index, target):
        """
        Search for a term using a hash table.

        Python's dictionary is used as the hash table.

        Average Time Complexity:
        O(1)
        """

        if target in index:
            return index[target]

        return None


def benchmark_search(terms, index, target):

    # Linear Search
    start = time.perf_counter()

    linear_result = SearchAlgorithms.linear_search(
        terms,
        target
    )

    linear_time = time.perf_counter() - start

    # Binary Search
    start = time.perf_counter()

    binary_result = SearchAlgorithms.binary_search(
        terms,
        target
    )

    binary_time = time.perf_counter() - start

    # Hash Search
    start = time.perf_counter()

    hash_result = SearchAlgorithms.hash_search(
        index,
        target
    )

    hash_time = time.perf_counter() - start

    print("\nSEARCH BENCHMARK")
    print("-" * 40)

    print(
        f"Linear Search : "
        f"{linear_time:.10f} seconds"
    )

    print(
        f"Binary Search : "
        f"{binary_time:.10f} seconds"
    )

    print(
        f"Hash Search   : "
        f"{hash_time:.10f} seconds"
    )

    print("\nRESULTS")
    print("-" * 40)

    print("Linear result:", linear_result)
    print("Binary result:", binary_result)
    print(
        "Hash result  :",
        "Found" if hash_result is not None else "Not Found"
    )


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

    with open(
        data_path,
        "r",
        encoding="utf-8"
    ) as file:

        documents = json.load(file)

    # Build vocabulary from the existing documents
    from algorithms.inverted_index import InvertedIndex

    inverted_index = InvertedIndex()
    inverted_index.build(documents)

    # Sorted vocabulary for binary search
    terms = sorted(inverted_index.index.keys())

    target = "machine"

    benchmark_search(
        terms,
        inverted_index.index,
        target
    )