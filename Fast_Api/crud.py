# crud.py
from sqlalchemy.orm import Session
from models import Employee
from datetime import datetime

def create_employee(db: Session, name: str, position: str, resume_filename: str):
    db_employee = Employee(name=name, position=position, hire_date=datetime.utcnow(), resume_filename=resume_filename)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()

def update_employee(db: Session, employee_id: int, name: str, position: str):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db_employee.name = name
        db_employee.position = position
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
