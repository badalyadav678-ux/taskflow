import re
from datetime import date, timedelta

from schemas import QuickAddTask


def parse_quick_add(
    text: str,
    project_id: int
) -> QuickAddTask:
    text = text.strip()

    if not text:
        raise ValueError("Quick-add text cannot be empty")

    priority = "medium"

    if "high priority" in text.lower():
        priority = "high"

    elif "low priority" in text.lower():
        priority = "low"

    title = text

    title = re.sub(
        r",?\s*high priority",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = re.sub(
        r",?\s*low priority",
        "",
        title,
        flags=re.IGNORECASE
    )

    due_date = None

    if "tomorrow" in text.lower():
        due_date = str(date.today() + timedelta(days=1))

        title = re.sub(
            r",?\s*due tomorrow",
            "",
            title,
            flags=re.IGNORECASE
        )

    elif "today" in text.lower():
        due_date = str(date.today())

        title = re.sub(
            r",?\s*due today",
            "",
            title,
            flags=re.IGNORECASE
        )

    title = title.strip(" ,.")

    return QuickAddTask(
        title=title,
        description=None,
        priority=priority,
        due_date=due_date,
        project_id=project_id
    )