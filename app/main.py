from fastapi import FastAPI
from .routers import students, goals, notes, dashboard, teachers

app = FastAPI(title="Student Tracker")

app.include_router(students.router)
app.include_router(goals.router)
app.include_router(notes.router)
app.include_router(dashboard.router)
app.include_router(teachers.router)