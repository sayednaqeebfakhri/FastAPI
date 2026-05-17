import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/mlops")
def mlops():
    return {"message": "Welcome to MLOps!"}

def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
        )
    ''')

#create student
@app.post("/students/")
def create_student(name:str, age:int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age) VALUES (?,?)", (name, age))
    conn.commit()
    return {"message": "Student created successfully"}


#get one student
@app.get("/students/{student_id}")
def read_student(student_id: int):
    conn = get_db()
    cur = conn.cursor()
    student = cur.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"id": student["id"], "name": student["name"], "age": student["age"]}


#upadate student
@app.put("/students/{student_id}")
def update_student(student_id: int, name: str, age: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=?, age=? WHERE id=?", (name, age, student_id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}


#get all students
@app.get("/students/")
def read_students():
    conn = get_db()
    cur = conn.cursor()
    students = cur.execute("SELECT * FROM students").fetchall()
    return [{"id": student["id"], "name": student["name"], "age": student["age"]} for student in students]

#delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}