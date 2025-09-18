from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/notes", tags=["notes"])
get_db = database.get_db


@router.post("/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, note, note.student_id)


@router.get("/student/{student_id}", response_model=list[schemas.Note])
def get_notes(student_id: int, db: Session = Depends(get_db)):
    return crud.get_notes_by_student(db, student_id)