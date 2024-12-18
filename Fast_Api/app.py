# # app.py
# from fastapi import FastAPI, Depends, File, UploadFile
# from typing import List

# from fastapi.responses import FileResponse
# from sqlalchemy.orm import Session
# from crud import create_employee, get_employees, get_employee, update_employee, delete_employee
# from schemas import EmployeeCreate, Employee
# from database import SessionLocal, init_db
# import os
# import shutil

# # Initialize the database
# init_db()

# # Create FastAPI instance
# app = FastAPI()

# # Dependency for getting the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Route to create a new employee
# @app.post("/employees/", response_model=Employee)
# async def create_employee_view(employee: EmployeeCreate, db: Session = Depends(get_db), resume: UploadFile = File(...)):
#     file_location = os.path.join("uploads", resume.filename)
#     with open(file_location, "wb") as f:
#         shutil.copyfileobj(resume.file, f)
    
#     db_employee = create_employee(db=db, name=employee.name, position=employee.position, resume_filename=resume.filename)
#     return db_employee

# # Route to get all employees
# @app.get("/employees/", response_model=List[Employee])
# def get_employees_view(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     employees = get_employees(db=db, skip=skip, limit=limit)
#     return employees

# # Route to get a single employee
# @app.get("/employees/{employee_id}", response_model=Employee)
# def get_employee_view(employee_id: int, db: Session = Depends(get_db)):
#     db_employee = get_employee(db=db, employee_id=employee_id)
#     return db_employee

# # Route to update employee information
# @app.put("/employees/{employee_id}", response_model=Employee)
# async def update_employee_view(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
#     db_employee = update_employee(db=db, employee_id=employee_id, name=employee.name, position=employee.position)
#     return db_employee

# # Route to delete an employee
# @app.delete("/employees/{employee_id}")
# async def delete_employee_view(employee_id: int, db: Session = Depends(get_db)):
#     db_employee = delete_employee(db=db, employee_id=employee_id)
#     return db_employee

# # Route to download the employee's resume
# @app.get("/employees/{employee_id}/download")
# def download_resume(employee_id: int, db: Session = Depends(get_db)):
#     db_employee = get_employee(db=db, employee_id=employee_id)
#     file_path = os.path.join("uploads", db_employee.resume_filename)
#     return FileResponse(file_path)


from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from crud import create_employee, get_employees, get_employee, update_employee, delete_employee
from schemas import EmployeeCreate, Employee
from database import SessionLocal, init_db

from fastapi.templating import Jinja2Templates
from fastapi import Request

# Initialize the database
init_db()

# Create FastAPI instance
app = FastAPI()

# Serve the index.html form page
# @app.get("/", response_class=HTMLResponse)
# async def serve_form():
#     with open("/static/index.html", "r") as f:
#         return HTMLResponse(content=f.read())

templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create a new employee
@app.post("/employees/", response_model=Employee)
async def create_employee_view(employee: EmployeeCreate, db: Session = Depends(get_db), resume: UploadFile = File(...)):
    file_location = os.path.join("uploads", resume.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(resume.file, f)
    
    db_employee = create_employee(db=db, name=employee.name, position=employee.position, resume_filename=resume.filename)
    return db_employee

# Route to get all employees
@app.get("/employees/", response_model=List[Employee])
def get_employees_view(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = get_employees(db=db, skip=skip, limit=limit)
    return employees

# Route to get a single employee
@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee_view(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(db=db, employee_id=employee_id)
    return db_employee

# Route to update employee information
@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee_view(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = update_employee(db=db, employee_id=employee_id, name=employee.name, position=employee.position)
    return db_employee

# Route to delete an employee
@app.delete("/employees/{employee_id}")
async def delete_employee_view(employee_id: int, db: Session = Depends(get_db)):
    db_employee = delete_employee(db=db, employee_id=employee_id)
    return db_employee

# Route to download the employee's resume
@app.get("/employees/{employee_id}/download")
def download_resume(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(db=db, employee_id=employee_id)
    file_path = os.path.join("uploads", db_employee.resume_filename)
    return FileResponse(file_path)
