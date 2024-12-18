from urllib import request
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from io import BytesIO
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Form
import mimetypes
import os

# Database setup
DATABASE_URL = "postgresql://postgres:Postgres%40123@localhost/postgres"
Base = declarative_base()

# Updated FileRecord Model with name and email
class FileRecord(Base):
    __tablename__ = 'files1'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_data = Column(LargeBinary)
    name = Column(String, index=True)  # New column for name
    email = Column(String, index=True)  # New column for email
    

# Database connection setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Set the directory for templates

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to serve the upload form
@app.get("/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# # Route to handle file upload
# @app.post("/upload/", response_class=HTMLResponse)
# async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     file_data = await file.read()
    
#     # Save the file to the database
#     db_file = FileRecord(filename=file.filename, file_data=file_data)
#     db.add(db_file)
#     db.commit()
#     db.refresh(db_file)
    
#     # Redirect to download page with file ID
#     return f"""
#     <h1>File Uploaded Successfully!</h1>
#     <p>File ID: {db_file.id}</p>
#     <p><a href="/download/{db_file.id}">Click here to download the file</a></p>
#     """



# @app.post("/upload/", response_class=HTMLResponse)
# async def upload_file(
#     file: UploadFile = File(...),
#     name: str = Form(...),  # Accept name
#     email: str = Form(...),  # Accept email
#     db: Session = Depends(get_db)
# ):
#     file_data = await file.read()

#     # Save the file to the database along with name and email
#     db_file = FileRecord(filename=file.filename, file_data=file_data, name=name, email=email)
#     db.add(db_file)
#     db.commit()
#     db.refresh(db_file)
    
#     # Redirect to display the uploaded files in a card format
#     # return templates.TemplateResponse("files.html", {"request": request, "files": files})
#     return f"""
#     <h1>File Uploaded Successfully!</h1>
#     <p>File ID: {db_file.id}</p>
#     <p>Name: {db_file.name}</p>
#     <p>Email: {db_file.email}</p>
#     <p>Filename: {db_file.filename}</p>
#     <p><a href="/download/{db_file.id}">Click here to download the file</a></p>
#     """


## Upload File
# @app.post("/upload/", response_class=HTMLResponse)
# async def upload_file(
#     request: Request ,
#     file: UploadFile = File(...),
#     name: str = Form(...),  # Accept name
#     email: str = Form(...),  # Accept email
#     db: Session = Depends(get_db),
    
# ):
#     file_data = await file.read()

#     # Save the file to the database along with name and email
#     db_file = FileRecord(filename=file.filename, file_data=file_data, name=name, email=email)
#     db.add(db_file)
#     db.commit()
#     db.refresh(db_file)

#     # Render the success page using the uploaded file's details
#     return templates.TemplateResponse(
#         "upload_success.html", 
#         {
#             "request": request, 
#             "file_id": db_file.id, 
#             "name": db_file.name, 
#             "email": db_file.email, 
#             "filename": db_file.filename
#         }
#     )

## Upload File with Restrictions only Pdf Files
@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    name: str = Form(...),  # Accept name
    email: str = Form(...),  # Accept email
    db: Session = Depends(get_db),
):
    # Check the file type
    mime_type, _ = mimetypes.guess_type(file.filename)
    
    # If the MIME type is not PDF, raise an error
    if mime_type != "application/pdf":
        # raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        return HTMLResponse(content=f"""
        <html>
            <head>
                <script type="text/javascript">
                    alert('Error..! Only PDF files are allowed..!');
                    window.location.href = '/'; 
                </script>
            </head>
            <body>
            </body>
        </html>
    """)    




    # ---------
    uploaded_files = []
    UPLOAD_DIRECTORY = os.path.abspath("./uploads")
    print(UPLOAD_DIRECTORY)

    print(file.filename)
        
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
        
    
    uploaded_files.append(file.filename)
    # --------------
        
    # Read the file data
    file_data = await file.read()

    # Save the file to the database along with name and email
    db_file = FileRecord(filename=file.filename, file_data=file_data, name=name, email=email)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    # Render the success page using the uploaded file's details
    return templates.TemplateResponse(
        "upload_success.html", 
        {
            "request": request, 
            "file_id": db_file.id, 
            "name": db_file.name, 
            "email": db_file.email, 
            "filename": db_file.filename
        }
    )

# Route to serve the download form
@app.get("/download/", response_class=HTMLResponse)
async def get_download_form(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})


# # Route to handle file download
# @app.get("/download/{file_id}")
# async def download_file(file_id: int, db: Session = Depends(get_db)):
#     # Fetch the file from the database
#     db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
#     if db_file is None:
#         raise HTTPException(status_code=404, detail="File not found")
    
#     # Return the file as a stream for downloading
#     return StreamingResponse(BytesIO(db_file.file_data), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={db_file.filename}"})

@app.get("/download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    # Fetch the file from the database
    db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return the file as a stream for downloading
    return StreamingResponse(BytesIO(db_file.file_data), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={db_file.filename}"})

@app.get("/files/", response_class=HTMLResponse)
async def get_uploaded_files(request: Request, db: Session = Depends(get_db)):
    # Retrieve all file records from the database
    files = db.query(FileRecord).all()
    
    # Return the list of files to the template
    return templates.TemplateResponse("files.html", {"request": request, "files": files})


# @app.post("/delete/{file_id}", response_class=HTMLResponse)
# async def delete_file(file_id: int, db: Session = Depends(get_db)):
#     # Fetch the file from the database
#     db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
#     if db_file is None:
#         raise HTTPException(status_code=404, detail="File not found")
    
#     # Delete the file record from the database
#     db.delete(db_file)
#     db.commit()
    
#     # Redirect to the files page after deletion
#     return """
#     <h1>File Deleted Successfully!</h1>
#     <p><a href="/files/">Go back to the list of files</a></p>
#     """


