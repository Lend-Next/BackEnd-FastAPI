from pydantic import BaseModel
from typing import Optional

# class UserCreate(BaseModel):
#     first_name: str
#     last_name: str
#     email : str
#     mobile_number: int
#     encrypted_enpassword: str
#     user_type: str
#     is_active: bool = True
    
#     class Config:
#         orm_mode = True

# class ResponseUser(BaseModel):
#     email : str
#     encrypted_enpassword: str
#     class Config:
#         orm_mode = True
class UserEmail(BaseModel):
    email:str
    
class CreateUser(BaseModel):
    firstName: str
    lastName: str
    email: str
    # mobile_number: Optional[str]= None
    password: str

class ConfirmUser(BaseModel):
    email: str
    confirmationCode: str

class SigninUser(BaseModel):
    email: str
    password: str