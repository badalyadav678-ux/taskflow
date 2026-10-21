const totalTasks = document.getElementById("totalTasks");
const pendingTasks = document.getElementById("pendingTasks");
const completedTasks = document.getElementById("completedTasks");
const taskForm = document.getElementById("taskForm");

const taskTitleInput = document.getElementById("taskTitle");
const taskDescriptionInput = document.getElementById("taskDescription");
const taskStatusInput = document.getElementById("taskStatus");
const taskPriorityInput = document.getElementById("taskPriority");
const taskDueDateInput = document.getElementById("taskDueDate");
const taskProjectInput = document.getElementById("taskProject");

const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");

const quickAddForm = document.getElementById("quickAddForm");
const quickAddInput = document.getElementById("quickAddInput");
const quickAddProject = document.getElementById("quickAddProject");

const taskMessage = document.getElementById("taskMessage");

function showMessage(element, message, type = "success") {
  element.textContent = message;

  element.className = "";

  if (type === "success") {
    element.classList.add("success-message");
  } else {
    element.classList.add("error-message");
  }

  setTimeout(function () {
    element.textContent = "";
    element.className = "";
  }, 3000);
}

quickAddForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const text = quickAddInput.value.trim();

  if (!text) {
    console.log("Please enter a task");
    return;
  }

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("https://taskflow-3485.onrender.com/tasks/quick-add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        text: text,
        project_id: Number(quickAddProject.value),
      }),
    });

    const data = await response.json();

    console.log("Quick Add status:", response.status);
    console.log("Quick Add response:", JSON.stringify(data, null, 2));

    if (!response.ok) {
      console.error("Quick Add failed:", data);
      return;
    }

    quickAddForm.reset();

    await loadTasks();
    await loadStatistics();
  } catch (error) {
    console.error("Quick Add error:", error);
  }
});

searchBtn.addEventListener("click", async function () {
  const title = searchInput.value.trim();

  if (!title) {
    console.log("Please enter a task title");
    loadTasks();
    return;
  }

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(
      `https://taskflow-3485.onrender.com/tasks/search?title=${encodeURIComponent(title)}&algo=linear`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    const data = await response.json();

    console.log("Search response:", JSON.stringify(data, null, 2));

    if (!response.ok) {
      console.error("Task not found:", data);
      taskList.innerHTML = "<p>Task not found.</p>";
      return;
    }

    taskList.innerHTML = "";

    const taskCard = document.createElement("div");
    taskCard.className = "task-card";

    taskCard.innerHTML = `
            <h3>${data.title}</h3>

            <p>
                ${data.description || "No description"}
            </p>

            <p>Status: ${data.status}</p>

            <p>Priority: ${data.priority}</p>

            <p>Due Date: ${data.due_date || "No due date"}</p>
        `;

    taskList.appendChild(taskCard);
  } catch (error) {
    console.error("Error searching task:", error);
  }
});

taskForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const taskData = {
    title: taskTitleInput.value.trim(),
    description: taskDescriptionInput.value.trim(),
    status: taskStatusInput.value,
    priority: taskPriorityInput.value,
    due_date: taskDueDateInput.value || null,
    project_id: Number(taskProjectInput.value),
  };

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("https://taskflow-3485.onrender.com/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    const data = await response.json();

    console.log("Task response:", data);

    if (!response.ok) {
      console.error("Failed to create task:", data);

      showMessage(
        taskMessage,
        data.detail || "Failed to create task.",
        "error",
      );

      return;
    }

    taskForm.reset();

    showMessage(
      taskMessage,
      `Task "${data.title}" created successfully!`,
      "success",
    );

    await loadTasks();
    await loadProjects();
    await loadStatistics();
  } catch (error) {
    console.error("Error creating task:", error);

    showMessage(
      taskMessage,
      "Something went wrong while creating the task.",
      "error",
    );
  }
});

const projectNameInput = document.getElementById("projectName");
const projectDescriptionInput = document.getElementById("projectDescription");
const projectList = document.getElementById("projectList");
const taskList = document.getElementById("taskList");
const TASK_CACHE_KEY = "taskflow_tasks";

