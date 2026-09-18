class SortingAlgorithms:

    @staticmethod
    def merge_sort(results):
        if len(results) <= 1:
            return results

        mid = len(results) // 2

        left = SortingAlgorithms.merge_sort(results[:mid])
        right = SortingAlgorithms.merge_sort(results[mid:])

        return SortingAlgorithms.merge(left, right)

    @staticmethod
    def merge(left, right):
        result = []

        i = 0
        j = 0

        while i < len(left) and j < len(right):

            # Higher score should come first
            if left[i][1] >= right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1

        while j < len(right):
            result.append(right[j])
            j += 1

        return result


if __name__ == "__main__":

    test_results = [
        (1, 0.25),
        (2, 0.80),
        (3, 0.45),
        (4, 0.10),
        (5, 0.65)
    ]

    print("BEFORE SORTING")
    print(test_results)

    sorted_results = SortingAlgorithms.merge_sort(test_results)

    print("\nAFTER MERGE SORT")
    print(sorted_results)


class SortingAlgorithms:

    @staticmethod
    def merge_sort(results):
        if len(results) <= 1:
            return results

        mid = len(results) // 2

        left = SortingAlgorithms.merge_sort(results[:mid])
        right = SortingAlgorithms.merge_sort(results[mid:])

        return SortingAlgorithms.merge(left, right)

    @staticmethod
    def merge(left, right):
        result = []

        i = 0
        j = 0

        while i < len(left) and j < len(right):

            if left[i][1] >= right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1

        while j < len(right):
            result.append(right[j])
            j += 1

        return result

    # ---------------- QUICK SORT ----------------

    @staticmethod
    def quick_sort(results):
        if len(results) <= 1:
            return results

        pivot = results[-1][1]

        higher = []
        equal = []
        lower = []

        for item in results:
            if item[1] > pivot:
                higher.append(item)
            elif item[1] == pivot:
                equal.append(item)
            else:
                lower.append(item)

        return (
            SortingAlgorithms.quick_sort(higher)
            + equal
            + SortingAlgorithms.quick_sort(lower)
        )


if __name__ == "__main__":

    test_results = [
        (1, 0.25),
        (2, 0.80),
        (3, 0.45),
        (4, 0.10),
        (5, 0.65)
    ]

    print("BEFORE SORTING")
    print(test_results)

    merge_sorted = SortingAlgorithms.merge_sort(test_results)

    print("\nAFTER MERGE SORT")
    print(merge_sorted)

    quick_sorted = SortingAlgorithms.quick_sort(test_results)

    print("\nAFTER QUICK SORT")
    print(quick_sorted)