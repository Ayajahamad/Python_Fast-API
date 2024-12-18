from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def home_page():
    return {
        'name' : 'abc',
        'age' : 20
        }
# http://127.0.0.1:8000/home


@app.get("/home/{user_name}")
def passing_parameter(user_name : str):
    return {
        "name" : user_name,
        "age" : 24
        }
# http://127.0.0.1:8000/home/username


@app.get("/query/{user_name}")
def passing_parameter_Query(user_name : str, query):
    return {
        "name" : user_name,
        "age" : 24,
        "query" : query
        }
# http://127.0.0.1:8000/query/username?query=password - calling