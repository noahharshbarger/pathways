
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/parents", tags=["parents"])
get_db = database.get_db

@router.get("/{parent_id}/students", response_model=list[schemas.Student])
def get_students_for_parent(parent_id: int, db: Session = Depends(get_db)):
    # Always return 200 with a list of students (may be empty)
    student_parents = db.query(crud.StudentParent).filter(crud.StudentParent.parent_id == parent_id).all()
    student_ids = [sp.student_id for sp in student_parents]
    students = []
    if student_ids:
        students = db.query(crud.Student).filter(crud.Student.id.in_(student_ids)).all()
    result = []
    for student in students:
        # Get all parent IDs for this student
        sps = db.query(crud.StudentParent).filter(crud.StudentParent.student_id == student.id).all()
        parent_ids = [sp.parent_id for sp in sps]
        # Build dict with all schema fields
        student_dict = {
            "id": student.id,
            "name": student.name,
            "dob": student.dob,
            "disabilities": student.disabilities,
            "baseline_skills": student.baseline_skills,
            "teacher_id": student.teacher_id,
            "parents": parent_ids,
        }
        result.append(student_dict)
    return result


@router.post("/", response_model=schemas.Parent)
def create_parent(parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    return crud.create_parent(db, parent)


@router.get("/", response_model=list[schemas.Parent])
def list_parents(db: Session = Depends(get_db)):
    return crud.get_parents(db)


@router.get("/{parent_id}", response_model=schemas.Parent)
def get_parent(parent_id: int, db: Session = Depends(get_db)):
    parent = crud.get_parent(db, parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent


@router.put("/{parent_id}", response_model=schemas.Parent)
def update_parent(
    parent_id: int, parent: schemas.ParentCreate, db: Session = Depends(get_db)
):
    updated = crud.update_parent(db, parent_id, parent)
    if not updated:
        raise HTTPException(status_code=404, detail="Parent not found")
    return updated


@router.delete("/{parent_id}")
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    crud.delete_parent(db, parent_id)
    return {"ok": True}
