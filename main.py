from fastapi import FastAPI,HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserCreate,UserUpdate
from ariadne.asgi import GraphQL
from schema import schema
app = FastAPI()

app.mount("/graphql",GraphQL(schema,debug=True))

MONGODB_URL= "mongodb://localhost:27017"
client= AsyncIOMotorClient(MONGODB_URL)
db= client["graphql"]
users_collection = db["test"]

@app.post("/users")
async def create_user(user_data:UserCreate):
    try:
        user_data = user_data.dict()
        result = await users_collection.insert_one(user_data)
        return {"inserted successfully"}
    except Exception as e:
        return e
@app.get("/users/{name}")
async def get_user(name:str):
    user = await users_collection.find_one({"name":name})
    if user:
        user["_id"] = str(user["_id"])
        return user
    else:
        raise HTTPException(status_code=404, detail="user not found")
    
@app.put("/users/{name}")
async def update_user(name:str,UserUpdate:dict):
    result = await users_collection.update_one({"name":name},{"$set":UserUpdate})
    if result.modified_count == 1:
        return {"updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")   


@app.delete("/users/{name}")
async def delete_user(name:str):
    result = await users_collection.delete_one({"name":name})
    if result.deleted_count == 1:
        return {"deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")     