function getTaskCacheKey() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    return null;
  }

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));

    return `taskflow_tasks_user_${payload.sub}`;
  } catch (error) {
    console.error("Unable to read user ID from JWT:", error);
    return null;
  }
}

function renderTasks(data) {
  taskList.innerHTML = "";

  console.log("Number of tasks:", data.length);
  console.log("taskList element:", taskList);

  data.forEach(function (task) {
    console.log("Rendering task:", task);

    const taskCard = document.createElement("div");
    taskCard.className = "task-card";

    const title = document.createElement("h3");
    title.textContent = task.title;

    const description = document.createElement("p");
    description.textContent = task.description || "No description";

    const status = document.createElement("p");
    status.textContent = `Status: ${task.status}`;

    const priority = document.createElement("p");
    priority.textContent = `Priority: ${task.priority}`;

    const dueDate = document.createElement("p");
    dueDate.textContent = `Due Date: ${task.due_date || "No due date"}`;

    const actions = document.createElement("div");
    actions.className = "card-actions";

    const editBtn = document.createElement("button");
    editBtn.className = "edit-btn";
    editBtn.textContent = "Edit";

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-btn";
    deleteBtn.textContent = "Delete";

    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    taskCard.appendChild(title);
    taskCard.appendChild(description);
    taskCard.appendChild(status);
    taskCard.appendChild(priority);
    taskCard.appendChild(dueDate);
    taskCard.appendChild(actions);

    taskList.appendChild(taskCard);

    // DELETE TASK
    deleteBtn.addEventListener("click", async function () {
      const token = localStorage.getItem("access_token");

      console.log("DELETE token exists:", !!token);
      console.log(
        "DELETE token starts with:",
        token ? token.substring(0, 10) : "NO TOKEN",
      );

      try {
        const response = await fetch(`https://taskflow-3485.onrender.com/tasks/${task.id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await response.json();

        console.log("Delete response:", data);

        if (!response.ok) {
          console.error("Failed to delete task:", data);

          showMessage(
            taskMessage,
            data.detail || "Failed to delete task.",
            "error",
          );

          return;
        }

        showMessage(taskMessage, "Task deleted successfully!", "success");

        await loadTasks();
        await loadStatistics();
      } catch (error) {
        console.error("Error deleting task:", error);
      }
    });

    // EDIT TASK
    editBtn.addEventListener("click", async function () {
      const newTitle = prompt("Enter new task title:", task.title);

      if (newTitle === null || newTitle.trim() === "") {
        return;
      }

      const newDescription = prompt(
        "Enter new description:",
        task.description || "",
      );

      const token = localStorage.getItem("access_token");

      const updatedTask = {
        title: newTitle.trim(),
        description: newDescription,
        status: task.status,
        priority: task.priority,
        due_date: task.due_date,
      };

      try {
        const response = await fetch(`https://taskflow-3485.onrender.com/tasks/${task.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(updatedTask),
        });

        const data = await response.json();

        console.log("Update response:", data);

        if (!response.ok) {
          console.error("Failed to update task:", data);

          showMessage(
            taskMessage,
            data.detail || "Failed to update task.",
            "error",
          );

          return;
        }

        showMessage(
          taskMessage,
          `Task "${data.title}" updated successfully!`,
          "success",
        );

        await loadTasks();
        await loadStatistics();
      } catch (error) {
        console.error("Error updating task:", error);
      }
    });
  });
}

