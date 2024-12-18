# # schemas.py
# from pydantic import BaseModel
# from datetime import date

# class EmployeeBase(BaseModel):
#     name: str
#     position: str

# class EmployeeCreate(EmployeeBase):
#     pass

# class Employee(EmployeeBase):
#     id: int
#     hire_date: date
#     resume_filename: str

#     class Config:
#         orm_mode = True


from pydantic import BaseModel
from datetime import date

class EmployeeBase(BaseModel):
    name: str
    position: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    hire_date: date
    resume_filename: str

    class Config:
        # Change 'orm_mode' to 'from_attributes' for compatibility with Pydantic v2
        from_attributes = True
