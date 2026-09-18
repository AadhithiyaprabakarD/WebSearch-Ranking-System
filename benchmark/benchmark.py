import sys
import os
import time
import random
import string

# Allow imports from the project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)

from algorithms.searching import SearchAlgorithms


def generate_terms(size):
    """Generate a sorted vocabulary of unique terms."""

    terms = set()

    while len(terms) < size:
        term = "".join(
            random.choices(
                string.ascii_lowercase,
                k=8
            )
        )
        terms.add(term)

    return sorted(terms)


def benchmark_search_algorithms():

    vocabulary_size = 10000

    terms = generate_terms(vocabulary_size)

    # Dictionary used for hash-based lookup
    term_index = {
        term: position
        for position, term in enumerate(terms)
    }

    # Choose a term near the end so linear search
    # has to inspect many elements
    target = terms[-1]

    trials = 1000

    print("\nSEARCH ALGORITHM BENCHMARK")
    print("=" * 55)
    print("Vocabulary size:", vocabulary_size)
    print("Trials:", trials)
    print("Target:", target)

    # ---------------- LINEAR SEARCH ----------------

    start = time.perf_counter()

    for _ in range(trials):
        SearchAlgorithms.linear_search(
            terms,
            target
        )

    linear_time = time.perf_counter() - start

    # ---------------- BINARY SEARCH ----------------

    start = time.perf_counter()

    for _ in range(trials):
        SearchAlgorithms.binary_search(
            terms,
            target
        )

    binary_time = time.perf_counter() - start

    # ---------------- HASH SEARCH ----------------

    start = time.perf_counter()

    for _ in range(trials):
        SearchAlgorithms.hash_search(
            term_index,
            target
        )

    hash_time = time.perf_counter() - start

    # ---------------- RESULTS ----------------

    print("\nAVERAGE TIME PER SEARCH")
    print("-" * 55)

    print(
        f"Linear Search : "
        f"{(linear_time / trials) * 1_000_000:.4f} microseconds"
    )

    print(
        f"Binary Search : "
        f"{(binary_time / trials) * 1_000_000:.4f} microseconds"
    )

    print(
        f"Hash Search   : "
        f"{(hash_time / trials) * 1_000_000:.4f} microseconds"
    )

    return {
        "labels": ["Linear Search", "Binary Search", "Hash Search"],
        "values": [
            (linear_time / trials) * 1_000_000,
            (binary_time / trials) * 1_000_000,
            (hash_time / trials) * 1_000_000
        ],
        "vocabulary_size": vocabulary_size,
        "trials": trials
    }



def benchmark_retrieval_algorithms():

    # Simulated sorted posting lists
    list_a = [
        (i, 1)
        for i in range(0, 10000, 2)
    ]

    list_b = [
        (i, 1)
        for i in range(1, 10000, 2)
    ]

    trials = 100

    print("\n\nRETRIEVAL ALGORITHM BENCHMARK")
    print("=" * 55)
    print("Posting list A size:", len(list_a))
    print("Posting list B size:", len(list_b))
    print("Trials:", trials)

    # Import retrieval algorithms
    from algorithms.retrieval import RetrievalAlgorithms

    # ---------------- NAIVE INTERSECTION ----------------

    start = time.perf_counter()

    for _ in range(trials):
        RetrievalAlgorithms.naive_intersection(
            list_a,
            list_b
        )

    naive_time = time.perf_counter() - start

    # ---------------- TWO-POINTER INTERSECTION ----------------

    start = time.perf_counter()

    for _ in range(trials):
        RetrievalAlgorithms.two_pointer_intersection(
            list_a,
            list_b
        )

    two_pointer_time = time.perf_counter() - start

    # ---------------- RESULTS ----------------

    print("\nAVERAGE TIME PER INTERSECTION")
    print("-" * 55)

    print(
        f"Naive Intersection : "
        f"{(naive_time / trials) * 1_000_000:.4f} microseconds"
    )

    print(
        f"Two-Pointer        : "
        f"{(two_pointer_time / trials) * 1_000_000:.4f} microseconds"
    )

    print("\nCOMPLEXITY")
    print("-" * 55)
    print("Naive Intersection : O(n × m)")
    print("Two-Pointer        : O(n + m)")

    return {
        "labels": ["Naive Intersection", "Two-Pointer"],
        "values": [
            (naive_time / trials) * 1_000_000,
            (two_pointer_time / trials) * 1_000_000
        ],
        "list_size": len(list_a),
        "trials": trials
    }

def benchmark_ranking_algorithms():

    from algorithms.sorting import SortingAlgorithms
    from algorithms.min_heap import MinHeapTopK

    # Simulate 10,000 scored search results
    results = [
        (i, random.random())
        for i in range(10000)
    ]

    trials = 20
    k = 10

    print("\n\nRANKING ALGORITHM BENCHMARK")
    print("=" * 55)
    print("Number of results:", len(results))
    print("Top-K:", k)
    print("Trials:", trials)

    # ---------------- MERGE SORT ----------------

    start = time.perf_counter()

    for _ in range(trials):
        SortingAlgorithms.merge_sort(results)

    merge_time = time.perf_counter() - start

    # ---------------- QUICK SORT ----------------

    start = time.perf_counter()

    for _ in range(trials):
        SortingAlgorithms.quick_sort(results)

    quick_time = time.perf_counter() - start

    # ---------------- MIN-HEAP ----------------

    start = time.perf_counter()

    for _ in range(trials):

        heap = MinHeapTopK(k)

        for result in results:
            heap.push(result)

        heap.get_top_k()

    heap_time = time.perf_counter() - start

    # ---------------- RESULTS ----------------

    print("\nAVERAGE TIME PER RANKING")
    print("-" * 55)

    print(
        f"Merge Sort : "
        f"{(merge_time / trials) * 1_000_000:.4f} microseconds"
    )

    print(
        f"Quick Sort : "
        f"{(quick_time / trials) * 1_000_000:.4f} microseconds"
    )

    print(
        f"Min-Heap   : "
        f"{(heap_time / trials) * 1_000_000:.4f} microseconds"
    )

    print("\nCOMPLEXITY")
    print("-" * 55)
    print("Merge Sort : O(R log R)")
    print("Quick Sort : O(R log R) average, O(R²) worst")
    print("Min-Heap   : O(R log K)")

    return {
        "labels": ["Merge Sort", "Quick Sort", "Min-Heap"],
        "values": [
            (merge_time / trials) * 1_000_000,
            (quick_time / trials) * 1_000_000,
            (heap_time / trials) * 1_000_000
        ],
        "results": len(results),
        "top_k": k,
        "trials": trials
    }
    
if __name__ == "__main__":
    benchmark_search_algorithms()
    benchmark_retrieval_algorithms()
    benchmark_ranking_algorithms()

    