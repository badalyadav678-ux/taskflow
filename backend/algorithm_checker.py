from algorithms import (
    insertion_sort,
    linear_search,
    binary_search,
    insertion_sort_count,
    linear_search_count,
    binary_search_count,
)


def check(name, condition):
    if condition:
        print(f"{name} -> PASS")
    else:
        print(f"{name} -> FAIL")


# -----------------------------
# Insertion Sort Tests
# -----------------------------

result = insertion_sort(
    [],
    lambda number: number
)

check(
    "Insertion sort - empty list",
    result == []
)


result = insertion_sort(
    [5],
    lambda number: number
)

check(
    "Insertion sort - single item",
    result == [5]
)


result = insertion_sort(
    [5, 2, 4, 1, 3],
    lambda number: number
)

check(
    "Insertion sort - normal list",
    result == [1, 2, 3, 4, 5]
)


# -----------------------------
# Linear Search Tests
# -----------------------------

result = linear_search(
    [10, 20, 30, 40, 50],
    10,
    lambda number: number
)

check(
    "Linear search - first item",
    result == 10
)


result = linear_search(
    [10, 20, 30, 40, 50],
    50,
    lambda number: number
)

check(
    "Linear search - last item",
    result == 50
)


result = linear_search(
    [10, 20, 30, 40, 50],
    30,
    lambda number: number
)

check(
    "Linear search - middle item",
    result == 30
)


result = linear_search(
    [10, 20, 30, 40, 50],
    100,
    lambda number: number
)

check(
    "Linear search - missing item",
    result is None
)


# -----------------------------
# Binary Search Tests
# -----------------------------

numbers = [10, 20, 30, 40, 50]


result = binary_search(
    numbers,
    10,
    lambda number: number
)

check(
    "Binary search - first item",
    result == 10
)


result = binary_search(
    numbers,
    50,
    lambda number: number
)

check(
    "Binary search - last item",
    result == 50
)


result = binary_search(
    numbers,
    30,
    lambda number: number
)

check(
    "Binary search - middle item",
    result == 30
)


result = binary_search(
    numbers,
    100,
    lambda number: number
)

check(
    "Binary search - missing item",
    result is None
)


# -----------------------------
# Comparison Count Tests
# -----------------------------

result, comparisons = insertion_sort_count(
    [5, 2, 4, 1, 3],
    lambda number: number
)

check(
    "Insertion sort count",
    result == [1, 2, 3, 4, 5] and comparisons > 0
)


result, comparisons = linear_search_count(
    [10, 20, 30, 40, 50],
    30,
    lambda number: number
)

check(
    "Linear search count",
    result == 30 and comparisons > 0
)


result, comparisons = binary_search_count(
    [10, 20, 30, 40, 50],
    30,
    lambda number: number
)

check(
    "Binary search count",
    result == 30 and comparisons > 0
)