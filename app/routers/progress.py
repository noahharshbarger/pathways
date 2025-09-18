from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(prefix="/progress", tags=["progress"])
get_db = database.get_db


@router.post("/", response_model=schemas.ProgressLog)
def create_progress_log(
    log: schemas.ProgressLogCreate,
    db: Session = Depends(get_db)
):
    return crud.create_progress_log(db, log)


@router.get("/iep/{iep_id}", response_model=List[schemas.ProgressLog])
def get_progress_logs_by_iep(iep_id: int, db: Session = Depends(get_db)):
    return crud.get_progress_logs_by_iep(db, iep_id)


@router.get("/{log_id}", response_model=schemas.ProgressLog)
def get_progress_log(log_id: int, db: Session = Depends(get_db)):
    log = crud.get_progress_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Progress log not found")
    return log


@router.delete("/{log_id}")
def delete_progress_log(log_id: int, db: Session = Depends(get_db)):
    crud.delete_progress_log(db, log_id)
    return {"ok": True}
