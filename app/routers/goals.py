from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/goals", tags=["goals"])
get_db = database.get_db

@router.post("/", response_model=schemas.Goal)
def create_goal(goal: schemas.GoalCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_goal(db, goal, user_id)

@router.patch("/{goal_id}", response_model=schemas.Goal)
def update_goal(goal_id: int, progress: float, db: Session = Depends(get_db)):
    updated = crud.update_goal_progress(db, goal_id, progress)
    if not updated:
        raise HTTPException(status_code=404, detail="Goal not found")
    return updated

@router.get("/student/{student_id}", response_model=list[schemas.Goal])
def get_goals(student_id: int, db: Session = Depends(get_db)):
    return crud.get_goals_by_student(db, student_id)