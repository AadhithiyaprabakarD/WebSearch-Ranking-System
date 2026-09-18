class MinHeapTopK:

    def __init__(self, k):
        self.k = k
        self.heap = []

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.heap[parent][1] <= self.heap[index][1]:
                break

            self.heap[parent], self.heap[index] = (
                self.heap[index],
                self.heap[parent]
            )

            index = parent

    def _heapify_down(self, index):
        size = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if (
                left < size
                and self.heap[left][1] < self.heap[smallest][1]
            ):
                smallest = left

            if (
                right < size
                and self.heap[right][1] < self.heap[smallest][1]
            ):
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = (
                self.heap[smallest],
                self.heap[index]
            )

            index = smallest

    def push(self, item):

        if self.k <= 0:
            return

        if len(self.heap) < self.k:
            self.heap.append(item)
            self._heapify_up(len(self.heap) - 1)

        elif item[1] > self.heap[0][1]:
            self.heap[0] = item
            self._heapify_down(0)

    def get_top_k(self):
        return sorted(
            self.heap,
            key=lambda item: item[1],
            reverse=True
        )


if __name__ == "__main__":

    results = [
        (1, 0.25),
        (2, 0.80),
        (3, 0.45),
        (4, 0.10),
        (5, 0.65)
    ]

    k = 3

    top_k = MinHeapTopK(k)

    for result in results:
        top_k.push(result)

    print("ALL RESULTS")
    print(results)

    print("\nTOP", k, "RESULTS")
    print(top_k.get_top_k())