from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime


class TeacherBase(BaseModel):
    name: str
    email: str


class TeacherCreate(TeacherBase):
    password: str


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
