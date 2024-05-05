from pydantic import BaseModel, EmailStr
from datetime import datetime

class LogisticTest(BaseModel):
    age: int
    work_experience: float 
    gender: str 
    ever_married: str 
    graduated: str 
    profession: str 

