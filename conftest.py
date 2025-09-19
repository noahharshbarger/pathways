import pytest
import sqlalchemy
from app.database import engine
import sys
import os

# Add the project root to sys.path so 'app' can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(autouse=True)
def clean_db():
	"""Truncate all relevant tables and reset identity before each test."""
	with engine.connect() as conn:
		conn.execute(sqlalchemy.text(
			"""
			TRUNCATE teachers, students, goals, notes, ieps, progress_logs, parents, student_parents \
			RESTART IDENTITY CASCADE;
			"""
		))
		conn.commit()
