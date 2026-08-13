from algorithms import (
    insertion_sort,
    linear_search,
    binary_search,
    insertion_sort_count,
    linear_search_count,
    binary_search_count,
)



def test_insertion_sort():
    numbers = [5, 2, 4, 1, 3]

    result = insertion_sort(
        numbers,
        lambda number: number
    )

    assert result == [1, 2, 3, 4, 5]

def test_linear_search():
    numbers = [10, 20, 30, 40]

    result = linear_search(
        numbers,
        30,
        lambda number: number
    )

    assert result == 30

def test_binary_search():
    numbers = [10, 20, 30, 40, 50]

    result = binary_search(
        numbers,
        40,
        lambda number: number
    )

    assert result == 40

def test_linear_search_not_found():
    numbers = [10, 20, 30, 40]

    result = linear_search(
        numbers,
        100,
        lambda number: number
    )

    assert result is None

def test_binary_search_not_found():
    numbers = [10, 20, 30, 40]

    result = binary_search(
        numbers,
        100,
        lambda number: number
    )

    assert result is None


def test_insertion_sort_count():
    numbers = [5, 2, 4, 1, 3]

    result, comparisons = insertion_sort_count(
        numbers,
        lambda number: number
    )

    assert result == [1, 2, 3, 4, 5]
    assert comparisons > 0

def test_linear_search_count():
    numbers = [10, 20, 30, 40]

    result, comparisons = linear_search_count(
        numbers,
        30,
        lambda number: number
    )

    assert result == 30
    assert comparisons == 3

def test_binary_search_count():
    numbers = [10, 20, 30, 40, 50]

    result, comparisons = binary_search_count(
        numbers,
        40,
        lambda number: number
    )

    assert result == 40
    assert comparisons > 0