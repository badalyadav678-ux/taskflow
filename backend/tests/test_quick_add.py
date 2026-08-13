from quick_add import parse_quick_add


def test_quick_add_high_priority():
    result = parse_quick_add(
    "Fix payment API, high priority",
    1
)

    assert result.title == "Fix payment API"
    assert result.priority == "high"


def test_quick_add_default_priority():
    result = parse_quick_add(
        "Update README",1
    )

    assert result.title == "Update README"
    assert result.priority == "medium"


def test_quick_add_tomorrow():
    result = parse_quick_add(
        "Deploy backend, high priority, due tomorrow",1
    )

    assert result.title == "Deploy backend"
    assert result.priority == "high"
    assert result.due_date is not None