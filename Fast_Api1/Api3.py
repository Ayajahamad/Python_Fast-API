# Pydantic model Declaration
# if we want to send it as Body then use Pydantic Model

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Name_validation(BaseModel):
    name : str = None # None means Not Required
    age : int
    salary : float
    
@app.get("/")
def getMethod(Name_validation:Name_validation):
    return {Name_validation}

@app.post("/postdata")
def postMethod(Name_validation:Name_validation):
    print(Name_validation)
    return {
        Name_validation.name
            }

# Using this also we can send it as a body request
from fastapi import Body
@app.post("/postdataBody")
def postdataBody(Name_validation:Name_validation,status:str=Body(...)):
    print(Name_validation)
    return {
        "name" : Name_validation.name,
        "status" : status
            }