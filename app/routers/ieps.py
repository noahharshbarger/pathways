from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(prefix="/ieps", tags=["ieps"])
get_db = database.get_db


@router.post("/", response_model=schemas.IEP)
def create_iep(iep: schemas.IEPCreate, db: Session = Depends(get_db)):
    return crud.create_iep(db, iep)


@router.get("/student/{student_id}", response_model=List[schemas.IEP])
def get_ieps_by_student(student_id: int, db: Session = Depends(get_db)):
    return crud.get_ieps_by_student(db, student_id)


@router.get("/{iep_id}", response_model=schemas.IEP)
def get_iep(iep_id: int, db: Session = Depends(get_db)):
    iep = crud.get_iep(db, iep_id)
    if not iep:
        raise HTTPException(status_code=404, detail="IEP not found")
    return iep


@router.put("/{iep_id}", response_model=schemas.IEP)
def update_iep(
    iep_id: int,
    iep_update: schemas.IEPBase,
    db: Session = Depends(get_db)
):
    updated_by = "system"  # Placeholder
    iep = crud.update_iep(db, iep_id, iep_update.data, updated_by)
    if not iep:
        raise HTTPException(status_code=404, detail="IEP not found")
    return iep


# Assume updated_by is passed (iep_update.data) or separate field in a real app
@router.delete("/{iep_id}")
def delete_iep(iep_id: int, db: Session = Depends(get_db)):
    crud.delete_iep(db, iep_id)
    return {"ok": True}
