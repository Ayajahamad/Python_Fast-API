from webbrowser import get
from fastapi import Depends, FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import SessionLocal, Employee, User
from fastapi.responses import JSONResponse
import os
from io import BytesIO
from pydantic import BaseModel

app = FastAPI()

# Linking to Html
templates = Jinja2Templates(directory = "templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# To Get the Hhome Page
@app.get("/", response_class = HTMLResponse)
def get_homepage(request : Request):
    return templates.TemplateResponse("home.html",{"request":request})

# To Get the Html Page for Upload
@app.get("/upload/", response_class = HTMLResponse)
def get_homepage(request : Request):
    return templates.TemplateResponse("upload.html",{"request":request})

# Uploading A Employee Datails
@app.post("/uploaded/", response_class=HTMLResponse)
async def upload_employee(
    request: Request,
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    number: int = Form(...),
    qualification: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
    ):
    
    # Read the file data
    file_data = await file.read()
    
    # ---------
    UPLOAD_DIRECTORY = os.path.abspath("./uploads")
    print("Directory:",UPLOAD_DIRECTORY)
     
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    print("File will be saved to:", file_location)
    
    try:
        with open(file_location, "wb") as f:
            f.write(file_data)
            
        print(f"File : {file.filename} saved successfully at : {file_location}")    
        
    except Exception as e:
         print(f"Error saving file: {e}")
         return JSONResponse(content={"error": f"Error saving file: {str(e)}"}, status_code=500)
    # -----------
    
    # Saving the Employee_Details to DataBase
    try:
        db_employee = Employee(
            filename=file.filename,
            file_data=file_data ,
            e_name = name, 
            email=email, 
            qualification=qualification, 
            number=number, 
            role=role)
    
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
    
        # # Return the employee ID as a JSON response
        # return JSONResponse(content={"id": db_employee.id,"name":name,"file":file.filename,"message":"Successfully Uploaded"})
    
        # Render the success page using the uploaded Employee details
        return templates.TemplateResponse(
            "upload_success.html", 
            {
                "request": request, 
                "id":db_employee.id,
                "file_id": db_employee.id, 
                "name": db_employee.e_name, 
                "email": db_employee.email, 
                "filename": db_employee.filename,
                # "emp":db_employee
            }
        )
    
    except Exception as e:
        print(f"Error saving employee data to database: {e}")
        return JSONResponse(content={"error": f"Error saving employee data to database: {str(e)}"}, status_code=500)
   
# Get the HTML For Downloading.
@app.get("/download/")   
def get_download(request : Request):
    return templates.TemplateResponse("download.html",{"request":request})

# Get the HTML For Updating.
@app.get("/updateid/")   
def get_download(request : Request):
    return templates.TemplateResponse("updateid.html",{"request":request})

# Get the HTML For Deleting.
@app.get("/deleteid/")   
def get_download(request : Request):
    return templates.TemplateResponse("delete.html",{"request":request})

# Download a Resume File Using ID.
@app.get("/download/{e_id}")
def resume_download(e_id:int, db:Session = Depends(get_db)):
    db_resume = db.query(Employee).filter(Employee.id == e_id).first()
    
    if db_resume is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # The Content-Disposition header controls how the browser handles the file: "inline" displays the file directly in the browser (if possible), while "attachment" prompts the user to download the file, specifying the suggested file name for download.
    return StreamingResponse(BytesIO(db_resume.file_data), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={db_resume.e_name + db_resume.filename}"})
  
# Getting All the Employees
@app.get("/employees/", response_class=HTMLResponse)
def getall_employees(request : Request,db:Session = Depends(get_db)):
    employees = db.query(Employee).all()
    
    return templates.TemplateResponse("all_employees.html",{"request":request, "employees":employees})

# Deleting an Employee
@app.post("/delete/{e_id}", response_class=HTMLResponse)
def delete_employee(request : Request, e_id:int, db:Session = Depends(get_db)):
    db_emp = db.query(Employee).filter(Employee.id == e_id).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    #--------Removing A File in Local Directory---------
    UPLOAD_DIRECTORY = os.path.abspath("./uploads")
    file_location = os.path.join(UPLOAD_DIRECTORY, db_emp.filename)

    # Check if the file exists and delete it
    if os.path.exists(file_location):
        os.remove(file_location)
    else:
        # raise HTTPException(status_code=404, detail="File not found")
        print(file_location," is not In Local Directory")
    #-----------------
    
    db.delete(db_emp)
    db.commit()

    return JSONResponse(content={"id": db_emp.id,"name":db_emp.e_name,"file":db_emp.filename,"message":"Successfully Deleted"}) 

# Get the HTML For Updating.
@app.get("/update/{e_id}")   
def get_download(request : Request, e_id:int, db:Session = Depends(get_db)):
    db_emp = db.query(Employee).filter(Employee.id == e_id).first()
    
    return templates.TemplateResponse("update.html",{"request":request, "emp":db_emp})

# Uploading A Employee Datails
@app.post("/update/{e_id}", response_class=HTMLResponse)
async def upload_employee(
    request: Request,
    e_id:int,
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    number: int = Form(...),
    qualification: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db),
    ):
    
    # Read the file data
    file_data = await file.read()

    # Retriving Employee using ID
    db_emp = db.query(Employee).filter(Employee.id == e_id).first()
    print("db_emp.e_name :", db_emp.e_name)
    # IF Id in not matching
    if db_emp is None:
        raise HTTPException(status_code=404, detail="File not found")

    db_emp.e_name = name
    db_emp.email = email
    db_emp.number = number
    db_emp.qualification = qualification
    db_emp.role = role
    db_emp.filename = file.filename
    db_emp.file_data = file_data

    print("name :", name)
    
    db.commit()

    return JSONResponse(content={"id": db_emp.id,"message":"Successfully Updated"}) 


@app.get("/get_allemployees/")
def get_allemployees(db:Session = Depends(get_db)):
    employees = db.query(Employee).all()
    emp_data = []

    for emp  in employees:
        emp_data.append({
                          "id": emp.id,
                          "details":{
                              "name": emp.e_name,
                              "contact_details":{
                                   "email": emp.email,
                                   "number": emp.number
                                    }
                              },
                          "job_details":{
                               "qualification": emp.qualification,
                               "role": emp.role,
                               "resume": emp.filename
                          }
                         })
        
    return JSONResponse(content={"Employees": emp_data})


# ------------------------------------User and Admin Registration-----------------------------------------------------------
# Get the HTML For Create_User.
@app.get("/register/")   
def get_register(request : Request):
    return templates.TemplateResponse("register.html",{"request":request})

# Pydantic models for data validation
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'admin' or 'candidate'

# User Routes
@app.post("/admin/register/" ,response_class=HTMLResponse)
def register(
    request: Request, 
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)):
    
    db_user = User(username=username, password=password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(content={"User": "db_user"})

# ------------------------Admin Registration----------------------------------------- 
# # Get the HTML For Create_User.
# @app.get("/create_admin/")   
# def create_user(request : Request):
#     return templates.TemplateResponse("create_admin.html",{"request":request})

# # User Routes
# @app.post("/admin/create_admin/" ,response_class=HTMLResponse)
# def create_admin(
#     request: Request, 
#     username: str = Form(...),
#     password: str = Form(...),
#     role: str = Form(...),
#     db: Session = Depends(get_db)):
    
#     db_admin = User(username=username, password=password, role=role)
#     db.add(db_admin)
#     db.commit()
#     db.refresh(db_admin)
#     return JSONResponse(content={"Admin": "Admin seccessfull"})

# -------------------------------Login For User---------------------------------------
# Get the HTML For user_login.
@app.get("/user_login/")   
def create_user(request : Request):
    return templates.TemplateResponse("user_login.html",{"request":request})

# Admin Routes
@app.post("/user/login/", response_class=HTMLResponse)
def user_login(
    request: Request, 
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)):
    
    users = db.query(User).all()
    print(username)
    print(password)
    
    for user in users:
        print(user.username)
        if username == user.username and password == user.password:
            print("user :",user.username)
            print("user :",user.password)
            # return JSONResponse(content={"user": "User Logged in seccessfully"})
            return templates.TemplateResponse("user_logged_in.html",{"request":request,"user":user})
       
    return JSONResponse(content={"Error": "Wrong Username or Password"})
        
# -----------------------Login For Admin------------------------------------------------
# Get the HTML For Admin_login.
@app.get("/admin_login/")   
def create_user(request : Request):
    return templates.TemplateResponse("admin_login.html",{"request":request})

# Admin Routes
@app.post("/admin/login/", response_class=HTMLResponse)
def admin_login(
    request: Request, 
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)):
    
    users = db.query(User).all()
    
    for user in users:
        if user.username == username and user.password == password:
            # return JSONResponse(content={"user": "Admin Logged in seccessfully"})
            return templates.TemplateResponse("admin_logged_in.html",{"request":request})

    return JSONResponse(content={"Error": "Wrong Username or Password"})
        
# -----------------------------Index page Link------------------------------------------
@app.get("/index/")   
def create_user(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})
        