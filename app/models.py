from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="teacher")
    classroom_id = Column(Integer, unique=True)

    # Relationships
    students = relationship("Student", back_populates="teacher", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="teacher", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    dob = Column(Date)
    disabilities = Column(JSON)
    baseline_skills = Column(JSON)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    # Relationships
    teacher = relationship("Teacher", back_populates="students")
    goals = relationship("Goal", back_populates="student", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="student", cascade="all, delete-orphan")


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    progress = Column(Integer, default=0)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

    # Relationships
    student = relationship("Student", back_populates="goals")
    teacher = relationship("Teacher", back_populates="goals")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    author = Column(String)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    content = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="notes")