async function loadProjects() {
  const token = localStorage.getItem("access_token");

  console.log("Project GET token:", token);

  try {
    // --------------------------------
    // 1. Get projects
    // --------------------------------

    const projectResponse = await fetch("https://taskflow-3485.onrender.com/projects", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const projects = await projectResponse.json();

    console.log("Projects response:", projects);

    if (!projectResponse.ok) {
      console.error("Failed to load projects:", projects);
      return;
    }

    // --------------------------------
    // 2. Get all tasks
    // --------------------------------

    const taskResponse = await fetch("https://taskflow-3485.onrender.com/tasks", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const tasks = await taskResponse.json();

    console.log("Tasks for projects:", tasks);

    if (!taskResponse.ok) {
      console.error("Failed to load tasks:", tasks);
      return;
    }

    // --------------------------------
    // 3. Clear old project cards
    // --------------------------------

    projectList.innerHTML = "";

    // --------------------------------
    // 4. Reset task dropdown
    // --------------------------------

    taskProjectInput.innerHTML = `
      <option value="">Select Project</option>
    `;

    // --------------------------------
    // 5. Reset Quick Add dropdown
    // --------------------------------

    quickAddProject.innerHTML = `
      <option value="">Select Project</option>
    `;

    // --------------------------------
    // 6. Create each project
    // --------------------------------

    projects.forEach(function (project) {
      // ==========================================
      // PROJECT CARD
      // ==========================================

      const projectCard = document.createElement("div");

      projectCard.className = "project-card";

      // ==========================================
      // PROJECT TITLE
      // ==========================================

      const projectTitle = document.createElement("h3");

      projectTitle.textContent = project.name;

      // ==========================================
      // PROJECT DESCRIPTION
      // ==========================================

      const projectDescription = document.createElement("p");

      projectDescription.textContent = project.description || "No description";

      // ==========================================
      // ADD NEW TASK BUTTON
      // ==========================================

      const addTaskBtn = document.createElement("button");

      addTaskBtn.className = "add-task-btn";

      addTaskBtn.textContent = "+ Add a new task";

      addTaskBtn.addEventListener("click", function () {
        // Select this project in the task form
        taskProjectInput.value = project.id;

        // Move user to task form
        taskForm.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });

        // Put cursor inside title field
        taskTitleInput.focus();
      });

      // ==========================================
      // TASK HEADING
      // ==========================================

      const tasksHeading = document.createElement("h4");

      tasksHeading.textContent = "Tasks:";

      // ==========================================
      // TASK LIST
      // ==========================================

      const projectTaskList = document.createElement("div");

      projectTaskList.className = "project-task-list";

      // Find tasks belonging to this project
      const projectTasks = tasks.filter(function (task) {
        return task.project_id === project.id;
      });

      // ==========================================
      // DISPLAY TASKS
      // ==========================================

      if (projectTasks.length === 0) {
        const noTasks = document.createElement("p");

        noTasks.textContent = "No tasks yet.";

        noTasks.className = "no-project-tasks";

        projectTaskList.appendChild(noTasks);
      } else {
        projectTasks.forEach(function (task) {
          // Task row
          const taskRow = document.createElement("div");

          taskRow.className = "project-task";

          // Checkbox
          const checkbox = document.createElement("input");

          checkbox.type = "checkbox";

          checkbox.checked = task.status === "completed";

          // Task title
          const taskTitle = document.createElement("span");

          taskTitle.textContent = task.title;

          // Completed task styling
          if (task.status === "completed") {
            taskTitle.classList.add("completed-task");
          }

          // Add checkbox and title
          taskRow.appendChild(checkbox);

          taskRow.appendChild(taskTitle);

          // ==========================================
          // CHECKBOX -> MARK TASK COMPLETED
          // ==========================================

          checkbox.addEventListener("change", async function () {
            const newStatus = checkbox.checked ? "completed" : "pending";

            const updatedTask = {
              title: task.title,

              description: task.description,

              status: newStatus,

              priority: task.priority,

              due_date: task.due_date,
            };

            try {
              const response = await fetch(
                `https://taskflow-3485.onrender.com/tasks/${task.id}`,
                {
                  method: "PUT",

                  headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                  },

                  body: JSON.stringify(updatedTask),
                },
              );

              const data = await response.json();

              if (!response.ok) {
                console.error("Failed to update task status:", data);

                // Revert checkbox
                checkbox.checked = !checkbox.checked;

                return;
              }

              // Update visual state
              if (newStatus === "completed") {
                taskTitle.classList.add("completed-task");
              } else {
                taskTitle.classList.remove("completed-task");
              }

              console.log(`Task "${task.title}" marked as ${newStatus}`);

              // Update statistics
              await loadStatistics();

              // Update task cache/list
              await loadTasks();
            } catch (error) {
              console.error("Error updating task status:", error);

              // Revert checkbox
              checkbox.checked = !checkbox.checked;
            }
          });

          projectTaskList.appendChild(taskRow);
        });
      }

      // ==========================================
      // PROJECT ACTION BUTTONS
      // ==========================================

      const projectActions = document.createElement("div");

      projectActions.className = "card-actions";

      // Edit
      const editProjectBtn = document.createElement("button");

      editProjectBtn.className = "edit-btn";

      editProjectBtn.textContent = "Edit";

      // Delete
      const deleteProjectBtn = document.createElement("button");

      deleteProjectBtn.className = "delete-btn";

      deleteProjectBtn.textContent = "Delete";

      projectActions.appendChild(editProjectBtn);

      projectActions.appendChild(deleteProjectBtn);

      // ==========================================
      // PUT EVERYTHING INSIDE PROJECT CARD
      // ==========================================

      projectCard.appendChild(projectTitle);

      projectCard.appendChild(projectDescription);

      projectCard.appendChild(addTaskBtn);

      projectCard.appendChild(tasksHeading);

      projectCard.appendChild(projectTaskList);

      projectCard.appendChild(projectActions);

      projectList.appendChild(projectCard);

      // ==========================================
      // EDIT PROJECT
      // ==========================================

      editProjectBtn.addEventListener("click", async function () {
        const newName = prompt("Enter new project name:", project.name);

        if (newName === null || newName.trim() === "") {
          return;
        }

        const newDescription = prompt(
          "Enter new project description:",
          project.description || "",
        );

        try {
          const response = await fetch(
            `https://taskflow-3485.onrender.com/projects/${project.id}`,
            {
              method: "PUT",

              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },

              body: JSON.stringify({
                name: newName.trim(),
                description: newDescription,
              }),
            },
          );

          const data = await response.json();

          if (!response.ok) {
            console.error("Failed to update project:", data);

            showMessage(
              projectMessage,
              data.detail || "Failed to update project.",
              "error",
            );

            return;
          }

          showMessage(
            projectMessage,
            `Project "${data.name}" updated successfully!`,
            "success",
          );

          await loadProjects();
        } catch (error) {
          console.error("Error updating project:", error);
        }
      });

      // ==========================================
      // DELETE PROJECT
      // ==========================================

      deleteProjectBtn.addEventListener("click", async function () {
        const confirmed = confirm(
          `Are you sure you want to delete "${project.name}"?`,
        );

        if (!confirmed) {
          return;
        }

        try {
          const response = await fetch(
            `https://taskflow-3485.onrender.com/projects/${project.id}`,
            {
              method: "DELETE",

              headers: {
                Authorization: `Bearer ${token}`,
              },
            },
          );

          const data = await response.json();

          console.log("Delete project response:", data);

          if (!response.ok) {
            console.error("Failed to delete project:", data);

            showMessage(
              projectMessage,
              data.detail || "Failed to delete project.",
              "error",
            );

            return;
          }

          showMessage(
            projectMessage,
            "Project deleted successfully!",
            "success",
          );

          await loadProjects();

          await loadTasks();

          await loadStatistics();
        } catch (error) {
          console.error("Error deleting project:", error);
        }
      });

      // ==========================================
      // TASK FORM PROJECT DROPDOWN
      // ==========================================

      const projectOption = document.createElement("option");

      projectOption.value = project.id;

      projectOption.textContent = project.name;

      taskProjectInput.appendChild(projectOption);

      // ==========================================
      // QUICK ADD PROJECT DROPDOWN
      // ==========================================

      const quickAddOption = document.createElement("option");

      quickAddOption.value = project.id;

      quickAddOption.textContent = project.name;

      quickAddProject.appendChild(quickAddOption);
    });
  } catch (error) {
    console.error("Error loading projects:", error);
  }
}

