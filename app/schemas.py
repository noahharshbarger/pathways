from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime


class TeacherBase(BaseModel):
    name: str
    email: str


class TeacherCreate(TeacherBase):
    password_hash: str


class Teacher(TeacherBase):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)


# -------------------
# Student Schemas
# -------------------
class StudentBase(BaseModel):
    name: str
    dob: datetime.date
    disabilities: Optional[List[str]] = []
    baseline_skills: Optional[dict] = {}


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    goals: List['Goal'] = []
    notes: List['Note'] = []

    model_config = ConfigDict(from_attributes=True)


# -------------------
# IEP and ProgressLog Schemas
# -------------------
class IEPBase(BaseModel):
    data: dict
    # Flexible IEP structure (goals, benchmarks, services, timelines)


class IEPCreate(IEPBase):
    student_id: int
    created_by: str


class IEP(IEPBase):
    id: int
    student_id: int
    created_by: str
    updated_by: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    progress_logs: List['ProgressLog'] = []

    model_config = ConfigDict(from_attributes=True)


class ProgressLogBase(BaseModel):
    data: dict  # Flexible log structure (daily/weekly logs, notes, attendance)


class ProgressLogCreate(ProgressLogBase):
    iep_id: int
    created_by: str


class ProgressLog(ProgressLogBase):
    id: int
    iep_id: int
    created_by: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


# Goal Schemas
class GoalBase(BaseModel):
    type: str
    description: str
    target_date: datetime.date
    progress: float = 0.0


class GoalCreate(GoalBase):
    student_id: int


class Goal(GoalBase):
    id: int
    student_id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------
# Notes Schemas
# -------------------
class NoteBase(BaseModel):
    author: str
    content: str


class NoteCreate(NoteBase):
    student_id: int


class Note(NoteBase):
    id: int
    student_id: int
    timestamp: datetime.datetime  # use datetime.datetime explicitly

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True  # needed for datetime
    )
