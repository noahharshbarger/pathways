from sqlalchemy.orm import Session
from typing import List
from .models import Teacher, Student, Goal, Note, IEP, ProgressLog
from .schemas import (
    GoalCreate,
    NoteCreate,
    TeacherCreate,
    StudentBase,
    IEPCreate,
    ProgressLogCreate,
)

# -----------------------------
# IEPs
# -----------------------------


def create_iep(db: Session, iep: IEPCreate) -> IEP:
    db_iep = IEP(**iep.dict())
    db.add(db_iep)
    db.commit()
    db.refresh(db_iep)
    return db_iep


def get_ieps_by_student(db: Session, student_id: int) -> List[IEP]:
    return db.query(IEP).filter(IEP.student_id == student_id).all()


def get_iep(db: Session, iep_id: int) -> IEP:
    return db.query(IEP).filter(IEP.id == iep_id).first()


def update_iep(db: Session, iep_id: int, data: dict, updated_by: str) -> IEP:
    db_iep = db.query(IEP).filter(IEP.id == iep_id).first()
    if db_iep:
        db_iep.data = data
        db_iep.updated_by = updated_by
        db.commit()
        db.refresh(db_iep)
    return db_iep


def delete_iep(db: Session, iep_id: int) -> None:
    db_iep = db.query(IEP).filter(IEP.id == iep_id).first()
    if db_iep:
        db.delete(db_iep)
        db.commit()

# -----------------------------
# Progress Logs
# -----------------------------


def create_progress_log(db: Session, log: ProgressLogCreate) -> ProgressLog:
    db_log = ProgressLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_progress_logs_by_iep(db: Session, iep_id: int) -> List[ProgressLog]:
    return db.query(ProgressLog).filter(ProgressLog.iep_id == iep_id).all()


def get_progress_log(db: Session, log_id: int) -> ProgressLog:
    return db.query(ProgressLog).filter(ProgressLog.id == log_id).first()


def delete_progress_log(db: Session, log_id: int) -> None:
    db_log = db.query(ProgressLog).filter(ProgressLog.id == log_id).first()
    if db_log:
        db.delete(db_log)
        db.commit()

# -----------------------------
# Goals
# -----------------------------


def create_goal(
        db: Session, goal: GoalCreate,
        student_id: int = None,
        teacher_id: int = None
        ) -> Goal:
    goal_data = goal.dict()
    goal_data.pop("student_id", None)
    # 'type' and 'target_date' ARE model columns and required, so keep them
    db_goal = Goal(**goal_data, student_id=student_id, teacher_id=teacher_id)
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
    note_data = note.dict()
    note_data.pop("student_id", None)
    db_note = Note(**note_data, student_id=student_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes_by_student(db: Session, student_id: int) -> List[Note]:
    return db.query(Note).filter(Note.student_id == student_id).all()


def get_notes_by_teacher(db: Session, teacher_id: int) -> List[Note]:
    # Join Student to filter by teacher
    return db.query(Note).join(Student).filter(
        Student.teacher_id == teacher_id).all()


# -----------------------------
# Students
# -----------------------------

def create_student(db: Session, student: StudentBase) -> Student:
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
