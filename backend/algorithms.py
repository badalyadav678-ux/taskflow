def insertion_sort(items, key_function):
    items = items.copy()

    for i in range(1, len(items)):
        current_item = items[i]
        j = i - 1

        while j >= 0 and key_function(items[j]) > key_function(current_item):
            items[j + 1] = items[j]
            j -= 1

        items[j + 1] = current_item

    return items


def linear_search(items, target, key_function):
    target = target.strip().lower()

    for item in items:
        value = key_function(item).strip().lower()

        if value == target:
            return item

    return None


def binary_search(items, target, key_function):
    left = 0
    right = len(items) - 1

    while left <= right:
        middle = (left + right) // 2

        value = key_function(items[middle])

        if value == target:
            return items[middle]

        if value < target:
            left = middle + 1
        else:
            right = middle - 1

    return None


def insertion_sort_count(items, key_function):
    items = items.copy()
    comparisons = 0

    for i in range(1, len(items)):
        current_item = items[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if key_function(items[j]) > key_function(current_item):
                items[j + 1] = items[j]
                j -= 1
            else:
                break

        items[j + 1] = current_item

    return items, comparisons


def linear_search_count(items, target, key_function):
    comparisons = 0

    for item in items:
        comparisons += 1

        if key_function(item) == target:
            return item, comparisons

    return None, comparisons


def binary_search_count(items, target, key_function):
    left = 0
    right = len(items) - 1
    comparisons = 0

    while left <= right:
        middle = (left + right) // 2

        value = key_function(items[middle])

        comparisons += 1

        if value == target:
            return items[middle], comparisons

        comparisons += 1

        if value < target:
            left = middle + 1
        else:
            right = middle - 1

    return None, comparisons