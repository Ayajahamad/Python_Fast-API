from typing import List
from fastapi import Depends, FastAPI, Request, UploadFile, File, Form, HTTPException, status, Body
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import SessionLocal, User
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
        
# To Get the Register Page Page
@app.get("/register/", response_class = HTMLResponse)
def get_homepage(request : Request):
    return templates.TemplateResponse("register.html",{"request":request})

# To Get the Login Page Page
@app.get("/login/", response_class = HTMLResponse)
def get_homepage(request : Request):
    return templates.TemplateResponse("login.html",{"request":request})

# To Get the Login Page Page
@app.get("/users_all/", response_class = HTMLResponse)
def get_homepage(request : Request):
    return templates.TemplateResponse("allusers.html",{"request":request})

# Pydantic models for data validation
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'admin' or 'candidate'

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    
@app.post("/register/user/", response_model = UserCreate)
def user_register(user: UserCreate, db: Session = Depends(get_db)):
    
    # Check if the username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=user.username, password=user.password, role=user.role)
    
    # Save the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the created user
    return new_user


# Models for Login Request and Response
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login/",response_model = UserResponse)
def login_user(login: LoginRequest = Body(...), db: Session = Depends(get_db)):
    
     # Fetch user by username
    db_user = db.query(User).filter(User.username == login.username).first()
    
    # Check if user exists and passwords match
    if db_user and db_user.password == login.password:
        return {
            "id": db_user.id,
            "username": db_user.username,
            "role": db_user.role
        }
    
    # Raise an exception if authentication fails
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )

@app.get("/password/{u_id}")
def get_pass(request:Request ,u_id,db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == u_id).first()
    
    if db_user:
        return templates.TemplateResponse("update.html",{"request":request,"user":db_user})
    

@app.put("/password/update/", response_model = UserResponse)
def update_password(login: LoginRequest = Body(...), db: Session = Depends(get_db)):
    
    # Fetch user by username
    db_user = db.query(User).filter(User.username == login.username).first()
    
    if db_user:
        db_user.password = login.password
    
        db.commit()
        db.refresh(db_user)
    
        return db_user
    
@app.get("/allusers/", response_model = List[UserResponse])
def getall_users(request : Request, db: Session = Depends(get_db)):
    
    users = db.query(User).all()
    
    # print(users_response)

    return users

@app.delete("/delete/{u_id}")
def delete_user(request:Request ,u_id,db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == u_id).first()
    
    if db_user:
        db.delete(db_user)
        db.commit()
        
    return {"message":"deleted successfully"}
    