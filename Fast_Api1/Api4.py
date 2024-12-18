# Rendering HTML File.
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="htmldirectory")

class NameValues(BaseModel):
    name:str = None
    country:str
    age:int
    salary:float

@app.get("/home/{user_name}", response_class= HTMLResponse)
def getHtml(request: Request, user_name:str):
    return templates.TemplateResponse("home.html",{"request":request, "user_name":user_name})