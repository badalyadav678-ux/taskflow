import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from jose import JWTError, jwt
from sqlalchemy import func
from algorithms import insertion_sort, linear_search, binary_search
from database import engine, get_db
from quick_add import parse_quick_add
from models import Base, User, Project, Task
from schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserLogin,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    QuickAddRequest,
    QuickAddTask,
    TaskResponse,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
)

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "http://127.0.0.1:5500",
         "http://localhost:5500",
         "https://taskflow-frontend-7lye.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} - "
        f"{process_time:.2f} ms"
    )

    return response

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


@app.get("/")
def home():
    return {
        "message": "TaskFlow API is running"
    }


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {
        "message": "Database session created successfully"
    }


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check whether another user already has this email
    existing_user = (
        db.query(User)
        .filter(
            User.email == user_data.email,
            User.id != user_id
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    password_is_correct = verify_password(
        form_data.password,
        user.password
    )

    if not password_is_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == task_data.project_id,
        Project.owner_id == current_user.id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this project"
        )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        project_id=task_data.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    sort: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = (
        db.query(Task)
        .join(Project)
        .filter(Project.owner_id == current_user.id)
        .all()
    )

    if sort == "priority":
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        tasks = insertion_sort(
            tasks,
            lambda task: priority_order[task.priority]
        )

    return tasks

@app.get(
    "/tasks/search",
    response_model=TaskResponse
)
def search_task(
    title: str,
    algo: str = "linear",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = (
        db.query(Task)
        .join(Project)
        .filter(Project.owner_id == current_user.id)
        .all()
    )

    if algo == "linear":
        task = linear_search(
            tasks,
            title,
            lambda task: task.title
        )

    elif algo == "binary":
        tasks = insertion_sort(
            tasks,
            lambda task: task.title
        )

        task = binary_search(
            tasks,
            title,
            lambda task: task.title
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Algorithm must be 'linear' or 'binary'"
        )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .join(Project)
        .filter(
            Task.id == task_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .join(Project)
        .filter(
            Task.id == task_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    task.priority = task_data.priority
    task.due_date = task_data.due_date

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .join(Project)
        .filter(
            Task.id == task_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }

@app.get("/projects/statistics")
def project_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    statistics = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
            Task.status.label("status"),
            func.count(Task.id).label("task_count")
        )
        .join(Task, Task.project_id == Project.id)
        .filter(Project.owner_id == current_user.id)
        .group_by(
            Project.id,
            Project.name,
            Task.status
        )
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "status": row.status,
            "task_count": row.task_count
        }
        for row in statistics
    ]





@app.post(
    "/tasks/quick-add",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def quick_add_task(
    request: QuickAddRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        parsed_task = parse_quick_add(
    request.text,
    request.project_id
)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error)
        )

    project = (
    db.query(Project)
    .filter(
        Project.id == parsed_task.project_id,
        Project.owner_id == current_user.id
    )
    .first()
)

    if project is None:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have access to this project"
    )

    new_task = Task(
        title=parsed_task.title,
        description=parsed_task.description,
        priority=parsed_task.priority,
        due_date=parsed_task.due_date,
        project_id=parsed_task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.post(
    "/projects",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectResponse
)
def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@app.get(
    "/projects",
    response_model=list[ProjectResponse]
)
def get_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = (
        db.query(Project)
        .filter(Project.owner_id == current_user.id)
        .all()
    )

    return projects




@app.get(
    "/projects/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project

@app.put(
    "/projects/{project_id}",
    response_model=ProjectResponse
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    project.name = project_data.name
    project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }


