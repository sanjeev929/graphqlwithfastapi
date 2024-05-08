from pydantic import BaseModel

class UserCreate(BaseModel):
    name:str
    email:str
    age:int

class UserUpdate(BaseModel):
    name:str
    email:str
    age:int

class User(UserCreate):
    id:str        