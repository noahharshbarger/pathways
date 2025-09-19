from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from typing import List

router = APIRouter(prefix="/students", tags=["students"])
get_db = database.get_db

@router.put("/{student_id}/parents", response_model=schemas.Student)
def set_student_parents(student_id: int, parent_ids: list[int], db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    crud.update_student_parents(db, student_id, parent_ids)
    return crud.get_student(db, student_id)


@router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # Pass StudentCreate directly to CRUD
    return crud.create_student(db, student)


@router.get("/", response_model=List[schemas.Student])
def list_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@router.get("/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student(db, student_id)