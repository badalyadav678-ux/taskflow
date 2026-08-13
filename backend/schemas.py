from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator




class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Password cannot be blank")

        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")

        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: str
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"
    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high)$"
    )
    due_date: str | None = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value

class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    status: str
    priority: str = Field(
        pattern="^(low|medium|high)$"
    )
    due_date: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    due_date: str | None = None
    project_id: int

    model_config = ConfigDict(from_attributes=True)

class QuickAddRequest(BaseModel):
    text: str
    project_id: int


class QuickAddTask(BaseModel):
    title: str
    description: str | None = None
    priority: str = "medium"
    due_date: str | None = None
    project_id: int

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

class ProjectUpdate(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)