@app.post("/delete/{file_id}", response_class=HTMLResponse)
async def delete_file(file_id: int,request: Request, db: Session = Depends(get_db)):
    # Fetch the file from the database
    db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete the file record from the database
    db.delete(db_file)
    db.commit()
    
    # Reset the sequence so that the next inserted ID starts from the last maximum value
    # db.execute("SELECT setval(pg_get_serial_sequence('files1', 'id'), (SELECT MAX(id) FROM files1));")
    # db.commit()

    # # Redirect to the files page after deletion
    # return templates.TemplateResponse("file_deleted.html", {"request": request})
    
    return HTMLResponse(content=f"""
        <html>
            <head>
                <script type="text/javascript">
                    alert('File deleted successfully!');
                    window.location.href = '/files/'; 
                </script>
            </head>
            <body>
            </body>
        </html>
    """)





@app.get("/update/{file_id}", response_class=HTMLResponse)
async def get_update_form(file_id: int, request: Request, db: Session = Depends(get_db)):
    # Fetch the file from the database
    db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return the update form with current data
    return templates.TemplateResponse("update.html", {
        "request": request,
        "file": db_file
    })

# @app.post("/update/{file_id}", response_class=HTMLResponse)
# async def update_file(file_id: int, name: str, email: str, db: Session = Depends(get_db)):
#     # Fetch the file from the database
#     db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
#     if db_file is None:
#         raise HTTPException(status_code=404, detail="File not found")
    
#     # Update the file's name and email
#     db_file.name = name
#     db_file.email = email
#     db.commit()
    
#     # Redirect back to the files list or a confirmation page
#     return f"""
#     <h1>File Updated Successfully!</h1>
#     <p>Name: {db_file.name}</p>
#     <p>Email: {db_file.email}</p>
#     <p><a href="/files/">Go back to the list of files</a></p>
#     """


# @app.post("/update/{file_id}", response_class=HTMLResponse)
# async def update_file(
#     file_id: int, 
#     name: str = Form(...),  # Accept name as form data
#     email: str = Form(...),  # Accept email as form data
#     db: Session = Depends(get_db)
# ):
#     # Fetch the file from the database
#     db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
#     if db_file is None:
#         raise HTTPException(status_code=404, detail="File not found")
    
#     # Update the file's name and email
#     db_file.name = name
#     db_file.email = email
#     db.commit()
    
#     # Redirect back to the files list or a confirmation page
#     return f"""
#     <h1>File Updated Successfully!</h1>
#     <p>Name: {db_file.name}</p>
#     <p>Email: {db_file.email}</p>
#     <p><a href="/files/">Go back to the list of files</a></p>
#     """


@app.post("/update/{file_id}", response_class=HTMLResponse)
async def update_file(
    request:Request,
    file_id: int, 
    name: str = Form(...),  # Accept name as form data
    email: str = Form(...),  # Accept email as form data
    db: Session = Depends(get_db)
):
    # Fetch the file from the database
    db_file = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Update the file's name and email
    db_file.name = name
    db_file.email = email
    db.commit()

    # Render the success page using the updated file's details
    return templates.TemplateResponse(
        "update_success.html",  # Ensure the template is saved as 'update_success.html'
        {
            "request": request,
            "name": db_file.name,
            "email": db_file.email,
            "filename": db_file.filename,
        }
    )
