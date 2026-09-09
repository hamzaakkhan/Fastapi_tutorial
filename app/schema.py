from typing import Literal, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
class Student(BaseModel):
    id : int = None
    name : str
    age : int
    major : str
    gpa : float

class UpdateStudent(BaseModel):
    name : str = None
    age : int = None
    major : str = None
    gpa : float = None

class userResponse(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime
    class Config:
            orm_mode = True

class StudentResponse(Student): 
    user_id : int
    user : userResponse

    class Config:
        orm_mode = True

class StudentVote(BaseModel):
     student : StudentResponse
     votes : int

     class Config:
        orm_mode = True
     

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    phone: int


class login(BaseModel):
     email: EmailStr
     password: str

class Token(BaseModel):
     access_token : str
     token_type : str

class TokenData(BaseModel):
     id: Optional[int] = None

class Vote(BaseModel):
     stu_id : int
     dir : Literal[0,1]