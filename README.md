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

AI Quick-Add
Quick Add Examples

The Quick Add feature accepts a plain-text task description and converts it into a structured task.

Example 1 — High Priority

Input

Fix payment API, high priority

Parsed fields

{
  "title": "Fix payment API",
  "description": null,
  "priority": "high",
  "due_date": null,
  "project_id": 1
}
Example 2 — Low Priority

Input

Update project documentation, low priority

Parsed fields

{
  "title": "Update project documentation",
  "description": null,
  "priority": "low",
  "due_date": null,
  "project_id": 1
}
Example 3 — Due Tomorrow

Input

Fix dashboard bug, due tomorrow

Parsed fields

{
  "title": "Fix dashboard bug",
  "description": null,
  "priority": "medium",
  "due_date": "YYYY-MM-DD",
  "project_id": 1
}

YYYY-MM-DD represents the date calculated by the parser for tomorrow.

Example 4 — High Priority and Due Today

Input

Deploy payment fix, high priority, due today

Parsed fields

{
  "title": "Deploy payment fix",
  "description": null,
  "priority": "high",
  "due_date": "YYYY-MM-DD",
  "project_id": 1
}

YYYY-MM-DD represents the current date when the parser runs.

Example 5 — Normal Task

Input

Review project documentation

Parsed fields

{
  "title": "Review project documentation",
  "description": null,
  "priority": "medium",
  "due_date": null,
  "project_id": 1
}

Prompting Technique

The TaskFlow Quick-Add feature is modeled on a zero-shot prompting approach. The system instruction describes how a task description should be interpreted, including priority detection, due-date detection, and title extraction, without providing multiple examples that the model must imitate.

Zero-shot prompting is appropriate for this feature because each task description can be different and the desired output structure is clearly defined by the application's rules. It also uses fewer tokens than a few-shot approach because the prompt does not need to include several example inputs and outputs. Fewer prompt tokens can reduce processing cost and latency.

The deterministic mock parser follows the same structured idea without making an external API call. This makes the Quick-Add feature reliable and testable because the same input produces the same output every time, while the prompt structure provides a clear path for an optional real LLM implementation in the future.


API Endpoint Documentation

The TaskFlow backend is built with FastAPI and exposes REST endpoints for users, projects, tasks, statistics, algorithm-based sorting/searching, and Quick Add.

Base URL
http://127.0.0.1:8000
1. User Endpoints
Create User
POST /users

Example request:

{
  "name": "Badal",
  "email": "badal@example.com",
  "password": "password123"
}

Example response:

{
  "id": 1,
  "name": "Badal",
  "email": "badal@example.com"
}
List Users
GET /users

Example response:

[
  {
    "id": 1,
    "name": "Badal",
    "email": "badal@example.com"
  }
]
2. Authentication
Login
POST /login

Example form data:

username=badal@example.com
password=password123

Example response:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}

Protected endpoints require the JWT access token.

3. Project Endpoints
Create Project
POST /projects

Example request:

{
  "name": "TaskFlow Development 1"
}

Example response:

{
  "id": 1,
  "name": "TaskFlow Development 1",
  "owner_id": 1
}
List Projects
GET /projects

Example response:

[
  {
    "id": 1,
    "name": "TaskFlow Development 1",
    "owner_id": 1
  }
]
Get Project by ID
GET /projects/{project_id}

Example:

GET /projects/1

Example response:

{
  "id": 1,
  "name": "TaskFlow Development 1",
  "owner_id": 1
}
Update Project
PUT /projects/{project_id}

Example request:

{
  "name": "Updated TaskFlow Project"
}
Delete Project
DELETE /projects/{project_id}

Example response:

{
  "message": "Project deleted successfully"
}
4. Task Endpoints
Create Task
POST /tasks

Example request:

{
  "title": "Fix dashboard bug",
  "description": "Fix the dashboard issue",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}

Example response:

{
  "id": 1,
  "title": "Fix dashboard bug",
  "description": "Fix the dashboard issue",
  "status": "pending",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}
List Tasks
GET /tasks

Example response:

[
  {
    "id": 1,
    "title": "Fix dashboard bug",
    "status": "pending",
    "priority": "high",
    "project_id": 1
  }
]
Get Task by ID
GET /tasks/{task_id}

Example:

GET /tasks/1
Update Task
PUT /tasks/{task_id}

Example request:

{
  "title": "Fix dashboard bug",
  "description": "Updated description",
  "status": "completed",
  "priority": "high",
  "due_date": "2026-08-15",
  "project_id": 1
}
Delete Task
DELETE /tasks/{task_id}

Example response:

{
  "message": "Task deleted successfully"
}
5. Project Statistics
GET /projects/statistics

Returns task statistics grouped by project and status.

Example response:

[
  {
    "project_id": 1,
    "project_name": "TaskFlow Development 1",
    "status": "pending",
    "task_count": 5
  },
  {
    "project_id": 3,
    "project_name": "test project",
    "status": "pending",
    "task_count": 1
  }
]

The aggregation is performed by the database using SQL aggregation rather than counting all tasks in Python.

6. Algorithm-Based Task Sorting
GET /tasks?sort=priority

Returns tasks sorted by priority using the project's custom insertion-sort implementation.

Priority order:

low → medium → high

Example:

GET /tasks?sort=priority

Example response:

[
  {
    "id": 6,
    "title": "Test task creation 5",
    "priority": "low"
  },
  {
    "id": 8,
    "title": "Fix dashboard bug",
    "priority": "medium"
  },
  {
    "id": 2,
    "title": "Fix payment API check",
    "priority": "high"
  }
]
7. Task Search
GET /tasks/search?title=<exact-title>&algo=<binary|linear>

The default search algorithm is binary search.

Example using binary search:

GET /tasks/search?title=Fix%20payment%20API&algo=binary

Example using linear search:

GET /tasks/search?title=Fix%20payment%20API&algo=linear

Example response:

{
  "id": 7,
  "title": "Fix payment API",
  "status": "pending",
  "priority": "high"
}

If the task does not exist, the endpoint returns:

404 Not Found
8. Quick Add
POST /tasks/quick-add

Example request:

{
  "description": "Fix dashboard bug tomorrow, urgent",
  "project_id": 1
}

Example response:

{
  "id": 10,
  "title": "Fix dashboard bug",
  "description": null,
  "status": "pending",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1
}

The Quick Add feature uses the deterministic rule-based parser by default and does not require an API key or external network request.

HTTP Status Codes
Status Code	Meaning
200	Successful read/update
201	Resource successfully created
401	Authentication credentials are invalid or missing
404	Requested resource was not found
422	Request validation failed
500	Unexpected server error

## Git Workflow

TaskFlow was developed using a feature-branch workflow. Changes were developed on a feature branch and merged back into the main branch after completion.

## Testing

The algorithm checks can be run with:

```bash
python backend/algorithm_checker.py