from fastapi import FastAPI ,Path
import json
from pydantic import BaseModel,Field
from typing import Annotated

# annotated: Type + extra rule lagana
# annotated se app 

class pydantic(BaseModel):
    name: Annotated[str|None, Field(default=None,min_length=0,max_length=50)] = None
    age: Annotated[int|None, Field(default=None, le=70,gt=10)]= None
    course: Annotated[str|None, Field(default=None, min_length=0,max_length=50)] = None




app=FastAPI()

# class pydantic(BaseModel):  #we can also takes another class name
#     name:str
#     age:int
#     course:str






def load_data():
    with open("data.json","r") as f:
        data=json.load(f)
        return data
    
def save_data(data):
    with open("data.json","w") as f:
        json.dump(data,f,indent=4) # indent=4 can gives us our data in vertical form




@app.get("/")
def first_api():
    return {"message":"Hello world"} #we make a dictionary like in a json format,because every language can except the code in the json format.

@app.get("/about")
def second_api():
    return {"message":"Hello about"}

@app.get("/view")
def show_data():
    data=load_data()
    return data

@app.get("/single/{id}")  #subroute
def specific_user(id:str): #Id is in string format due to json
    data = load_data()
    if id in data:
        return data[id]
    return {"Message":"Yeh Id exist nhi karti"}


#Post request
@app.post("/create")  #post can creates new data
def create_data(data_id:str,new_data:pydantic):  #From pydantic we can adds a validation ,for taking required inputs.
    data=load_data()

    #Id ko check krraha hay
    if data_id in data:
        return {"Message":"Yeh ID pehlay say exist karti hay"}
    # data create karraha hay
    data[data_id] = new_data.model_dump() #It(model.dump) converts  into json(dictionary) format
    save_data(data)
    return {
        "message": "New data Added Succesfully",
        "patient": data_id,
        "patient_data":new_data
    }

@app.put("/update_data")   #It is for updating our data
def update_data(id:str,update_data:dict):
    data=load_data()

    if id not in data:
        return {"message":"Yeh ID pehlay say mojood hay"}
    data[id].update(update_data)
    save_data(data) #It saves our updated results
    return {
        "message":"Data update hogaya",
        "patient":id,
        "patient_data":update_data
    }

@app.delete("/delete")
def delete_data(id:str=Path(...,description="Yahan aapko ID deni hay",example="p0065")):
    data=load_data()

    if id not in data:
        return {"message":"This ID is not Available"}
    delete_item = data.pop(id)   #We can also do this by using del() function del(data[id])
    save_data(data)
    return {
        "message":"Data Deleted Succesfully",
        "patient":id,
        "Deleted":delete_item
    }

    
    