async function loadTasks() {
  const token = localStorage.getItem("access_token");

  // --------------------------------
  // 1. Render cached tasks first
  // --------------------------------

  const cacheKey = getTaskCacheKey();

  const cachedTasks = cacheKey ? localStorage.getItem(cacheKey) : null;

  if (cachedTasks) {
    try {
      const parsedTasks = JSON.parse(cachedTasks);

      console.log("Rendering tasks from localStorage:", parsedTasks);

      renderTasks(parsedTasks);
    } catch (error) {
      console.error("Invalid task cache:", error);

      localStorage.removeItem(TASK_CACHE_KEY);
    }
  }

  // --------------------------------
  // 2. Fetch latest tasks from backend
  // --------------------------------

  try {
    const response = await fetch("https://taskflow-3485.onrender.com/tasks", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await response.json();

    console.log("Tasks response:", data);

    if (!response.ok) {
      console.error("Failed to load tasks:", data);
      return;
    }

    // --------------------------------
    // 3. Update localStorage
    // --------------------------------

    if (cacheKey) {
      localStorage.setItem(cacheKey, JSON.stringify(data));
    }

    console.log("Tasks cached in localStorage");

    // --------------------------------
    // 4. Render latest backend data
    // --------------------------------

    renderTasks(data);
  } catch (error) {
    console.error("Error loading tasks:", error);
  }
}

async function loadStatistics() {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch("https://taskflow-3485.onrender.com/projects/statistics", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await response.json();

    console.log("Statistics response:", data);

    if (!response.ok) {
      console.error("Failed to load statistics:", data);
      return;
    }

    let total = 0;
    let pending = 0;
    let completed = 0;

    data.forEach(function (project) {
      total += project.task_count;

      if (project.status === "pending") {
        pending += project.task_count;
      }

      if (project.status === "completed") {
        completed += project.task_count;
      }
    });

    totalTasks.textContent = total;
    pendingTasks.textContent = pending;
    completedTasks.textContent = completed;
  } catch (error) {
    console.error("Error loading statistics:", error);
  }
}

const projectForm = document.getElementById("projectForm");

projectForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const projectName = projectNameInput.value.trim();
  const projectDescription = projectDescriptionInput.value.trim();

  if (!projectName) {
    console.log("Please enter a project name");
    return;
  }

  const token = localStorage.getItem("access_token");

  console.log("Creating project...");
  console.log("Token exists:", !!token);
  console.log(
    "Token starts with:",
    token ? token.substring(0, 10) : "NO TOKEN",
  );

  if (!token) {
    console.error("No JWT token found. Please login again.");
    return;
  }

  const projectData = {
    name: projectName,
    description: projectDescription,
  };

  try {
    const response = await fetch("https://taskflow-3485.onrender.com/projects", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(projectData),
    });

    const data = await response.json();

    console.log("Project POST status:", response.status);
    console.log("Project POST response:", data);

    if (!response.ok) {
      console.error("Failed to create project:", data);
      return;
    }

    console.log("Project created successfully!");

    projectForm.reset();

    await loadProjects();

    alert(`Project "${data.name}" created successfully!`);
  } catch (error) {
    console.error("Error creating project:", error);
  }
});

const loginForm = document.getElementById("loginForm");

const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");

loginForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const email = loginEmail.value;
  const password = loginPassword.value;

  const formData = new URLSearchParams();

  formData.append("username", email);
  formData.append("password", password);

  try {
    const response = await fetch("https://taskflow-3485.onrender.com/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    const data = await response.json();

    console.log("Login response:", data);

    if (!response.ok) {
      console.error("Login failed:", data);
      return;
    }

    localStorage.setItem("access_token", data.access_token);

    console.log("JWT stored successfully");

    await loadProjects();
    await loadTasks();
    await loadStatistics();
  } catch (error) {
    console.error("Login error:", error);
  }
});
const savedToken = localStorage.getItem("access_token");

if (savedToken) {
  loadProjects();
  loadTasks();
  loadStatistics();
}
const logoutBtn = document.getElementById("logoutBtn");

logoutBtn.addEventListener("click", function () {
  localStorage.removeItem("access_token");

  console.log("Logged out successfully");

  location.reload();
});
