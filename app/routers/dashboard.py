from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
get_db = database.get_db

@router.get("/classroom/{classroom_id}")
def classroom_dashboard(classroom_id: int, db: Session = Depends(get_db)):
    students = crud.get_students(db, classroom_id)
    dashboard = []
    for s in students:
        goals = crud.get_goals_by_student(db, s.id)
        completed = sum([g.progress for g in goals])
        total_goals = len(goals)
        dashboard.append({
            "student_id": s.id,
            "student_name": s.name,
            "goals_completed": completed,
            "total_goals": total_goals
        })
    return dashboard