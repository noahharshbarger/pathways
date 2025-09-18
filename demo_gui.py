import streamlit as st
import requests
import datetime

API_URL = "http://localhost:8000"

st.title("Student Demo GUI")

st.header("Add a Student")
with st.form("student_form"):
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth", value=datetime.date(2010, 1, 1))
    disabilities = st.text_input("Disabilities (comma separated)")
    baseline_skills = st.text_area(
        "Baseline Skills (JSON)",
        value='{"math": "basic", "reading": "intermediate"}'
        )
    submitted = st.form_submit_button("Add Student")

    if submitted:
        try:
            skills = eval(baseline_skills)
            data = {
                "name": name,
                "dob": str(dob),
                "disabilities":
                [d.strip() for d in disabilities.split(",") if d.strip()],
                "baseline_skills": skills
            }
            resp = requests.post(f"{API_URL}/students/", json=data)
            if resp.status_code == 200:
                st.success("Student added!")
            else:
                st.error(f"Error: {resp.text}")
        except Exception as e:
            st.error(f"Invalid input: {e}")

st.header("All Students")
if st.button("Refresh List"):
    st.session_state["students"] = None

if "students" not in st.session_state or st.session_state["students"] is None:
    resp = requests.get(f"{API_URL}/students/")
    if resp.status_code == 200:
        st.session_state["students"] = resp.json()
    else:
        st.session_state["students"] = []

for student in st.session_state["students"]:
    st.write(student)
