from sqlalchemy.orm import Session
from typing import List
from .models import Teacher, Student, Goal, Note
from .schemas import GoalCreate, NoteCreate, StudentCreate, TeacherCreate

# -----------------------------
# Goals
# -----------------------------

def create_goal(db: Session, goal: GoalCreate, student_id: int = None, teacher_id: int = None) -> Goal:
    db_goal = Goal(**goal.dict(), student_id=student_id, teacher_id=teacher_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal_progress(db: Session, goal_id: int, progress: int) -> Goal:
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal:
        db_goal.progress = progress
        db.commit()
        db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int) -> None:
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()

def get_goals_by_student(db: Session, student_id: int) -> List[Goal]:
    return db.query(Goal).filter(Goal.student_id == student_id).all()

def get_goals_by_teacher(db: Session, teacher_id: int) -> List[Goal]:
    return db.query(Goal).filter(Goal.teacher_id == teacher_id).all()


# -----------------------------
# Notes
# -----------------------------

def create_note(db: Session, note: NoteCreate, student_id: int) -> Note:
    db_note = Note(**note.dict(), student_id=student_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes_by_student(db: Session, student_id: int) -> List[Note]:
    return db.query(Note).filter(Note.student_id == student_id).all()

def get_notes_by_teacher(db: Session, teacher_id: int) -> List[Note]:
    # Join Student to filter by teacher
    return db.query(Note).join(Student).filter(Student.teacher_id == teacher_id).all()


# -----------------------------
# Students
# -----------------------------

def create_student(db: Session, student: StudentCreate) -> Student:
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int) -> Student:
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session) -> List[Student]:
    return db.query(Student).all()

def delete_student(db: Session, student_id: int) -> None:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()


# -----------------------------
# Teachers
# -----------------------------

def create_teacher(db: Session, teacher: TeacherCreate) -> Teacher:
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_teacher(db: Session, teacher_id: int) -> Teacher:
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()

def get_teachers(db: Session) -> List[Teacher]:
    return db.query(Teacher).all()

def delete_teacher(db: Session, teacher_id: int) -> None:
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
