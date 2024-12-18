from fastapi import FastAPI

app = FastAPI()

list_of_users = list()

@app.get("/get")
def put_method():
    return list_of_users

@app.put("/put/{user_name}")
def put_method(user_name : str):
    list_of_users.append(user_name)
    return list_of_users

@app.post("/post/{user_name}")
def post_method(user_name : str):
    list_of_users.append(user_name)
    return list_of_users

@app.delete("/delete/{user_name}")
def put_method(user_name : str):
    list_of_users.remove(user_name)
    return list_of_users


# Using all the methods in One 
@app.api_route("/homedat", methods=['GET','PUT','POST','DELETE'])
def handle_homedata(user_name : str):
    print(user_name)
    return(user_name)