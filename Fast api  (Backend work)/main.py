from fastapi import FastAPI

app=FastAPI()

data={
    "pool1":{
        "name" : "Ali",
        "roll_no" : 176578,
        "age" : 20,
        "father_name": "noman",
        "salary":90
    },
    "pool2":{
        "name" : "Zeeshan",
        "roll_no" : 1765570,
        "age" : 22,
        "father_name": "Farhan",
        "salary":94
    }
}





@app.get("/")
def first_api(): #route
    return {"message": 'Hello World'}

#/about (mai saylani ka student hun)
@app.get("/about")
def second_api():
    return {"mai saylani ka student hun"}

@app.get("/view")  #Saara data show hoga
def view_data():
    return data

@app.get("/fetch_specific_data")
def specific_user(data_id: str):
    if data_id in data:
        return data[data_id] 
    return {"error":"Yeh ID nhi hay"}





#making an environment 
#python -m venv environmentname
# for activatng our environment
#venv\Scripts\activate
# If our name of environment ocmes before file name so the environment is active
#If we install fast api at a single time in our environment so at next time,we only want to activate our environment and fastapi is working.
#Lets we can sending the request on server
#uvicorn filename:app(the object that carry our api function) --reload
# write /docs after localhsot so we get the detaied result
#for deactivate our environment
# deactivate venv

# The route in this 