from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime


class ParentBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class ParentCreate(ParentBase):
    pass


class Parent(ParentBase):
    id: int
    # List of student IDs (many-to-many)
    students: Optional[list[int]] = []
    model_config = ConfigDict(from_attributes=True)


# Association schema for Student <-> Parent (optional, for advanced use)
class StudentParentBase(BaseModel):
    student_id: int
    parent_id: int


class StudentParent(StudentParentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TeacherBase(BaseModel):
    name: str
    email: str
    role: Optional[str] = "teacher"


class TeacherCreate(TeacherBase):
    password_hash: str


class Teacher(TeacherBase):
    id: int
    email: str
    name: str
    role: str
    classroom_id: Optional[int] = None

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
    parents: Optional[list[int]] = []


class Student(StudentBase):
    id: int
    dob: datetime.date
    disabilities: Optional[List[str]] = []
    baseline_skills: Optional[dict] = {}
    teacher_id: Optional[int] = None
    # List of parent IDs (many-to-many)
    parents: Optional[list[int]] = []

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
    data: dict
    created_by: str
    updated_by: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ProgressLogBase(BaseModel):
    data: dict  # Flexible log structure (daily/weekly logs, notes, attendance)


class ProgressLogCreate(ProgressLogBase):
    iep_id: int
    created_by: str


class ProgressLog(ProgressLogBase):
    id: int
    iep_id: int
    data: dict
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
    description: str
    progress: float = 0.0
    teacher_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# -------------------
# Notes Schemas
# -------------------
class NoteBase(BaseModel):
    author: str
    content: str
    goal_id: Optional[int] = None


class NoteCreate(NoteBase):
    student_id: int


class Note(NoteBase):
    id: int
    student_id: int
    goal_id: Optional[int] = None
    author: str
    content: str
    timestamp: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
