from pydantic import BaseModel
from typing import List
class UserBase(BaseModel):
    full_name: str
    email: str

class UserLogin(BaseModel):
    email:str 
    password: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class Flower(BaseModel):
    name: str
    count: int
    cost: int

class Flowers(BaseModel):
    flowers: List[Flower]
    total_cost: int
