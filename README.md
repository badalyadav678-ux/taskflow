Quick Add — Worked Examples

The Quick Add parser accepts a plain-text task description and converts it into structured task fields.

Example 1 — High Priority

Input:

Fix payment API, high priority

Parsed output:

{
  "title": "Fix payment API",
  "description": null,
  "priority": "high",
  "due_date": null,
  "project_id": 1
}
Example 2 — Low Priority

Input:

Update documentation, low priority

Parsed output:

{
  "title": "Update documentation",
  "description": null,
  "priority": "low",
  "due_date": null,
  "project_id": 1
}
Example 3 — Tomorrow

Input:

Fix dashboard bug, due tomorrow

Parsed output:

{
  "title": "Fix dashboard bug",
  "description": null,
  "priority": "medium",
  "due_date": "YYYY-MM-DD",
  "project_id": 1
}

YYYY-MM-DD represents the date for tomorrow when the parser is executed.

Example 4 — Today + High Priority

Input:

Deploy payment fix, high priority, due today

Parsed output:

{
  "title": "Deploy payment fix",
  "description": null,
  "priority": "high",
  "due_date": "YYYY-MM-DD",
  "project_id": 1
}

YYYY-MM-DD represents today's date when the parser is executed.

Example 5 — Normal Task

Input:

Review project documentation

Parsed output:

{
  "title": "Review project documentation",
  "description": null,
  "priority": "medium",
  "due_date": null,
  "project_id": 1
}

These examples demonstrate the supported Quick Add rules for priority detection, due-date detection, title cleanup, and the default medium priority.