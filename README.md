# Student Tracker API

A modern FastAPI backend for managing students, teachers, goals, and notes in an educational setting. Includes a demo Streamlit GUI and a full test suite.

## Features

- **Student Management:** Create, list, and retrieve students
- **Teacher Management:** Create, retrieve, and delete teachers
- **Goals:** Assign and update goals for students
- **Notes:** Add and view notes for students
- **Dashboard:** View classroom dashboards
- **Authentication:** Signup and login endpoints for teachers
- **Demo GUI:** Streamlit-based interface for quick testing and demos
- **Testing:** Pytest-based test suite

## Tech Stack
- Python 3.9+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- PostgreSQL
- Streamlit (for demo GUI)
- Pytest (for testing)

## Project Structure

```
app/
  main.py           # FastAPI app and router includes
  models.py         # SQLAlchemy models
  schemas.py        # Pydantic schemas
  crud.py           # CRUD operations
  database.py       # DB connection/session
  routers/          # API endpoints (students, teachers, goals, notes, dashboard, auth)
alembic/            # Database migrations
alembic.ini         # Alembic config
conftest.py         # Pytest config
requirements.txt    # Python dependencies
demo_gui.py         # Streamlit demo GUI
tests/              # Pytest test modules
```

## Setup

1. **Clone the repo and enter the directory:**
   ```sh
   git clone <your-repo-url>
   cd pathways
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure your database** in `.env` or `alembic.ini`.
4. **Run migrations:**
   ```sh
   alembic upgrade head
   ```
5. **Start the API:**
   ```sh
   uvicorn app.main:app --reload
   ```
6. **(Optional) Run the demo GUI:**
   ```sh
   streamlit run demo_gui.py
   ```
7. **Run tests:**
   ```sh
   pytest
   ```

## API Documentation

Interactive docs available at [http://localhost:8000/docs](http://localhost:8000/docs) when the server is running.

## Example: Create a Student

```
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "dob": "2010-05-15",
    "disabilities": ["dyslexia"],
    "baseline_skills": {"math": "basic", "reading": "intermediate"}
  }'
```

## License

MIT License
