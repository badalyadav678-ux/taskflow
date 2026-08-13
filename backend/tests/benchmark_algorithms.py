from algorithms import (
    insertion_sort_count,
    linear_search_count,
    binary_search_count,
)


def create_records(size):
    return [
        {
            "id": number,
            "title": f"Task {number}",
            "priority": "medium",
            "status": "pending",
        }
        for number in range(1, size + 1)
    ]


def benchmark(size):
    records = create_records(size)

    target = f"Task {size}"

    # -----------------------------
    # Insertion Sort
    # -----------------------------

    sorted_records, insertion_comparisons = insertion_sort_count(
        records,
        lambda record: record["title"]
    )

    # -----------------------------
    # Linear Search
    # -----------------------------

    linear_result, linear_comparisons = linear_search_count(
        records,
        target,
        lambda record: record["title"]
    )

    # -----------------------------
    # Binary Search
    # -----------------------------

    binary_result, binary_comparisons = binary_search_count(
        sorted_records,
        target,
        lambda record: record["title"]
    )

    print(f"\nDataset size: {size}")

    print(
        f"Insertion Sort | "
        f"Comparisons: {insertion_comparisons}"
    )

    print(
        f"Linear Search  | "
        f"Target: {target} | "
        f"Found: {linear_result is not None} | "
        f"Comparisons: {linear_comparisons}"
    )

    print(
        f"Binary Search  | "
        f"Target: {target} | "
        f"Found: {binary_result is not None} | "
        f"Comparisons: {binary_comparisons}"
    )


def main():
    dataset_sizes = [10, 500, 3000]

    for size in dataset_sizes:
        benchmark(size)


if __name__ == "__main__":
    main()